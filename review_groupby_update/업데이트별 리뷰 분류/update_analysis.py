import numpy as np
import pandas as pd
import cx_Oracle

def txtTOlist(filename):
    with open(filename, encoding='utf-8') as file:
        mylist = [item.split(',') for item in file.readlines()]
    return mylist[0]

def csvTOframe(filename):
    mytoken = pd.read_csv(filename, encoding='utf-8', index_col=0)
    mytoken = mytoken.set_index('update_id')
    return mytoken

def selectKey(token, updateID, droplist, idx):
    keyframe = token.loc[[int(updateID[idx]),int(updateID[idx+1])],:]

    newframe = keyframe.loc[[int(updateID[idx])]]
    nextframe = keyframe.loc[[int(updateID[idx+1])]]

    # 업데이트 날짜 수정
    startyear = newframe.loc[int(updateID[idx]), 'year']
    startmonth = newframe.loc[int(updateID[idx]), 'month']
    startday = newframe.loc[int(updateID[idx]), 'day']

    endyear = nextframe.loc[int(updateID[idx+1]), 'year']
    endmonth = nextframe.loc[int(updateID[idx+1]), 'month']
    endday = nextframe.loc[int(updateID[idx+1]), 'day']

    # 업데이트 키워드 분석
    # 업데이트 키워드 리스트 변경
    mylist = list(np.array(newframe['word'].tolist()))
    keylist = mylist[0].split(',')

    # 업데이트 불용키워드 제거
    for item in droplist:
        if item in keylist:
            del keylist[keylist.index(item)]

    return startyear, startmonth, startday, endyear, endmonth, endday, keylist

def selectToken(token, update_id, removekeyword):
    conn = None  # 접속 객체
    cur = None  # 커서 객체

    try:
        # 아이디/비번@hostname:port_number/sid(시스템 인식자(데이터 베이스 이름))
        loginfo = 'python/oracle@192.168.0.50:1521/xe'
        conn = cx_Oracle.connect(loginfo, encoding='utf-8')

        for idx in range(0, len(update_id) - 1):
            keyword = selectKey(token, update_id, removekeyword, idx)
            print(keyword)
            startyear = str(keyword[0])
            startmonth = str(keyword[1])
            startday = str(keyword[2])
            endyear = str(keyword[3])
            endmonth = str(keyword[4])
            endday = str(keyword[5])
            keylist = keyword[6]

            # Keyword_analysis(conn, startyear, startmonth, startday, endyear, endmonth, endday, keylist)
            Update_analysis(conn, startyear, startmonth, startday, endyear, endmonth, endday, keylist)


    except Exception as err:
        print(err)

    finally:
        if conn is not None:
            conn.close()

def Keyword_analysis(conn, startyear, startmonth, startday, endyear, endmonth, endday, keylist):
    for item in keylist:
        sql = " select * from reviews "
        sql += " where contents like '%" + item + "%'"
        sql += " and ((year = " + startyear + " and month = " + startmonth + " and day > " + startday + ") "
        sql += " or (year = " + endyear + " and month = " + endmonth + " and day <= " + endday + ")) "

        mycolumns = ['store', 'score', 'year', 'month', 'day', 'contents']

        myframe = pd.read_sql(sql=sql, con=conn, columns=mycolumns)
        myframe.set_index('ID', inplace=True)
        print(myframe.head())
        print('-'*50)
        break

def Update_analysis(conn, startyear, startmonth, startday, endyear, endmonth, endday, keylist):
    cnt = 0
    sql = " select * from reviews "
    sql += " where ("
    for item in keylist:
        sql += " contents like '%"+item+"%'"
        cnt += 1
        if cnt < len(keylist):
            sql += " or "
    sql += " ) and ((year = " + startyear + " and month = " + startmonth + " and day > " + startday + ") "
    sql += " or (year = " + endyear + " and month = " + endmonth + " and day <= " + endday + ")) "
    # print(sql)
    mycolumns = ['store', 'label', 'score', 'year', 'month', 'day', 'contents']

    myframe = pd.read_sql(sql=sql, con=conn, columns=mycolumns)
    myframe.set_index('ID', inplace=True)

    filename = 'update_review_' + startyear + '년' + startmonth + '월' + startday + '일.csv'

    myframe.to_csv(filename, encoding='utf-8')

    print(myframe)
    print('-' * 50)

def main():
    token = csvTOframe('update_word_csv_v03.csv')
    update_id = txtTOlist('update_id.txt')
    removekeyword = txtTOlist('removekeyword.txt')
    selectToken(token, update_id, removekeyword)
    print('finished')

if __name__=="__main__":
    main()