import sqlite3 
import sqlite3 as sq

def table():
    connection = sq.connect('databases/IPdb.db')
    cursor = connection.cursor()
    devices_tb = '''
    CREATE TABLE IF NOT EXISTS devices(
    divece_id INTEGER PRIMARY KEY AUTOINCREMENT,
    divece_nm TEXT NOT NULL,
    ip_address TEXT NOT NULL UNIQUE
    ) '''
    cursor.execute(devices_tb)
    connection.commit()
    cursor.close()
    connection.close()
table()

def insertBD(divece_nm, ip_address):
    connection = sq.connect('databases/IPdb.db')
    cursor = connection.cursor()
    cursor.execute('''
    INSERT INTO DEVICES (divece_nm, ip_address) VALUES(?, ?);
''', (divece_nm, ip_address))
    print('Были добавлены - ', divece_nm,',' ,ip_address)
    connection.commit()
    cursor.close()
    connection.close()

def getDevices():
    conn = sqlite3.connect('databases/IPdb.db')
    cursor = conn.cursor()
    cursor.execute("SELECT divece_nm, ip_address FROM DEVICES ")  
    devices = cursor.fetchall()
    conn.close()
    device_list = [{'name': device[0], 'ip': device[1]} for device in devices]
    return device_list

def deleteRecord(id):
    conn = sqlite3.connect('databases/IPdb.db')  #
    cursor = conn.cursor()
    cursor.execute("DELETE from devices where ip_address = ?", (id, ))
    conn.commit()
    cursor.close()

print(getDevices)