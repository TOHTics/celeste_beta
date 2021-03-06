import psycopg2
import thread
import time

class CelesteDB:
    def __init__(self, dbName_, userDb_, tableName_):
        self.dbName=dbName_
        self.userDb=userDb_
        self.tableName=tableName_
    
    def insertXml(self, xmlData):
        conn=psycopg2.connect(dbname=self.dbName, user=self.userDb)
        cur = conn.cursor()
        cur.execute("INSERT INTO "+self.tableName+" VALUES(%s);", [xmlData])
        conn.commit()#make the changes to the db persistent
        conn.close()
        cur.close()

    def getTopElement(self):
        conn=psycopg2.connect(dbname=self.dbName, user=self.userDb)
        cur = conn.cursor()
        cur.execute("SELECT * FROM "+self.tableName+" LIMIT 1;")
        #cur.execute("SELECT * FROM "+self.tableName+";")
        results=cur.fetchall()
        conn.close()
        cur.close()
        return results

    def getAllElements(self):
        conn=psycopg2.connect(dbname=self.dbName, user=self.userDb)
        cur = conn.cursor()
        #cur.execute("SELECT * FROM "+self.tableName+"LIMIT 1;")
        cur.execute("SELECT * FROM "+self.tableName+";")
        results=cur.fetchall()
        conn.close()
        cur.close()
        return results

    def deleteTopElement(self):
        conn=psycopg2.connect(dbname=self.dbName, user=self.userDb)
        cur = conn.cursor()
        cur.execute("DELETE FROM "+self.tableName+" WHERE xml=any(array(SELECT xml FROM "+self.tableName+" LIMIT 1));")
        conn.commit()
        conn.close()
        cur.close()

    def getNElements(self):
        conn=psycopg2.connect(dbname=self.dbName, user=self.userDb)
        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM "+self.tableName+";")
        results=cur.fetchall()
        conn.close()
        cur.close()
        return results[0][0]

    def threadTest(self, threadName, delay):
        count=0
        while count<5:
            time.sleep(delay)
            count+=1
            print "%s: %s"%(threadName, time.ctime(time.time()))



