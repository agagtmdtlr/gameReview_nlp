import pandas as pd
import cx_Oracle

log = 'oraman/oracle@localhost:1521/xe'
conn = cx_Oracle.connect(log,encoding='utf-8')
curr = conn.cursor()

# 베이지안 라벨이 붙어있는 프레임
upFrame = pd.read_csv('../update_word_csv_v04.csv', index_col='update_id')
update_ID = [60,54,49,45,41,37,33,28,24,20,17,14,8]

df_dict = dict()

def select(upFrame,update_ID):
    frame = upFrame.loc[[update_ID[-1]],['year','month','day','word']]
    row = list(frame.iterrows())
    byear = row[0][1][0]
    bmonth = row[0][1][1]
    bday = row[0][1][2]
    keyword_list = row[0][1][3].split(',')

    keyword = " or ".join([f" contents like '%{x}%' " for x in keyword_list])
    try:
        sql = " select * from reviews "
        sql += f" where ( {keyword} "
        sql += f" ) and ( ( year ='{byear}' and month = '{bmonth}' and day <= '{bday}' )" \
               f" or ( year='{byear}' and month > '{bmonth}' and day >= '1') )"

        frame = pd.read_sql(sql, conn)
        print(len(frame))
        frame.to_csv(f'select_review_by_update_data/update_id{update_ID[-1]}_{byear}_{bmonth}_{bday}.csv')
    except Exception as err:
        print(err)
    ##################
    for idx in range(len(update_ID)-1):
        df_dict[idx] = dict()

        frame = upFrame.loc[[update_ID[idx],update_ID[idx+1]],['year','month','day','word']]
        row = list(frame.iterrows())
        byear = row[0][1][0]
        bmonth = row[0][1][1]
        bday = row[0][1][2]
        keyword_list = row[0][1][3].split(',')

        eyear = row[1][1][0]
        emonth = row[1][1][1]
        eday = row[1][1][2]

        keyword = " or ".join([f" contents like '%{x}%' " for x in keyword_list])

        try:
            sql = " select * from reviews "
            sql += f" where ( {keyword} "
            sql +=f" ) and ( ( year ='{eyear}' and month = '{emonth}' and day > '{eday}' )" \
                    f" or ( year='{byear}' and month = '{bmonth}' and day <= '{bday} ') )"\

            frame = pd.read_sql(sql,conn)
            print(len(frame))
            if len(frame) >= 200:
                df_dict[idx][keyword] = frame
                frame.to_csv(f'update_id{update_ID[idx]}_{byear}_{bmonth}_{bday}.csv')
        except Exception as err :
            print(err)
            continue
        print('len',len(df_dict[idx].keys()))


select(upFrame,update_ID)