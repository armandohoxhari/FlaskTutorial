# This is a sample Python script.
from flask import Flask, render_template
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

app.config['SECRET_KEY'] = 'bf37a96b10529f456e32fc346033a608'
posts = [
    {
        'author': 'Armando',
        'title' : 'post 1',
        'content': 'first post',
        'date_posted' : 'Oct 11 ,2022'
    },
    {
        'author': 'George',
        'title': 'post 2',
        'content': 'second post',
        'date_posted' : 'Oct 12 ,2022'
    }

        ]
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'feed_me'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route("/")
def home():

    return render_template('home.html', posts=posts)



@app.route("/random")
def random():
    con = mysql.connect()
    cur = con.cursor()
    cur.execute('SELECT name FROM recipes ORDER BY RAND() LIMIT 1')
    data = cur.fetchall()
    cur.execute('SELECT name,price FROM ingredients WHERE ingredient_id IN '
                '(SELECT ingredient_id FROM relations WHERE recipe_id ='
                '(SELECT recipe_id FROM recipes WHERE name = %s))', data)
    ing = cur.fetchall()
    return render_template('random.html', data=data, ing=ing)
    con.close()

@app.route("/veggie")
def veggie():
    con = mysql.connect()
    cur = con.cursor()
    cur.execute('SELECT name FROM recipes WHERE category= "Vegeterian" ORDER BY RAND() LIMIT 1')
    data = cur.fetchall()
    cur.execute('SELECT name,price FROM ingredients WHERE ingredient_id IN '
                '(SELECT ingredient_id FROM relations WHERE recipe_id ='
                '(SELECT recipe_id FROM recipes WHERE name = %s))', data)
    ing = cur.fetchall()
    return render_template('random.html', data=data, ing=ing)
    con.close()

@app.route("/non_veggie")
def non_veggie():
    con = mysql.connect()
    cur = con.cursor()
    cur.execute('SELECT name FROM recipes WHERE category = "Non-Vegeterian" ORDER BY RAND() LIMIT 1')
    data = cur.fetchall()
    cur.execute('SELECT name,price FROM ingredients WHERE ingredient_id IN '
                '(SELECT ingredient_id FROM relations WHERE recipe_id ='
                '(SELECT recipe_id FROM recipes WHERE name = %s))', data)
    ing = cur.fetchall()
    return render_template('random.html', data=data, ing=ing)
    con.close()
@app.route("/about")
def about():

    return render_template('about.html', title='About')

@app.route("/surprise")
def surprise():
    return render_template('test.html')





if __name__ == "__main__":
    app.run(debug=True)