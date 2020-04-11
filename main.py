from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
import os
from werkzeug import secure_filename
from flask_mail import Mail,Message
from functools import wraps
#from data import Articles

app = Flask(__name__)
app.secret_key = 'super-secret-key'
app.config['UPLOAD_FOLDER'] = "C:\\Users\\DELL\\Desktop\\WEB_DEV\\Web Flask1\\static\\profilepics"

app.config.update(
        MAIL_SERVER = 'smtp.gmail.com',
        MAIL_PORT = '465',
        MAIL_USE_SSL = True,
        MAIL_USERNAME ="arpanchowdhury050@gmail.com",
        MAIL_PASSWORD = "google123#",
        )
mail = Mail(app)

#config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'learn'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#initialize MySQL

mysql = MySQL(app)

#check user if logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorised, Please login','danger')
            return redirect(url_for('login'))
    return wrap

#Articles = Articles()

@app.route('/')
def index():
     #create a cursor
    cur = mysql.connection.cursor()
        
    #get user by username
    result = cur.execute("SELECT * from users")
    if result > 0:
        users = cur.fetchall()
    result = cur.execute("SELECT * from articles ORDER BY comment_count DESC")
    articles = cur.fetchall()
    article = articles[0]
    id = article['id']
    
    liked = 0
    if 'username' in session:
        flag = cur.execute("SELECT * FROM likes WHERE liker_username = %s AND article_id=%s",(session['username'],id))
        
        liked = len(cur.fetchall())
    
    return render_template('index.html',users=users,article  = article,liked=liked)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    cur = mysql.connection.cursor()
    result = cur.execute('SELECT * from articles')
    
    articles = cur.fetchall()
    
    if result > 0:
        return render_template('articles.html',articles=articles)
    else:
        msg = 'No articles found'
        return render_template('articles.html',msg=msg)
    cur.close()


@app.route('/articles/<string:id>',methods = ["GET"])
def article_route(id):
    cur = mysql.connection.cursor()
    result = cur.execute('SELECT * from articles WHERE id = %s',[id])
    if result > 0:
        article = cur.fetchone()
        
        result = cur.execute('SELECT * from comments WHERE article_id = %s',[id])
        
        comments = cur.fetchall()
        
        liked=0
        if 'username' in session:
            flag = cur.execute("SELECT * FROM likes WHERE liker_username = %s AND article_id=%s",(session['username'],id))
        
            liked = len(cur.fetchall())
        
        cur.close()
        return render_template('article_route.html',article=article,comments = comments,liked=liked)


class CommentForm(Form):
    body = StringField('Name',[validators.Length(min=1, max=200)])
    
    
@app.route('/articles/article_comment/<string:id>',methods = ["GET","POST"])
@is_logged_in
def article_comment(id):
    
    form = CommentForm(request.form)
    if request.method == 'POST' and form.validate():
        body = form.body.data
        author = session["username"]
        
        #create cursor
        
        cur = mysql.connection.cursor()
        
        result = cur.execute("SELECT * FROM articles WHERE id=%s",[id])
        
        count = cur.fetchone()['comment_count']
        #execute query
        cur.execute("INSERT INTO comments(article_id,author,body) VALUES(%s, %s, %s)",
                    (id,author,body))
        cur.execute("UPDATE articles SET comment_count=%s WHERE id=%s",(count+1,id))
        
        #commit to db
        mysql.connection.commit()
        
        #close connection
        cur.close()
        
        flash('Comment Added', 'success')
        return redirect('/articles/' +str(id))
        
    return render_template('comment_form.html')


    



class RegisterForm(Form):
    name = StringField('Name',[validators.Length(min=1, max=50)])
    username = StringField('Username',[validators.Length(min=4, max=25)])
    email = StringField('Email',[validators.Length(min=6, max=50)])
    password = PasswordField('Password',[
            validators.DataRequired(),
            validators.EqualTo('confirm',message='Password do not match')
            ])
    confirm = PasswordField('Confirm Password')
    
