from datetime import datetime
import mysql.connector

db = mysql.connector.connect(host='localhost',
                        user='campkt',
                        passwd='Jrnz,hm03',
                        db="Campaign_KT")

cursor = db.cursor()     # get the cursor

# cursor.execute(f"INSERT INTO Campaign_KT.User VALUES('Azam', '123qweghost', 'True', '{data}');")
# db.commit

# cursor.execute("INSERT INTO Campaign_KT.Settings VALUES ('10.165.0.14', 'asterisk1.telecom.kz', 30);")
# db.commit()


# cursor.execute("INSERT INTO Campaign_KT.Settings (SIP_Server, SIP_Trunk, Time_Out) VALUES ('10.165.0.14', 'asterisk1.telecom.kz', '20');")
# db.commit()

# cursor.execute(f"UPDATE Campaign_KT.OPERATION SET Status = %s;" %(1) )
# db.commit()

# cursor.execute("UPDATE Campaign_KT.Settings SET SIP_Server = %s, SIP_Trunk = %s, TIME_Out = %s;", ('10.165.0.14', 'asterisk1.telecom.kz', '10'))
# db.commit()

# cursor.execute("ALTER TABLE Settings ADD Sip_Ip varchar(20);")
# db.commit()


cursor.execute("SELECT * FROM Settings;")

records = cursor.fetchall()

# sym = 0

# for i in records:
#     if i[0] != 0:
#         sym += int(i[0])
#         print(i[0]) 

print(records)

# if records is None:
    # print(records)
# else:
    # print("hello")
# 
# import socket
# print(socket.gethostbyname(socket.gethostname()))