from flask import Flask, g,render_template, redirect, url_for, session, abort, request, flash
from werkzeug.utils import secure_filename
import requests
from bs4 import BeautifulSoup
import psycopg2
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import glob
import pandas as pd
import random
import sys

import re

app = Flask(__name__ , static_url_path='/static')
# get directory of this file
dir = os.path.dirname(os.path.abspath(__file__))
pathsfile = os.path.join(dir, 'paths.csv')

# read filepaths form csv file in working directory
paths = {}
with open(pathsfile, 'r') as f:
    for line in f:
        key, value = line.strip().split(',')
        paths[key] = value


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = paths['dikumon']

args = sys.argv

try: 
    db = f"dbname='{args[1]}' user='{args[2]}' host='{args[3]}' password='{args[4]}'"
except:
    # set your own database name, username and password
    db = "dbname='dikumon' user='postgres' host='localhost' password='admin123'"


conn = psycopg2.connect(db)
cursor = conn.cursor() 

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

bcrypt = Bcrypt(app)

@app.route("/createaccount", methods=['POST', 'GET'])
def createaccount():
    cur = conn.cursor()
    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']
        cur.execute(f'''select * from users where username = '{new_username}' ''')
        unique = cur.fetchall()
        if  len(unique) == 0:
            cur.execute(f'''INSERT INTO users(username, password) VALUES ('{new_username}', '{new_password}')''')
            flash('Account created!')
            conn.commit()

            return redirect(url_for("home"))
        else: 
            flash('Username already exists!')
    return render_template("createaccount.html")

@app.route('/create', methods=['GET', 'POST'])
def create():
    if 'username' in session:
        curr_username = session['username']
    else:
        flash('You are not logged in.')
        return redirect(url_for("logout"))
    
    cur = conn.cursor()
    if request.method == 'POST':
        # check if the post request has the file part
        if 'picture' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['picture']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            cur.execute(f'''SELECT MAX(number) + 1 FROM dikumon''')
            number = cur.fetchone()[0]
            filename = secure_filename(f'{number}.{file.filename.rsplit(".", 1)[1].lower()}')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                #Input for new dikumon
            name = request.form['name']
            type1 = request.form['type1']
            type2 = request.form['type2']
            hp = request.form['hp']
            attack = request.form['attack']
            defense = request.form['defense']
            sp_attack = request.form['sp_attack']
            sp_defense = request.form['sp_defense']
            speed = request.form['speed']
            generation = request.form['generation']
            legendary = request.form['legendary']
            

            #Check for unique
            cur.execute(f'''select * from dikumon where name = '{name}' ''')
            unique = cur.fetchall()

            #Instert into dikumon
            if  len(unique) == 0:
                cur.execute(f'''SELECT MAX(number) + 1 FROM dikumon''')
                number = cur.fetchone()[0]
                total = sum([int(hp), int(attack), int(defense), int(sp_attack), int(sp_defense), int(speed)])
                cur.execute(f'''INSERT INTO dikumon(username, number, name, type1, type2, total, hp, attack, defense, sp_attack, sp_defense, speed, generation, legendary) 
                                VALUES ('{curr_username}', '{number}', '{name}', '{type1}', '{type2}', '{total}', '{hp}', '{attack}', '{defense}', 
                                        '{sp_attack}', '{sp_defense}', '{speed}', '{generation}', '{legendary}')''')
                flash('DIKUMON!!!!!! created!')
                conn.commit()

                return redirect(url_for("home"))
            else: 
                flash('Username already exists!')
                
    return render_template("create.html")




