import pymysql

class MySql:
    def __init__(self, host, port, user, pwd, db):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.db = db

    def _get_connect(self):
        if not self.db:
            raise(NameError,"沒有設置資料庫資訊")
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.pwd, database=self.db, charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise(NameError,"連接資料庫失敗")
        else:
            return cur

    def exec_query(self, sql):
        cur = self._get_connect()
        cur.execute(sql)
        resList = cur.fetchall()
        self.conn.close()
        return resList

    def ExecNonQuery(self,sql):
        cur = self._get_connect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()

def main():
    mysql = MySql(host="localhost", port=3306, user="root", pwd="#Asdfg881110", db="ner")
    resList = mysql.exec_query("SELECT d_text,d_tag FROM data_table where d_id >= 1 AND d_id <= 5;")
    for inst in resList:
        print(inst)
        
if __name__ == '__main__':
    main()