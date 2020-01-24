import sys
import inspect

condition = {1:'优秀', 2:'良好', 3:'正常', 4:'较差', 5:'很差', '':'未评分'}
exam = ['四肢肌肉韧带状态', '肩袖肌群及颈椎僵直状态', '腰部劳损状态', '背部肌肉僵直状态']
massage = ['大腿及小腿', '肩部', '腰部', '背部']
test = ['抬腿测试(检查左右腿伸展情况)', '腿部发力测试(检查发力位置牵动腰椎程度)', '左右腿扭转测试(检查大腿两侧韧带状态)']
recover = ['脊椎反弓下压', '臀部收紧腹桥']
lst1 = [exam, massage, test, recover]

def retrieve_name(var):
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]

def menuPresent(recipe_dict, max_num = 3):
    for index in recipe_dict.keys():
        print(index, recipe_dict[index])

    try:
        choice = int(input('请输入你的选择:'))
    except:
        choice = 'error'

    if choice in recipe_dict.keys():
        return (True, choice)
    elif max_num > 1 and choice != 'error':
        print('错误，不合法的输入！', max_num - 1)
        return menuPresent(recipe_dict, max_num - 1)
    elif max_num > 1 and choice == 'error':
        print('错误，不合法的输入！', max_num - 1)
        return menuPresent(recipe_dict, max_num - 1)
    else:
        print('错误输入超过三次，离开系统')
        return (False, choice)

def score_input(condition_dict, i, max_num = 3):
    temp = input('%s score: '%i[1])
    if len(temp) < 1:
        return temp + ';'
    try:
        temp = int(temp)
    except:
        temp = 'error'
    if temp in condition_dict.keys():
        score = str(temp) + ';'
        return score
    elif max_num > 1 and temp != 'error':
        print('错误，不合法的输入！', max_num - 1)
        return score_input(condition_dict, i, max_num - 1)
    elif max_num > 1 and temp == 'error':
        print('错误，不合法的输入！', max_num - 1)
        return score_input(condition_dict, i, max_num - 1)
    else:
        sys.exit(0)

def displayFunc(data, col_name_list):
    for i in data:
        for j in range(len(i)):
            if i[j] is not None:
                print(col_name_list[j],':', i[j])
            if i[j] is not None and col_name_list[j] == 'exam':
                str_exam = i[j].split(';')
                #print('the length is : ',len(str_exam)-1)
                str_exam_score = i[j-1].split(';')
                for t in range(len(str_exam)-1):
                    print(exam[t], '\t\tscore(', str_exam_score[t], '): \t\t', str_exam[t])
            elif i[j] is not None and col_name_list[j] == 'test':
                str_exam = i[j].split(';')
                #print('the length is : ',len(str_exam)-1)
                str_exam_score = i[j-1].split(';')
                for t in range(len(str_exam)-1):
                    print(test[t], '\t\tscore(', str_exam_score[t], '): \t\t', str_exam[t])
            elif i[j] is not None and col_name_list[j] == 'recover':
                str_exam = i[j].split(';')
                #print('the length is : ',len(str_exam)-1)
                str_exam_score = i[j-1].split(';')
                for t in range(len(str_exam)-1):
                    print(recover[t], '\t\tscore(', str_exam_score[t], '): \t\t', str_exam[t])
            elif i[j] is not None and col_name_list[j] == 'massage':
                str_exam = i[j].split(';')
                print('the length is : ',len(str_exam)-1)
                str_exam_score = i[j-1].split(';')
                for t in range(len(str_exam)-1):
                    print(massage[t], '\t\tscore(', str_exam_score[t], '): \t\t', str_exam[t])
        print("")

def displayUtils(cur, displayOption):

    if displayOption == 1:
        cur.execute("PRAGMA table_info(record)")
        col_name_list = [tuple[1] for tuple in cur]
        data = cur.execute('SELECT * FROM record')

        displayFunc(data, col_name_list)
    elif displayOption == 2:
        num = int(input('请输入行数: '))
        cur.execute("PRAGMA table_info(record)")
        col_name_list = [tuple[1] for tuple in cur]
        data = cur.execute('SELECT * FROM record WHERE num = ?',(num,))

        displayFunc(data, col_name_list)
