#flask - small and easy

from flask import Flask, render_template, url_for, request, redirect
import psycopg2
import multiprocessing
import time
import datetime
import csv

#django - heavyweight

# create your own virtual env?  python3 -m venv venv or python3 -m venv DIR
# windows can be py -3 -m venv venv

# not sure i need it for this, or if i want it.

print(__name__)
app = Flask(__name__)

def view() -> list:
    conn=psycopg2.connect("dbname='inteviewTableJan17' user='postgres' password='TN!B007jb' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    userRows=cur.fetchall()
    print(f"userRows = {userRows}")
    cur.execute("SELECT * FROM login")
    loginRows=cur.fetchall()

    conn.commit()
    conn.close()

    #rows = zip(userRows, loginRows)
    rows = userRows + loginRows
    for r in rows:
        print(r)
    #listRows = list(rows)
    #print(listRows)
    print(rows)
    return rows  # this is a list


def insert_name(name):
    conn=psycopg2.connect("dbname='inteviewTableJan17' user='postgres' password='TN!B007jb' host='localhost' port='5432'")
    cur = conn.cursor()
    hashed = name + "_is_hashed"
    email = name + f"@{name}.com"
    joinedTime = str(datetime.datetime.now())


    cur.execute("INSERT INTO users (name, email, joined) VALUES (%s, %s, %s)", (name, email, joinedTime))  # not great, allows sql injection
    cur.execute("INSERT INTO login (hash, email) VALUES (%s, %s)", (hashed, email))  # not great, allows sql injection
    conn.commit()
    conn.close()

def insert_names(names):
    with multiprocessing.Pool() as pool:
        pool.map(insert_name, names)

def insert():
    name = "AUSER"
    names = [name+str(i) for i in range(100)]
    start_time = time.time()
    insert_names(names)
    duration = time.time() - start_time
    print(f"Duration {duration} seconds")

def write_to_file(data):
    with open('database.txt', mode='a') as database:
        email = data['email']
        subject = data['subject']
        message = data['message']
        file = database.write(f'\n{email}, {subject}, {message}')


def write_to_csv(data):
    with open('database.csv', newline='', mode='a') as database2:
        #fieldnames = ['email', 'subject', 'message']
        #csv_writer = csv.DictWriter(database2, fieldnames=fieldnames, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        email = data['email']
        subject = data['subject']
        message = data['message']
        # look at csv module docs from python

        csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email, subject, message])


#@app.route("/<username>")  #can pass username on
#def hello_world(username=None):
@app.route("/<username>/<int:post_id>")  #can pass username on
def hello_world(username=None, post_id=None):

    #print(url_for('static', filename='Pyramid.ico'))
    #return "<p>Hello, Kev!</p>"
    return render_template("Myindex.html", name=username, post_id=post_id)

@app.route("/")
def my_home():
    return render_template("index.html")

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    error = None
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            ##if valid_login(request.form['username'],
            ##               request.form['password']):
            ##    return log_the_user_in(request.form['username'])
            ##else:
            ##    error = 'Invalid username/password'
            #print(data)
            write_to_csv(data) # write_to_file(data)
            return redirect('./thankyou.html')  #'form submitted hooorayyy!'
        except:
            return 'did not save to database'
    else:
        return 'form submitted but badly!'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    ##return render_template('login.html', error=error)

@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


'''
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)
'''

'''
@app.route("/index.html")
def index():
    return render_template("index.html")

#@app.route("/about.html")
@app.route("/about.html")
def about():
    return render_template("about.html")

@app.route("/works.html")
def works():
    return render_template("works.html")

@app.route("/contact.html")
def contact():
    return render_template("contact.html")

@app.route("/blog.html")
def blog():
    return "<p>These are my thoughts on blogs</p>"

@app.route("/dbview.html")
def viewdb():
    rows = view()
    print(rows)
    return f"<p>{rows}</p>"

@app.route("/dbinsert.html")
def insertdb():
    insert()
    return "<p>inserted</p>"
    #print(rows)
    #return f"<p>{rows}</p>"

'''

# set FLASK_ENV=development will auto restart when a change is detected and reload
# set FLASK_APP=PYTHONFILE.PY
# flask run

def theserver():
    pass

if __name__ == "__main__":
    print("running server main")

'''

what is the {{ STUFF like url_for }}

they are python expressions to be evaluated via Ginger(?)

'''