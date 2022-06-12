from mysql import MySql

def main():
    mysql = MySql(host="localhost", port=3306, user="root", pwd="#Asdfg881110", db="ner")
    res_tuple = mysql.exec_query("SELECT d_text,d_tag FROM data_table;")
    training_list = []
    for inst in res_tuple:
        inst = list(inst)
        inst[1] = eval(inst[1].replace("`","'"))
        training_list.append(inst)
    # print(training_list)
    with open('./training/training_data.txt', 'w', encoding='UTF-8') as f:
        f.write(str(training_list))
        
if __name__ == '__main__':
    main()