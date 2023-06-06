from flask import Flask, render_template,\
    request, redirect, url_for, jsonify

from flask_mysqldb import MySQL, MySQLdb
import json

app = Flask(__name__)

app.config['MYSQL_HOST'] = '192.168.137.77'
app.config['MYSQL_USER'] = 'cahya'
app.config['MYSQL_PASSWORD'] = '@Cahya123'
app.config['MYSQL_DB'] = 'to_do'
mysql = MySQL(app)


@app.route('/get', methods=['GET'])
def ambil_data():

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM todo")
    rv = cur.fetchall()

    data_list = []
    conw = {}

    for data in rv:
        conw = {'id': data['id'], 'judul':data['judul'], 'deskripsi': data['deskripsi']}

        data_list.append(conw)
        conw = {}

    array = {
        'success': True,
        'message': 'Berhasil ambil data',
        'data': data_list
    }

    return jsonify(data_list)



@app.route('/upload', methods=['POST'])
def up_data():
    request_json = request.get_json()
    id = request.get_json('id')
    judul = request_json.get('judul')
    deskripsi = request_json.get('deskripsi')

    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO todo(judul, deskripsi) VALUES (%s, %s)',(judul, deskripsi))
    mysql.connection.commit()

    array = {
        'succes' : True,
        'message' : "Berhasil upload"
    }

    return jsonify(array)



@app.route('/update', methods=['POST','PUT'])
def update_data():
    request_json = request.get_json()
    id = request.get_json('id')
    judul = request.get_json('judul')
    deskripsi = request.get_json('deskripsi')

    data_update = [judul['judul'], deskripsi['deskripsi'], str(id['id'])]

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM todo WHERE id =" + str(id['id']))
    cur.execute('UPDATE todo SET judul= %s, deskripsi= %s WHERE id = ' + str(id['id']), (judul['judul'], deskripsi['deskripsi'] ) )
    mysql.connection.commit()

    array = {
        'succes' : True,
        'message' : "Berhasil Update data"
    }

    return jsonify(array)


@app.route('/delete', methods=['POST','DELETE'])
def delete_data():
    request_json = request.get_json()
    id = request.get_json('id')
    print(str(id['id']))

    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM todo WHERE id = ' + str(id['id']))
    mysql.connection.commit()

    array = {
        'succes' : True,
        'message' : "Berhasil hapus"
    }

    return jsonify(array)






if __name__ == '__main__':
    app.run(debug=True)