@app.route("/", methods=["POST", "GET"])
def home():
    cur = conn.cursor()
    #Getting 10 random rows from Attributes
    tenrand = '''select * from dikumon order by random() limit 10;'''
    cur.execute(tenrand)
    dikumons = list(cur.fetchall())
    length = len(dikumons)

    #Getting random number from table Attributes
    randname = '''select name from dikumon order by random() limit 1;'''
    cur.execute(randname)

    randomNumber = cur.fetchone()[0]
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        length = len(dikumons)
        if request.method == 'POST':
            input_id = request.form['dikumon'].title() or ""
            if re.match(r'^[A-Za-z0-9\s]+$', input_id):
                input_id = re.match(r'^[A-Za-z0-9\s]+$', input_id)
                cur.execute(f"SELECT name FROM dikumon WHERE name LIKE '{input_id[0]}%'")
                results = cur.fetchall()
                if len(results) == 1:
                    return redirect(url_for("dikumonpage", dikumon=results[0][0]))
                else:
                    search_query = request.form['dikumon']
                    cur.execute(f"SELECT * FROM dikumon WHERE name ~* '{search_query}'")
                    dikumons = cur.fetchall()
                    return render_template("dikulist.html", content=dikumons, length=len(dikumons))
            else:
                flash('Please enter a valid pokemon name.')        
        return render_template("index.html", content=dikumons, length=length, randomNumber=randomNumber)

@app.route('/login', methods=['POST'])
def do_admin_login():
    cur = conn.cursor()
    username = request.form['username']
    password = request.form['password'] 

    insys = f''' SELECT * from users where username = '{username}' and password = '{password}' '''

    cur.execute(insys)

    ifcool = len(cur.fetchall()) != 0

    if ifcool:
        session['logged_in'] = True
        session['username'] = username
    else:
        flash('wrong password!')
    return redirect(url_for("home"))


@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/logout")
def logout():
    session.pop('username', None)
    session['logged_in'] = False
    return home()

def get_dikumon_no(name):
    cur = conn.cursor()
    cur.execute(f"""SELECT number FROM dikumon where name = '{name}'""")
    number = cur.fetchone()
    # return as dict with name as key and number as value
    return int(number[0]) if number else 0

@app.route("/profile")
def profile():
    if 'username' in session:
        curr_username = session['username']
    else:
        flash('You are not logged in.')
        return redirect(url_for("logout"))
    
    cur = conn.cursor()
    
    sql1 = f"""select * from dikumon where username = '{curr_username}' """
    cur.execute(sql1)
    favs = cur.fetchall()
    length = len(favs)

    sql2 = f"""select * from reviews where username = '{curr_username}' """
    cur.execute(sql2)
    reviews = cur.fetchall()
    length_reviews = len(reviews)

    # name, number pairs dict
    d = []
    for r in reviews:
        d.append((r[2],get_dikumon_no(r[2])))
    print(d)

    
    return render_template("profile.html", content=favs, length=length, username = curr_username, reviews = reviews, length_reviews = length_reviews, dikumon_numbers = d)

@app.route('/delete_dikumon/<int:number>', methods=['POST'])
def delete_dikumon(number):
    cur = conn.cursor()
    cur.execute("SELECT * FROM dikumon WHERE number = %s AND username = %s", (number, session['username']))
    result = cur.fetchone()
    if result is None:
        flash('No such DIKUMON associated with the current user.')
        return redirect(url_for('profile'))
    cur.execute("DELETE FROM dikumon WHERE number = %s AND username = %s", (number, session['username']))
    conn.commit()
    flash('DIKUMON deleted successfully.')
    return redirect(url_for('profile'))

@app.route('/delete_review/<int:rid>', methods=['POST'])
def delete_review(rid):
    cur = conn.cursor()
    cur.execute("SELECT * FROM reviews WHERE rid = %s AND username = %s", (rid, session['username']))
    result = cur.fetchone()
    if result is None:
        flash('No such reviews associated with the current user.')
        return redirect(url_for('profile'))
    cur.execute("DELETE FROM reviews WHERE rid = %s AND username = %s", (rid, session['username']))
    conn.commit()
    flash('review deleted successfully.')
    return redirect(url_for('profile'))

