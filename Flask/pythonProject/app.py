from flask import Flask, render_template, \
    request,redirect,url_for, jsonify

from datetime import datetime
from flask_mysqldb import MySQL, MySQLdb
import json
# import pymysql.cursors, os

app = Flask(__name__)
# conn = cursor = None



app.config['MYSQL_HOST'] = 'us-cdbr-east-06.cleardb.net'
app.config['MYSQL_USER'] = 'b0fe5498264fd4'
app.config['MYSQL_PASSWORD'] = '288dea7b'
app.config['MYSQL_DB'] = 'heroku_b0414d4e623738d'
mysql = MySQL(app)


@app.route('/')
def hello_world():

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM mahasiswa")
    rv = cur.fetchall()
    user = []
    conw = {}

    for data in rv:
        conw = {'id': data['id'], 'username': data['username'], 'email': data['email'], 'password': data['password']}

        user.append(conw)
        conw = {}

    array = {
        'success': True,
        'message': "berhasil ambil data",
        'data': user}





    return jsonify(array)

@app.route('/aktivasi', methods=["POST"])
def login():
    request_json  = request.get_json()
    email = request_json.get("email")
    password = request_json.get("password")

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM  mahasiswa WHERE email = %s AND password = %s',(email,password,))
    account = cur.fetchone()

    if account:

        array = {
            'success': True,
            'message': "berhasil Login"}

        return jsonify(array)

    else:

        array = {
            'success': False,
            'message': "Salah password / email"}

    return jsonify(array)


@app.route('/list', methods=['GET'])
def task():

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM task")
    rv = cur.fetchall()
    user = []
    conw = {}

    for data in rv:
        conw = {'id': data['id'], 'id_task': data['id_task'],'namatugas': data['namatugas'], 'deskripsi': data['deskripi'], 'deadline': str(data['deadline']), 'alarm': str(data['alarm']) }

        user.append(conw)
        conw = {}

    array = {
        'success': True,
        'message': "berhasil ambil data",
        'data': user}

    return jsonify(array)


@app.route('/tasknew', methods=['POST'])
def newTask():
    request_json  = request.get_json()
    namaTugas = request_json.get("namatugas")
    deskripsi = request_json.get("deskripsi")



    dateJSOn = request_json.get("deadline")
    # formatDate = "%Y-%m-%d"
    # date_obj = datetime.strptime(dateJSOn, formatDate)
    # date = date_obj.date()

    alarmJson = request_json.get("alarm")
    # formatTime = "%H:%M:%S"
    # date_obj = datetime.strptime(alarmJson, formatTime)
    # time = date_obj.time()



    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO task(namatugas, deskripi, deadline, alarm) VALUES (%s, %s, %s, %s)', (namaTugas, deskripsi, dateJSOn, alarmJson))
    mysql.connection.commit()

    array = {
        'success': True,
        'message': "berhasil Upload"}

    return jsonify(array)


@app.route("/register", methods=['POST'])
def regster():
    request_json = request.get_json()
    username = request_json.get("username")
    email = request_json.get("email")
    password = request_json.get("password")


    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO mahasiswa(username, email, password) VALUES (%s, %s, %s)',(username, email, password))
    mysql.connection.commit()

    array = {
        'success': True,
        'message': "berhasil register"}

    return jsonify(array)


@app.route("/delete", methods = ["POST"])
def hapus():
    request_json = request.get_json()
    namatugas = request_json.get("namatugas")
    print(namatugas)

    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM task WHERE namatugas = %s ', (namatugas,))
    mysql.connection.commit()

    array = {
        'success': True,
        'message': "berhasil Hapus"}

    return jsonify(array)




if __name__ == '__main__':
    app.run(debug=True)
