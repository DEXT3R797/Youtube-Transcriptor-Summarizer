from flask import Flask, render_template , request,redirect,session
from flask_sqlalchemy import SQLAlchemy
from text_summary import sunmmarizer
from transc import get_transcript
import bcrypt


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
db=SQLAlchemy(app)
app.secret_key ='secret_key'

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(100),unique=True)
    password= db.Column(db.String(100))

    def __init__(self, email, password, name):
        self.name = name
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    
with app.app_context():
    db.create_all()

@app.route('/home')
def home():
    return render_template('home.html')
@app.route('/')
def home2():
    return render_template('home2.html')



@app.route('/trans', methods=['GET','POST'])
def trans():
    #handle reques of transcript
    if request.method=='POST':
        urll=request.form['urll']
        transcript=get_transcript(urll)
        return render_template('home2.html',transcript=transcript)
@app.route('/analyze', methods=['GET','POST'])
def analyze():
    #handle reques of summary
    if request.method == 'POST':
        rawtext=request.form['rawtext']
        summary,original_text,len_orig_txt,len_summary=sunmmarizer(rawtext)
    return render_template('summary.html',summary=summary,original_text=original_text,len_orig_txt=len_orig_txt,len_summary=len_summary)  
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
            #handle reques of login
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['name']= user.name
            session['email']= user.email
            session['password']= user.password
            return redirect('/home')
        else:
             return render_template('login.html',error="Invalid User")
            
        
    return render_template('login.html')



@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
            #handle reques of register
        name=request.form['name']
        email=request.form['email']
        password=request.form['password']

        new_user=User(name=name,email=email,password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')

    return render_template('register.html')


if __name__== '__main__':
    app.run(debug=True)
