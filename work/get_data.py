from mysql import MySql

def main():
    mysql = MySql(host="localhost", port=3306, user="root", pwd="#Asdfg881110", db="ner")
    res_tuple = mysql.exec_query("SELECT d_text,d_tag FROM data_table;")
    data_list = []
    for inst in res_tuple:
        inst = list(inst)
        inst[1] = eval(inst[1].replace("`","'"))
        data_list.append(inst)
    # print(training_list)
    with open('./data/data.txt', 'w', encoding='UTF-8') as f:
        f.write(str(data_list))
    return data_list
        
if __name__ == '__main__':
    data_list = main()