
from flask import Flask, request, render_template, session, flash, url_for,redirect, logging
from flask_mysqldb import MySQL
import yaml
import uuid
import os


app = Flask(__name__)
mysql = MySQL(app)


db = yaml.load(open('db.yaml'))
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = 'thhytygfg54t342fes'

# Dashboard

@app.route('/')

def dashboard():
    # Create cursor
    cur = mysql.connection.cursor()
    # Get articles
    result = cur.execute("SELECT id,book_name,author,catagory ,book_image FROM books")
    if result > 0:
        books = cur.fetchall()
        return render_template('dashboard.html', books=books)
        # Close connection
        cur.close()    
    else:
        msg = 'No books Found'
    return render_template('dashboard.html', msg=msg)



# Edit book
@app.route('/edit_book/<int:id>', methods=['GET', 'POST'])
#@login_required
def edit_book(id):
    # Create cursor
    cur = mysql.connection.cursor()
    # Get book by id
    
    if request.method == 'POST':
        book_name = request.form['name']
        author = request.form['author']
        
        # Create Cursor
        cur = mysql.connection.cursor()
        
        # Execute
        cur.execute ("UPDATE books SET book_name=%s, author=%s WHERE id=%s",(book_name, author, id))
        # Commit to DB
        mysql.connection.commit()
        #Close connection
        cur.close()
        flash('book Updated', 'success')
        return redirect(url_for('dashboard'))
        
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM books WHERE id = %s", [id])
    book = cur.fetchone()
    return render_template('edit_book.html', book=book)
    cur.close()
    #return render_template('edit_book.html', book=book)


@app.route('/delete_book/<int:id>', methods=['POST'])
#@login_required
def delete_book(id):
    # Create cursor
    cur = mysql.connection.cursor()
    # Execute
    cur.execute("DELETE FROM books WHERE id = %s", [id])
    # Commit to DB
    mysql.connection.commit()
    #Close connection
    cur.close()
    flash('book Deleted')
    return redirect(url_for('dashboard'))


# Add book
@app.route('/addbook/', methods=['GET', 'POST'])

def addbook():    
    if request.method == 'POST': 
            
        book_name = request.form['book_name']
        author = request.form['author']
        catagory=request.form['catagory']
        upload_image=request.files["upload_image"]

        uniq_id_img=str(uuid.uuid1())+os.path.splitext(upload_image.filename)[1]
        upload_image.save(os.path.join("static/images/bookImages",uniq_id_img))

               
        # Create Cursor
        cur = mysql.connection.cursor()
        # Execute
        
        sql="INSERT INTO books(book_name, author,book_image,catagory) VALUES(%s, %s, %s, %s)"
        values=( book_name, author,uniq_id_img,catagory )
        cur.execute(sql,values)
        # Commit to DB
        mysql.connection.commit()
        #Close connection
        cur.close()
        #flash('thank you for your time', 'success')
        return redirect(url_for('dashboard'))
    return render_template('addbook.html')








if __name__ == '__main__':
    
    app.run(debug=True)