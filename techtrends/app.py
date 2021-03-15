import sqlite3
import datetime
from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
from datetime import datetime
import logging
# Function to get a database connection.
count = 0

# This function connects to database with the name `database.db`
def get_db_connection():
    global count
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    count +=1
    return connection





# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post






# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'



@app.route('/healthz')
def healthz():
    response = app.response_class(
            response=json.dumps({"result":"OK - healthy"}),
            status=200,
            mimetype='application/json'
    )

    ## log line
    
    return response 




@app.route('/metrics')
def metrics():
    # var = app.response_class(
    #         response=json.dumps({"status":"success","code":0,"data":{"UserCount":14,"UserCountActive":2}}),
    #         status=200,
    #         mimetype='application/json'
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    number_of_post = len(posts)
    value = {"database_count": count, "number_of_post": number_of_post}
    return value




    

    ## log line
    
    # return var


@app.route('/docker')
def hello():
    return " successfully dockerized"










# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
        log_message(
            '"{id}" does not exist'.format(id=post_id))
        return render_template('404.html'), 404
    else:
      log_message('"{title}" recovered'.format(title=post['title']))
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    log_message('The page is recovered!')
    return render_template('about.html')













# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            log_message( '"{title}" Successfully Created'.format(title=title))
            return redirect(url_for('index'))

    return render_template('create.html')


def log_message(messages):
    app.logger.info('{time_frame} | {message}'.format(time_frame=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), message=messages))

# start the application on port 3111
if __name__ == "__main__":
    app.run(debug=True)
    app.run(host='0.0.0.0', port='3111', debug=True)
