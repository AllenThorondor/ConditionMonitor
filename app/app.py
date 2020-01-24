import time
import sqlite3
from utils.utils import retrieve_name, menuPresent, score_input, displayUtils

condition = {1:'优秀', 2:'良好', 3:'正常', 4:'较差', 5:'很差', '':'未评分'}
exam = ['四肢肌肉韧带状态', '肩袖肌群及颈椎僵直状态', '腰部劳损状态', '背部肌肉僵直状态']
massage = ['大腿及小腿', '肩部', '腰部', '背部']
test = ['抬腿测试(检查左右腿伸展情况)', '腿部发力测试(检查发力位置牵动腰椎程度)', '左右腿扭转测试(检查大腿两侧韧带状态)']
recover = ['脊椎反弓下压', '臀部收紧腹桥']
lst1 = [exam, massage, test, recover]

dbname = "test1.db"
conn = sqlite3.connect(dbname)
cur = conn.cursor()

def addItem():
    print("\n--------------------添加数据------------------")
    #数据对应关系
    correlation = {1:'exam', 2:'massage', 3:'test', 4:'recover', 5:'return'}

    modify_dict = {1:"检查", 2:"按摩", 3:"测试",4:"康复", 5:"返回"}
    result = menuPresent(modify_dict)

    if result[0]:

        choice =  correlation[int(result[1])]
        if choice =='return':
            return main()
        else:
            current = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

            if cur.execute('SELECT num FROM record ORDER BY num DESC LIMIT 1').fetchone() is None:
                num = 1
                print('num is none')
            else:
                num = int(cur.execute('SELECT num FROM record ORDER BY num DESC LIMIT 1').fetchone()[0])
                print(type(num))
                num += 1

            print("this is num:", num)
            cur.execute('INSERT OR IGNORE INTO record(num, date) VALUES(?, ?)',(int(num), current))
            cur.execute('SELECT * FROM items WHERE class = ?',(choice,))

            print('下面是表内的项目：')
            temp_list = []
            for i in cur:
                temp_list.append(i)
                print(i)
            #填写数据
            score = ''
            content = ''
            for i in temp_list:
                print(i)
                print('请按照格式填写【评分，其他说明】')
                print('1:优秀， 2:良好， 3:正常， 4:较差， 5:很差')

                score += score_input(condition, i)
                content += input('%s discription: '%i[1]) + ';'

                if i[0] == 'exam':
                    update_item = 'UPDATE record SET exam = ?, exam_score = ? WHERE num = ? '
                elif i[0] == 'massage':
                    update_item = 'UPDATE record SET massage = ?, massage_score = ? WHERE num = ?'
                elif i[0] == 'test':
                    update_item = 'UPDATE record SET test = ?, test_score = ? WHERE num = ?'
                elif i[0] == 'recover':
                    update_item = 'UPDATE record SET recover = ?, recover_score = ? WHERE num = ?'
                else:
                    print('something went wrong')


                cur.execute(update_item,(content, score, int(num)))
                conn.commit()
            print(len(score))



def deleteItem():
    #主界面
    print("\n--------------------删除数据------------------")
    delete_dict = {1:"删除某些数据", 2:"删除某天数据", 3:"删除所有数据", 4:"返回"}
    result = menuPresent(delete_dict)

    if result[0]:
    #提示语言
        choice = result[1]
        if choice == 1:
            num = input('请输入选择的行数')
            cur.execute('DELETE FROM record WHERE num = ?', (num,))
            conn.commit()
        elif choice == 2:
            num = input('请输入选择的行数')
            cur.execute('DELETE FROM record WHERE num = ?', (int(num),))
            conn.commit()
        elif choice == 3:
            cur.execute('DROP TABLE IF EXISTS record ')
            cur.execute('''CREATE TABLE IF NOT EXISTS record(num PRIMARY KEY, date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                            content TEXT, exam_score INTEGER, exam TEXT, massage_score INTEGER, massage TEXT,
                            test_score INTEGER, test TEXT, recover_score INTEGER, recover TEXT, other TEXT)''')
        elif choice == 4:
            return main()
def displayItem():
    print("\n--------------------展示数据------------------")
    display_dict = {1:'展示全部', 2:'选择行数', 3:'选择日期', 4:'返回'}
    result = menuPresent(display_dict)

    if result[0]:
        choice = result[1]
    if choice == 1:
        return displayUtils(cur, 1)
    elif choice == 2:
        return displayUtils(cur, 2)
    elif choice == 3:
        pass
    elif choice == 4:
        return main()
    else:
        pass

def modifyItem():
    print("\n--------------------修改数据------------------")
    #数据对应关系
    correlation = {1:'exam', 2:'massage', 3:'test', 4:'recover', 5:'return'}

    modify_dict = {1:"检查", 2:"按摩", 3:"测试",4:"康复", 5:"返回"}
    result = menuPresent(modify_dict)

    if result[0]:

        choice =  correlation[int(result[1])]
        current = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        if choice == 'return':
            return main()
        else:
            num = int(input('请输入需要修改的行数: '))
            print("this is num:", num)
            cur.execute('INSERT OR IGNORE INTO record(num, date) VALUES(?, ?)',(num, current))
            cur.execute('SELECT * FROM items WHERE class = ?',(choice,))

            print('下面是表内的项目：')

            temp_list = []
            for i in cur:
                temp_list.append(i)
                print(i)
            print('')
            #填写数据
            score = ''
            content = ''
            for i in temp_list:
                print(i)
                print('请按照格式填写【评分，其他说明】')
                print('1:优秀， 2:良好， 3:正常， 4:较差， 5:很差')

                score += score_input(condition, i)
                content += input('%s discription: '%i[1]) + ';'

                if i[0] == 'exam':
                    update_item = 'UPDATE record SET exam = ?, exam_score = ? WHERE num = ? '
                elif i[0] == 'massage':
                    update_item = 'UPDATE record SET massage = ?, massage_score = ? WHERE num = ?'
                elif i[0] == 'test':
                    update_item = 'UPDATE record SET test = ?, test_score = ? WHERE num = ?'
                elif i[0] == 'recover':
                    update_item = 'UPDATE record SET recover = ?, recover_score = ? WHERE num = ?'
                else:
                    print('something went wrong')


                cur.execute(update_item,(content, score, int(num)))
                conn.commit()
            print(len(score))

def main():
    import sys
    print("\n--------------------康复记录软件------------------")

    main_dict = {1:"添加数据", 2:"修改数据", 3:"展示数据",4:"删除数据", 5:"退出"}
    result = menuPresent(main_dict)
    while True:
        if result[0]:
            if result[1] == 1:
                addItem()
            elif result[1] == 2:
                modifyItem()
            elif result[1] == 3:
                displayItem()
            elif result[1] == 4:
                deleteItem()
            elif result[1] == 5:
                print("离开系统")
                try:
                    sys.exit(0)
                finally:
                    cur.close()
                    conn.close()
        else:
            print('出现错误，离开系统')
            sys.exit(0)
