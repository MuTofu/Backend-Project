from flask import Flask, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL, MySQLdb

app = Flask(__name__)

# app.config['MYSQL_HOST'] = '192.168.137.77'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'test'
mysql = MySQL(app)


@app.route('/produk/get', methods=['GET'])
def ambil_data():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM produk")
    rv = cur.fetchall()

    data_list = []

    for data in rv:
        conw = {'id':data["idproduk"], 'nama':data["nama"], 'harga':data["harga"], 'deskripsi':data["deskripsi"], 'ukuran':data["ukuran"]}
        data_list.append(conw)
        print(conw)
        conw = {}

    arr = {
        'success' :True,
        'message' : 'berhasil mengambil data',
        'data' : data_list
    }

    return jsonify(arr)


@app.route('/user/login', methods=['GET','POST'])
def login_user():
    request_json = request.get_json()
    email = request_json.get('email')
    password = request_json.get('password')

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM user")
    rv = cur.fetchall()
    status = False

    for data in rv:
        conw = {'email':data["email"], 'password':data["password"]}
        if conw['email'] == email and conw['password'] == password:
            status = True
            break

        conw = {}

    arr = {
        "status" : status,
        "message" : "Berhasil Login :3"
    }

    return jsonify(arr)


@app.route("/user/register", methods=["POST", "PUT"])
def register_user():
    request_json = request.get_json()
    nama_depan = request_json.get('nama_depan')
    nama_belakang = request_json.get('nama_belakang')
    email = request_json.get('email')
    phone = request_json.get('phone')
    alamat = request_json.get('alamat')
    password = request_json.get('password')

    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO user(namadepan, namabelakang, email, phone, alamat, password) VALUES (%s, %s, %s, %s, %s, %s)', (nama_depan, nama_belakang, email, phone, alamat, password))
    mysql.connection.commit()


    array = {
        "messagge" : "berhasil daftar"
    }

    return jsonify(array)






if __name__ == '__main__':
    app.run()
