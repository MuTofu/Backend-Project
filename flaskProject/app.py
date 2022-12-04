from flask import Flask, render_template, \
    request,redirect,url_for, jsonify

import json
import pymysql.cursors, os



app = Flask(__name__)
conn = cursor = None

def dbConect():
    global conn, cursor
    conn = pymysql.connect(db="api", user="root", passwd="", host="localhost" )
    cursor = conn.cursor()

def dbClose():
    global conn,cursor
    cursor.close()
    conn.close()


@app.route('/')
def hello_world():  # put application's code here

    dbConect()

    container = []
    sql = "SELECT * FROM mahasiswa"
    cursor.execute(sql)
    result = cursor.fetchall()

    for data in result:
        container.append(data)
    dbClose()


    json_list = []
    for row in result:
        data_dict = {}
        for i in range(len(container)):
            data_dict[str(container[i])] = row[i]

        json_list.append(data_dict)

    return jsonify({"space": json_list})

# @app.route("/tambah", methods=['GET', "POST"])
# def tambah():
#     if request.method == "POST":
#         nama = request.form["nama"]
#         email = request.form["email"]
#         password = request.form["password"]
#
#         dbConect()
#         sql = "INSERT INTO mahasiswa (username, email, password) VALUES (%s, %s, %s)"
#         val = (nama, email, password)
#         conn.commit()
#         dbClose()
#         return redirect(url_for("tambah"))
#     else:
#         return render_template("tambah.html")




if __name__ == '__main__':
    app.run(debug=True)
