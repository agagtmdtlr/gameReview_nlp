import cx_Oracle

conn = None # 접속 객체
cur = None # 커서 객체

try:
    # 아이디/비번@hostname:port_number/sid(시스템 인식자(데이터 베이스 이름))
    loginfo = 'oraman/oracle@localhost:1521/xe'
    conn = cx_Oracle.connect(loginfo, encoding='utf-8')
    # print(type(conn))

    cur = conn.cursor()
    # print(type(cur))


    with open('review_label_02.csv', 'rt', encoding='utf-8') as file:
        mylist =[item.strip() for item in file.readlines()]


    for sublist in mylist[1:]:
        minilist = sublist.split(sep=',', maxsplit=7)
        for index, value in enumerate(minilist):
            if index == 7:
                minilist[index] = minilist[index].replace('"', '').replace("'", '')
        print(len(minilist[7]))
        print(minilist)
        if len(minilist[7]) > 5000:
            # print(len(minilist[6]))
            # print(minilist)
            sql = " insert into reviews (id, store, score, year, month, day,label)" \
                  " values('" + minilist[0] + "', '" + minilist[2] + "', '" + minilist[1] + "', '" + minilist[3] + "', '" + minilist[4] + "', '" + minilist[5] +"', '" + minilist[6] + "')"
            cur.execute(sql)
            sql = " update reviews set contents = to_clob('" + minilist[7][:1000] + "') || "
            sql += " to_clob('" + minilist[7][1000:2000] + "') || to_clob('" + minilist[7][2000:3000] + "') ||"
            sql += " to_clob('" + minilist[7][3000:4000] + "') || to_clob('" + minilist[7][4000:5000] + "') ||"
            sql += " to_clob('" + minilist[7][5000:] + "')" # || to_clob('" + minilist[6][6000] + "') ||"
            sql += " where id = '"+minilist[0]+"'"
            cur.execute(sql)

            sql = " update reviews set full_date = to_date('" + '/'.join([minilist[3],minilist[4],minilist[5]]) + "','YYYY/MM/DD')"
            sql += " where id = '"+minilist[0]+"'"
            cur.execute(sql)
        elif len(minilist[7]) > 4000:
            # print(len(minilist[6]))
            # print(minilist)
            sql = " insert into reviews (id, store, score, year, month, day,label)" \
                  " values('" + minilist[0] + "', '" + minilist[2] + "', '" + minilist[1] + "', '" + minilist[
                      3] + "', '" + minilist[4] + "', '" + minilist[5] +"', '" + minilist[6] + "')"
            cur.execute(sql)
            sql = " update reviews set contents = to_clob('" + minilist[7][:1000] + "') || "
            sql += " to_clob('" + minilist[7][1000:2000] + "') || to_clob('" + minilist[7][2000:3000] + "') ||"
            sql += " to_clob('" + minilist[7][3000:4000] + "') || to_clob('" + minilist[7][4000:] + "')"
            sql += " where id = '" + minilist[0] + "'"
            cur.execute(sql)

            sql = " update reviews set full_date = to_date('" + '/'.join(
                [minilist[3], minilist[4], minilist[5]]) + "','YYYY/MM/DD')"
            sql += " where id = '" + minilist[0] + "'"
            cur.execute(sql)
        elif len(minilist[7]) > 3000:
            # print(len(minilist[6]))
            # print(minilist)
            sql = " insert into reviews (id, store, score, year, month, day,label)" \
                  " values('" + minilist[0] + "', '" + minilist[2] + "', '" + minilist[1] + "', '" + minilist[
                      3] + "', '" + minilist[4] + "', '" + minilist[5] +"', '" + minilist[6] + "')"
            cur.execute(sql)
            sql = " update reviews set contents = to_clob('" + minilist[7][:1000] + "') || "
            sql += " to_clob('" + minilist[7][1000:2000] + "') || to_clob('" + minilist[7][2000:3000] + "') ||"
            sql += " to_clob('" + minilist[7][3000:] + "')"
            sql += " where id = '" + minilist[0] + "'"
            cur.execute(sql)

            sql = " update reviews set full_date = to_date('" + '/'.join(
                [minilist[3], minilist[4], minilist[5]]) + "','YYYY/MM/DD')"
            sql += " where id = '" + minilist[0] + "'"
            cur.execute(sql)
        elif len(minilist[7]) > 2000:
            # print(len(minilist[6]))
            # print(minilist)
            sql = " insert into reviews (id, store, score, year, month, day,label)" \
                  " values('" + minilist[0] + "', '" + minilist[2] + "', '" + minilist[1] + "', '" + minilist[
                      3] + "', '" + minilist[4] + "', '" + minilist[5] +"', '" + minilist[6] + "')"
            cur.execute(sql)
            sql = " update reviews set contents = to_clob('" + minilist[7][:1000] + "') || "
            sql += " to_clob('" + minilist[7][1000:2000] + "') || to_clob('" + minilist[7][2000:] + "') "
            sql += " where id = '" + minilist[0] + "'"
            cur.execute(sql)

            sql = " update reviews set full_date = to_date('" + '/'.join(
                [minilist[3], minilist[4], minilist[5]]) + "','YYYY/MM/DD')"
            sql += " where id = '" + minilist[0] + "'"
            cur.execute(sql)
        else:
            sql = " insert into reviews (id,store,score,year,month,day,label,contents)" \
                  " values('"+minilist[0]+"', '"+minilist[2]+"', '"+minilist[1]+"', '"+minilist[3]+"', '"+minilist[4]+"', '"+minilist[5]+"', '"+minilist[6]+"', '"+minilist[7]+"')"
            cur.execute(sql)

            sql = " update reviews set full_date = to_date('" + '/'.join(
                [minilist[3], minilist[4], minilist[5]]) + "','YYYY/MM/DD')"
            sql += " where id = '" + minilist[0] + "'"
            cur.execute(sql)
    conn.commit()

except Exception as err:
    print(err)

finally:
    if cur is not None:
        cur.close()

    if conn is not None:
        conn.close()

print('finished')