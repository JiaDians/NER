import json
from mysql import MySql
import sys

def saveData(start_id):
    mysql = MySql(host="localhost", port=3306, user="root", pwd="#Asdfg881110", db="ner")
    lines = []
    with open(r'../C.txt', 'r') as f:
        lines = f.readlines()
        
    for i in range(len(lines)):
        result = json.loads(lines[i].replace("\'", "\""))
        sql = "INSERT INTO data_table(d_id, d_source, d_type, d_date, d_text, d_tag) VALUES (" + str(start_id + i) + ",'" + result['source'] + "','" + result['type'] + "','" + result['date'] + "','" + result['text'] + "','" + str(result['tag']).replace('\'','`') +"');"
        mysql.ExecNonQuery(sql)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('no argument')
        sys.exit()
    saveData(int(sys.argv[1]))
    