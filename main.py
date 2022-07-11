from flask import Flask, render_template, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'rest_python'
mysql = MySQL(app)

@app.route('/api/customers/<int:id>')
def getCustomer(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM CLIENTES WHERE id = %s", str(id))
    data = cur.fetchall()
    content = {}
    for row in data:
       content= {
             "id": row[0],
             "name": row[1],
             "surname": row[2],
             "address": row[3],
             "tel": row[4],
             "email": row[5]
             }
    return jsonify(content)

@app.route('/api/customers')
def getAllCustomers():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM CLIENTES")
    data = cur.fetchall()
    result = []
    for row in data:
        content = {"id": row[0], "name": row[1], "surname": row[2], "address": row[3], "tel": row[4], "email": row[5]}
        result.append(content)
    return jsonify(result)

@app.route('/api/customers', methods = ['POST'])
def saveCustomer():
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO `clientes` ( `id`, `name`, `surname`, `address`, `tel`, `email`) VALUES ( NULL, %s, %s, %s, %s, %s);",
                (request.json['name'], request.json['surname'], request.json['address'], request.json['tel'], request.json['email']))
    mysql.connection.commit()
    return "Cliente Guardado"

@app.route('/api/customers', methods = ['PUT'])
def updateCustomer():
    cur = mysql.connection.cursor()
    cur.execute("UPDATE rest_python.clientes SET name=%s, surname=%s, address=%s, tel=%s, email=%s WHERE id=%s;",
                (request.json['name'], request.json['surname'], request.json['address'], request.json['tel'],
                 request.json['email'], request.json['id']))
    mysql.connection.commit()
    return "Cliente Actualizado"

@app.route('/api/customers/<int:id>', methods = ['DELETE'])
def removeCustomer(id):
    cur = mysql.connection.cursor()
    cur.execute(" DELETE FROM rest_python.clientes WHERE id = %s;", str(id))
    mysql.connection.commit()

    return "Cliente Eliminado"




@app.route('/')
def index():
    datos = "Lucas"
    return render_template('index.html', atr=datos)

if __name__ == '__main__':
    app.run(None,3000, True)