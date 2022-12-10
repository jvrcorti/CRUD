from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import os

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'templates')
app = Flask(__name__) 

# Database connection
mysql = MySQL()
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='sistemas'
#app.config['MYSQL_DATABASE_']
#mysql.init_app(app)
mysql = MySQL(app)

# Path the application 
@app.route('/')
def index():
    return render_template('empleados/index.html')

@app.route('/add_contact', methods=['POST', 'GET'])
def add_contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        foto = request.form['foto']
        cursor = mysql.connection.cursor()
        cursor.execute(' INSERT INTO empleados VALUES(NULL, %s, %s, %s)',(name, email, foto))
        mysql.connection.commit()
        cursor.close()
        print(name, email, foto)
        return render_template('empleados/index.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)