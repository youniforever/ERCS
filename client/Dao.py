import sqlite3 as lite


dbPath = '/usr/local/ERCS/client/SCHEMA.db'


def userDuplicateCheck(loginInfo):
    conn = lite.connect(dbPath)
    cur = conn.cursor()

    query = "SELECT COUNT(user_id) FROM user WHERE user_id='" + loginInfo['userId'] + "' "
    cur.execute(query)
    row = cur.fetchone()
    cur.close()

    return row

def userLoginCheck(loginInfo):
    conn = lite.connect(dbPath)
    cur = conn.cursor()

    cur.execute("SELECT user_id, name FROM user WHERE user_id='" + loginInfo['userId'] + "' AND password='" + loginInfo['userPw'] + "' ")
    row = cur.fetchone()
    cur.close()

    return row

def insUser(data):
    conn = lite.connect(dbPath)
    cur = conn.cursor()

    sql = "INSERT INTO `user` " \
          "(`user_id`, `password`, `name`) " \
          "VALUES " \
          "('" + data['userId'] + "', '" + data['userPw'] + "', '" + data['userName'] + "')"
    cur.execute(sql)
    conn.commit()
    cur.close()

def getDevice(cond):
    conn = lite.connect(dbPath)
    cur = conn.cursor()

    sql = "SELECT " \
          "`uid`, " \
          "`user_id`, " \
          "`device_ip`, " \
          "`device_port`, " \
          "`device_name`, " \
          "`pin_no`, " \
          "`pin_status` " \
          "FROM device " \
          "WHERE " \
          "`user_id` = '" + cond['userId'] + "' "

    if ( cond.has_key('uId') and cond['uId'] != "" ):
        sql += " AND `uid` = '" + cond['uId'] + "' "

    cur.execute(sql)
    row = cur.fetchall()
    cur.close()

    return row

def insDevice(data):
    conn = lite.connect(dbPath)
    cur = conn.cursor()

    sql = "INSERT INTO `device` " \
          "(uid, user_id, device_ip, device_port, device_name, pin_no) " \
          "VALUES " \
          "('" + data['uId'] + "', '" + data['userId'] + "', '" + data['deviceIp'] + "', '" + data['devicePort'] + "', " \
          "'" + data['deviceName'] + "', '" + data['pinNo'] + "')"

    cur.execute(sql)
    conn.commit()
    cur.close()

def delDevice(data):
    conn = lite.connect(dbPath)
    cur = conn.cursor()

    sql = "DELETE FROM `device` WHERE `uid` IN ('" + "','".join(data['uId']) + "')"
    cur.execute(sql)
    conn.commit()
    cur.close()

def udtPinStatus(pinInfo):
    conn = lite.connect(dbPath)
    cur = conn.cursor()

    sql = "UPDATE `device` SET `pin_status` = '" + pinInfo['pinStatus'] + "' WHERE `pin_no` = '" + pinInfo['pinId'] + "' "
    cur.execute(sql)
    conn.commit()
    cur.close()
