from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_mysqldb import MySQL
from datetime import datetime
import os

#template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
#template_dir = os.path.join(template_dir, 'templates')
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

#Generado secret_key para introducir mensajes en web page
app.secret_key = 'mysecretkey'
# Creo el acceso a la carpeta del sistema 
carpeta = os.path.join("uploads")
app.config['CARPETA']=carpeta

# Path the application 
@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    # Los datos son manipulados en la web page
    cursor.execute('SELECT * FROM empleados')
    data = cursor.fetchall()
    print(data)
    return render_template('empleados/index.html', employees = data)

@app.route('/uploads/<foto>')
def uploads(foto):
    return send_from_directory(carpeta, foto)

@app.route('/add_employee', methods=['POST', 'GET'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        foto = request.files['foto']
        # Modificacion del nombre archivo foto
        now = datetime.now()
        tiempo = now.strftime("%Y%H%M%S")
        if foto.filename != '':
            nuevo_nombre_foto = tiempo + foto.filename
            foto.save("uploads/" + nuevo_nombre_foto)
        cursor = mysql.connection.cursor()
        cursor.execute(' INSERT INTO empleados VALUES(NULL, %s, %s, %s)',(name, email, nuevo_nombre_foto))
        mysql.connection.commit()
        cursor.close()
        print(name, email, nuevo_nombre_foto)
        flash('El empleado fue registrado correctamente')
        return redirect(url_for('index'))


@app.route('/edit/<id>')
def get_employee(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM empleados WHERE id = {0}'.format(id))
    data = cursor.fetchall()
    print(data[0])
    return render_template('empleados/edit-empleados.html', employees = data[0])

@app.route('/edit_employee/<id>', methods = ['POST'])
def edit_employee(id):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        foto = request.files['foto']
        cursor = mysql.connection.cursor()
        now = datetime.now()
        tiempo = now.strftime("%Y%H%M%S")
        if foto.filename != '':
            nuevo_nombre_foto = tiempo + foto.filename
            foto.save("uploads/" + nuevo_nombre_foto)
            cursor.execute('SELECT Foto FROM empleados WHERE id = {0}'.format(id))
            file = cursor.fetchall()
            print(file)
            os.remove(os.path.join('uploads', file[0][0]))
            cursor.execute('UPDATE empleados SET Nombre = %s, Email = %s, Foto = %s WHERE id = %s',(name, email, nuevo_nombre_foto, id))
            mysql.connection.commit()
            flash('El empleado fue actualizado correctamente')
            return redirect(url_for('index'))

@app.route('/delete/<string:id>')
def delete_employee(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT Foto FROM empleados WHERE id = {0}'.format(id))
    file = cursor.fetchall()
    print(file)
    os.remove(os.path.join('uploads', file[0][0]))
    cursor.execute(' DELETE FROM empleados WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('El empleado fue eliminado correctamente')
    return redirect(url_for('index'))

# Iniciar App
if __name__ == '__main__':
    app.run(port=5000, debug=True)