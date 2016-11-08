import MySQLdb
conn= MySQLdb.connect(
        host='192.168.1.240',
        port = 3306,
        user='pt',
        passwd='123',
        db ='test_1',
        )
cur = conn.cursor()
#cur.execute("create table student(id int ,name varchar(20),class varchar(30),age varchar(10))")
cur.execute("insert into student values('2','Tom','3 year 2 class','6')")
cur.execute("insert into student values('2','Tom','3 year 2 class','5')")
cur.execute("insert into student values('2','Tom','3 year 2 class','4')")
cur.execute("delete from student where age='9'")

cur.close()
conn.commit()
conn.close()