@app.route('/register',methods=["GET","POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        
        #create cursor
        
        cur = mysql.connection.cursor()
        
        #execute query
        cur.execute("INSERT INTO users(name,username,password,email) VALUES(%s, %s, %s, %s)",
                    (name,username,password,email))
        
        #commit to db
        mysql.connection.commit()
        
        #close connection
        cur.close()
        
        flash('You are now registered and can login', 'success')
        return redirect(url_for('index'))
        
    return render_template('register.html',form=form)

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password_candidate = request.form['password']
        
        #create a cursor
        cur = mysql.connection.cursor()
        
        #get user by username
        result = cur.execute("SELECT * from users WHERE username = %s", [username])
        
        if result > 0:
            data = cur.fetchone()
            password = data['password']
            name = data['name']
            
            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username
                
                flash('You are now logged in'+" " + str(name) ,'success')
                return redirect(url_for('dashboard'))
            
            else:
                error = "Invalid login credential"
                return render_template('login.html',error = error)
            
            cur.close()
        else:
            error = "Username not found"
            return render_template('login.html',error = error)
            
    return render_template('login.html')


@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out','success')
    return redirect(url_for('login'))
    

@app.route('/dashboard')
@is_logged_in
def dashboard():
    cur = mysql.connection.cursor()
    result = cur.execute('SELECT * from articles WHERE author = %s',[session['username']])
    
    articles = cur.fetchall()
    
    if result > 0:
        return render_template('dashboard.html',articles=articles)
    else:
        msg = 'No articles found'
        return render_template('dashboard.html',msg=msg)
    cur.close()

class ArticleForm(Form):
    title = StringField('Title',[validators.Length(min=1, max=200)])
    body = TextAreaField('Body',[validators.Length(min=30)])
    

@app.route('/add_article',methods=['GET','POST'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method == "POST" and form.validate():
        title = form.title.data
        body = form.body.data
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO articles(title,body,author) VALUES(%s, %s, %s)",(title,body,session['username']))
        mysql.connection.commit()
        cur.close()
        
        flash('Article created','success')
        
        return redirect(url_for('dashboard'))
    
    return render_template('add_article.html',form=form)                    
                        



@app.route('/edit_article/<string:id>',methods=['GET','POST'])
@is_logged_in
def edit_article(id):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM articles WHERE id = %s",[id])
    
    if result > 0:
        article = cur.fetchone()
    
    form = ArticleForm(request.form)
    
    form.title.data = article['title']
    form.body.data = article['body']
    
    if request.method == "POST" and form.validate():
        title = request.form['title']
        body = request.form['body']
        
        cur = mysql.connection.cursor()
        cur.execute("UPDATE articles SET title=%sbody=%s WHERE id=%s",(title,body,id))
        mysql.connection.commit()
        cur.close()
        
        flash('Article Updated','success')
        
        return redirect(url_for('dashboard'))
    
    return render_template('edit_article.html',form=form) 

@app.route('/delete_article/<string:id>',methods=['GET','POST'])
@is_logged_in
def delete_article(id):
    cur = mysql.connection.cursor()
    
    cur.execute("DELETE FROM articles WHERE id = %s",[id])
    mysql.connection.commit()
    cur.close()
    
    flash('Article Deleted','success')
        
    return redirect(url_for('dashboard'))
       

@app.route('/profile')
@is_logged_in
def profile():
    username = session['username']
    #create a cursor
    cur = mysql.connection.cursor()
        
    #get user by username
    result = cur.execute("SELECT * from users WHERE username = %s", [username])
    if result > 0:
        data = cur.fetchone()
        #name = data['name']
        #uname = data['username']
        
    cur = mysql.connection.cursor()
    result1 = cur.execute('SELECT * from articles WHERE author = %s',[session['username']])
    
    articles = cur.fetchall()
    cur.close()
        
    return render_template('profile.html',data=data,articles=articles)
    
@app.route('/profile_route/<string:sno>')
def profile_route(sno):
    #create a cursor
    cur = mysql.connection.cursor()
        
    #get user by username
    result = cur.execute("SELECT * from users WHERE sno = %s", [sno])
    if result > 0:
        data = cur.fetchone()
        #name = data['name']
        uname = data['username']
        
    cur = mysql.connection.cursor()
    result1 = cur.execute('SELECT * from articles WHERE author = %s',[uname])
    
    
    articles = cur.fetchall()
    
    if len(articles) == 0:
        flash("No articles to show",'success')
    cur.close()
        
    return render_template('profile_route.html',data=data,articles=articles)

    


@app.route('/uploader',methods=["GET","POST"])
@is_logged_in
def uploader():
    if request.method == "POST":
        if 'file1' not in request.files:
            flash("No file chosen",'danger')
            return redirect('/profile')
            
        f = request.files['file1']
        
        name = f.filename
        #creating cursor
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET propic=%s WHERE username = %s",(name,session['username']))
        mysql.connection.commit()
        cur.close()
        
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        flash("Profile Picture uploaded successfully",'success')
        return redirect('/profile')
    
@app.route('/articles/article_like/<string:id>',methods = ["GET","POST"])
@is_logged_in
def article_like(id):

    author = session['username']  
     #create cursor
        
    cur = mysql.connection.cursor()
        
    result = cur.execute("SELECT * FROM articles WHERE id=%s",[id])
        
    count = cur.fetchone()['like_count']
        #execute query
    cur.execute("UPDATE articles SET like_count=%s WHERE id=%s",(count+1,id))
    cur.execute("INSERT INTO likes(article_id,liker_username) VALUES(%s, %s)",(id,author))
        
        #commit to db
    mysql.connection.commit()
        
        #close connection
    cur.close()
        
    flash('Article Liked', 'success')
    return redirect('/articles/' +str(id))


@app.route('/articles/article_dislike/<string:id>',methods = ["GET","POST"])
@is_logged_in
def article_dislike(id):

     #create cursor
        
    cur = mysql.connection.cursor()
        
    result = cur.execute("SELECT * FROM articles WHERE id=%s",[id])
        
    count = cur.fetchone()['like_count']

    #execute query
    cur.execute("UPDATE articles SET like_count=%s WHERE id=%s",(count-1,id))
    cur.execute("DELETE FROM likes WHERE article_id = %s",[id])
        
        #commit to db
    mysql.connection.commit()
        
        #close connection
    cur.close()
        
    flash('Article disliked', 'success')
    return redirect('/articles/' +str(id))  

@app.route('/forgot_route/',methods = ["GET","POST"])
def forgot_route():

    if request.method == "POST":
        email = request.form['email']

        cur = mysql.connection.cursor()
            
        result = cur.execute("SELECT * FROM users WHERE email = %s",[email])

        if result > 0:

            res = cur.fetchone()
            username = res['username']
            password =  res['password']

            msg = Message("Forgot Password - LeArN",
                        sender = "arpanchowdhury050@gmail.com",
                        recipients = [email])

            link = "http://127.0.0.1:5000/reset_password/" + password
            msg.body = 'Hello ' + username + ',\nYou or someone else has requested to reset password for your account.If it was you click the link : ' + link
            mail.send(msg)

            flash("A password-reset mail has been sent! Please click on the link given in the mail!",'success')
        else:
            error = "Email-id is not registered"
            return render_template('forgot_route.html',error=error)

       

    return render_template('forgot_route.html')




class ResetPasswordForm(Form):
    password = PasswordField('New Password',[
            validators.DataRequired(),
            validators.EqualTo('confirm',message='Password do not match')
            ])
    confirm = PasswordField('Re-enter new password')  

@app.route('/reset_password/<path:password>/',methods = ["GET","POST"])
def reset_password(password):
    
    form = ResetPasswordForm(request.form)

    cur = mysql.connection.cursor()
            
    result = cur.execute("SELECT * FROM users WHERE password = %s",[password])

    username = cur.fetchone()['username']

    cur.close()


    if request.method == "POST":
        password = sha256_crypt.encrypt(str(form.password.data))
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET password=%s WHERE username=%s",(password,username))
        mysql.connection.commit()
        cur.close()
        flash("Your password is changed and updated. Please login!",'success')
        return redirect(url_for('login'))


    return render_template("reset_password.html",username=username,form=form)


if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000)
    