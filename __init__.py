import sqlite3
from utils.utils import retrieve_name
condition = {1:'优秀', 2:'良好', 3:'正常', 4:'较差', 5:'很差', '':'未评分'}
exam = ['四肢肌肉韧带状态', '肩袖肌群及颈椎僵直状态', '腰部劳损状态', '背部肌肉僵直状态']
massage = ['大腿及小腿', '肩部', '腰部', '背部']
test = ['抬腿测试(检查左右腿伸展情况)', '腿部发力测试(检查发力位置牵动腰椎程度)', '左右腿扭转测试(检查大腿两侧韧带状态)']
recover = ['脊椎反弓下压', '臀部收紧腹桥']
lst1 = [exam, massage, test, recover]

dbname = input('请输入数据库名称: ')
if dbname.endswith('.db'):
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
else:
    conn = sqlite3.connect(dbname+'.db')
    cur = conn.cursor()
#系统初始化（请慎重使用该功能）
#创建表格
add_table1 = '''CREATE TABLE IF NOT EXISTS record(num PRIMARY KEY, date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
content TEXT, exam_score INTEGER, exam TEXT, massage_score INTEGER, massage TEXT,
test_score INTEGER, test TEXT, recover_score INTEGER, recover TEXT, other TEXT)'''
add_table2 = '''CREATE TABLE IF NOT EXISTS items(class TEXT, item TEXT)'''

cur.execute(add_table2)
cur.execute(add_table1)
print('数据表创建完毕')

#初始化items表格
for i in lst1:
    for j in i:
        cur.execute('INSERT OR IGNORE INTO items (class, item) VALUES(?, ?)',(retrieve_name(i)[0], j))
conn.commit()
print('数据表初始化完毕')
cur.close()
conn.close()
