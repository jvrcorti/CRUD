from flask import Flask, render_template, request
from flaskext.mysql import MySQL
import os

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'templates')
app = Flask(__name__) 

# Database connection
mysql = MySQL()
app.config['MYSQL_DATABASE_HOTS']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_BD']='sistemas'
#app.config['MYSQL_DATABASE_']
mysql.init_app(app)

# Path the application 
@app.route('/')
def index():
    return render_template('empleados/index.html')

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        foto = request.form['foto']
        sql = "INSERT INTO `sistemas`.`empleados` (`id`, `Nombre`, `Email`, `Foto`) VALUES (%s, %s, %s, %s)', (NULL, name, email, foto)"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        print(name)
        print(email)
        print(foto)
        return 'recivided'

if __name__ == '__main__':
    app.run(port=5000, debug=True)