@app.route('/delete_all_my_dikumon', methods=['POST'])
def delete_all_my_dikumon():
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM dikumon WHERE username = '{session['username']}'")
    result = cur.fetchall()
    if result is None:
        flash('No DIKUMON associated with the current user.')
        return redirect(url_for('profile'))
    cur.execute(f"DELETE FROM dikumon WHERE username = '{session['username']}'")
    conn.commit()
    flash('DIKUMON deleted successfully.')
    return redirect(url_for('profile'))

@app.route('/delete_all_my_reviews', methods=['POST'])
def delete_all_my_reviews():
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM reviews WHERE username = '{session['username']}'")
    result = cur.fetchall()
    print(result)
    if result is None:
        flash('No reviews associated with the current user.')
        return redirect(url_for('profile'))
    cur.execute(f"DELETE FROM reviews WHERE username = '{session['username']}'")
    conn.commit()
    flash('reviews deleted successfully.')
    return redirect(url_for('profile'))

@app.route('/delete_my_profile', methods=['POST'])
def delete_my_profile():
    
    confirm = request.form.get('confirm')
    if confirm != 'confirm':
        flash('Must check the box to confirm deletion.')
        return redirect(url_for('profile'))
    else:
        print('succes')
        cur = conn.cursor()
        cur.execute(f"delete FROM users cascade WHERE username = '{session['username']}'")
        conn.commit()
        flash('Profile deleted successfully. Redirecting to login page.')
        return redirect(url_for('logout'))

@app.route("/dikumon/<dikumon>", methods=["POST", "GET"])
def dikumonpage(dikumon):
    cur = conn.cursor()
    
    if not session.get('logged_in'):
        return render_template('login.html')
    

    sql1 = f''' select * from dikumon where name = '{dikumon}' '''
    cur.execute(sql1)
    ct = cur.fetchone()

    sql2 = f''' select * from reviews where name = '{dikumon}' '''
    cur.execute(sql2)
    reviews = cur.fetchall()
    review_count = len(reviews)
    

    return render_template("dikumon.html", content=ct, reviews = reviews, review_count = review_count)  

@app.route('/give_review/<id>/', methods=["POST"])
def give_review(id):
    username = None
    if(session['logged_in']):
        username = session.get('username')
        if request.method == 'POST':
            cur = conn.cursor()
            cur.execute('''
                SELECT max(rid) 
                FROM reviews
            ''')
            # check if nothing else max +1
            rid = 0
            results = cur.fetchone()
            if results[0] == None:
                rid = '1'
            else:
                rid = str(results[0]+1)
                
            name = id

            review = request.form['review-text']
            rating = request.form['rating']

            cur.execute('''
                INSERT INTO reviews
                VALUES (%(rid)s, %(username)s, %(name)s, %(rating)s, %(review)s)
            ''', 
            {'rid':str(rid), 'review':str(review), 'rating':rating, 'username':str(username), 'name':str(name)} 
            )
            flash('Review added!')
            conn.commit()
            return redirect('/dikumon/'+id)
        else:
            return render_template('dikumon.html')


@app.route('/dikulist', methods=["POST", "GET"])
def dikulist():
    cur = conn.cursor()
    if request.method == 'POST':
        search_query = request.form['search']
        cur.execute(f"SELECT * FROM dikumon WHERE name ~* '{search_query}'")
        dikumons = cur.fetchall()
        if len(dikumons) == 0:
            flash('No DIKUMON found.')
        else:
            flash('DIKUMON found.')
            length = len(dikumons)
            return render_template("dikulist.html", content=dikumons, length=length)
            

    else:
        cur.execute(f"SELECT * FROM dikumon")
        dikumons = cur.fetchall()
    length = len(dikumons)
    return render_template("dikulist.html", content=dikumons, length=length)

@app.route('/random_dikumon', methods=["GET"])
def random_dikumon():
    # select all dikumon names
    cur = conn.cursor()
    cur.execute("SELECT name FROM dikumon")
    names = cur.fetchall()
    # select a random name
    name = random.choice(names)[0]
    return redirect('/dikumon/'+name)



if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
