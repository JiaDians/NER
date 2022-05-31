import json
import pymysql
import sys

def saveData(start_id):
    #資料庫連線
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='#Asdfg881110', db='ner', charset='utf8mb4')
    cursor = db.cursor()
    
    lines = []
    with open(r'C.txt', 'r') as f:
        lines = f.readlines()
        
    for i in range(len(lines)):
        # print('article:', str(i+1))
        result = json.loads(lines[i].replace("\'", "\""))
        print(i,result['text'])
        sql = "INSERT INTO data_table(d_id, d_source, d_type, d_date, d_text, d_tag) VALUES (" + str(start_id + i) + ",'" + result['source'] + "','" + result['type'] + "','" + result['date'] + "','" + result['text'] + "','" + str(result['tag']).replace('\'','`') +"');"
        try:
          cursor.execute(sql)
          #提交修改
          db.commit()
        except pymysql.Error as e:
            #發生錯誤時停止執行SQL
            db.rollback()
            print('[error]')
            print(e.args[0], e.args[1])
    print('ok')
    db.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('no argument')
        sys.exit()
        
    saveData(int(sys.argv[1]))
    