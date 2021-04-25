from flask import Flask, request, make_response,jsonify
from mysql.connector import errorcode
from configparser import ConfigParser
import mysql.connector
import configparser
import logging
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
config = configparser.ConfigParser()
config.read(f'{dir_path}/flaskapi.cfg')
logging.basicConfig(filename=config['DEFAULT']['log_file'], level=config['DEFAULT']['log_level'])

app = Flask(__name__)



def connect():
    return mysql.connector.connect(
        user=config['DEFAULT']['mysql_user'],
        password=config['DEFAULT']['mysql_password'],
        host=config['DEFAULT']['mysql_host'],
        database=config['DEFAULT']['mysql_database'],
        auth_plugin='mysql_native_password')  



@app.route('/Select', methods=['GET'])
def select():

    try:
        mysqldb = connect()
        cursor =  mysqldb.cursor(buffered=True)
        query = f"SELECT * FROM {config['DEFAULT']['mysql_database']}.{config['DEFAULT']['mysql_table']};"
        cursor.execute(query)
        response = cursor.fetchall()
        mysqldb.close()
    
    except mysql.connector.Error as e:
        if (e.errno == errorcode.ER_ACCESS_DENIED_ERROR):
            logging.error(str(e))
            return make_response(("AUTH ERROR! PLEASE CHECK LOG FILE."),401)
        elif(e.errno == errorcode.ER_BAD_DB_ERROR):
            logging.error(str(e))
            return make_response(("DB NOT EXIST! PLEASE CHECK LOG FILE."),404)
        else:
            logging.error(str(e))
            return make_response(jsonify("SOME ERROR OCCURED! PLEASE CHECK LOG FILE."),400)
    
    return("SUCCESS")


@app.route('/Insert', methods= ['POST'])
def insert(name, lastname, address):
    
    name = request.args.get("name")
    lastname = request.args.get("lastname")
    address = request.args.get("address")

    try:
        mysqldb = connect()
        cursor =  mysqldb.cursor(buffered=True)
        query = f'''INSERT INTO {config['DEFAULT']['mysql_database']}.{config['DEFAULT']['mysql_table']}(name, lastname, address) VALUES ('{name}','{lastname}','{address}'); '''
        cursor.execute(query)
        mysqldb.commit()
        mysqldb.close()
    
    except mysql.connector.Error as e:
        if(e.errno == errorcode.ER_ACCESS_DENIED_ERROR):
            logging.error(str(e))
            return make_response(("AUTH ERROR! PLEASE CHECK LOG FILE."),401)
            
        elif(e.errno == errorcode.ER_BAD_DB_ERROR):
            logging.error(str(e))
            return make_response(("DB NOT EXIST! PLEASE CHECK LOG FILE."),404)
            
        else:
            print(e)
            logging.error(str(e))
            return make_response(("SOME ERROR OCCURED! PLEASE CHECK LOG FILE."),400)
            
    return("SUCCESS")


@app.route('/Delete', methods= ['DELETE'])
def delete(num):

    num = request.args.get("num")
    try:
        mysqldb = connect()
        cursor =  mysqldb.cursor(buffered=True)
        query = f'''DELETE FROM {config['DEFAULT']['mysql_database']}.{config['DEFAULT']['mysql_table']}(name, lastname, address) WHERE id = {num}; '''
        cursor.execute(query)
        mysqldb.commit()
        mysqldb.close()

    except mysql.connector.Error as e:
        if(e.errno == errorcode.ER_ACCESS_DENIED_ERROR):
            logging.error(str(e))
            return make_response(("AUTH ERROR! PLEASE CHECK LOG FILE."),401)
            
        elif(e.errno == errorcode.ER_BAD_DB_ERROR):
            logging.error(str(e))
            return make_response(("DB NOT EXIST! PLEASE CHECK LOG FILE."),404)
            
        else:
            print(e)
            logging.error(str(e))
            return make_response(("SOME ERROR OCCURED! PLEASE CHECK LOG FILE."),400)
            


def main():
    response_insert = insert(Mirel, Dik, Adana)
    response_select = select()
    response_delete = delete(1)
    return (response_insert)


if __name__=="__main__":
    app.run(host=config['APISERVER']['api_host'], port=config['APISERVER']['api_port'])