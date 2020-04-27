 
def email_conn(directory):
    connect_bd = psycopg2.connect(
    database="mail_db", 
    user="postgres", 
    password="", 
    host="127.0.0.1", 
    port="5432"
    )
    cur = connect_bd.cursor()
    cur.execute("SELECT RAIPO,LOGIN,PASSWORD,LAST from EMAILS") 
    rows = cur.fetchall() 
    server = "imap.yandex.ru"
    port = "143"
    i=0
    for row in rows: 
        login = rows[i][1]
        password = rows[i][2]
        mail = imaplib.IMAP4_SSL(server)
        mail.login(login, password)
        mail.list()
        mail.select("inbox", readonly = True)
        result, data = mail.uid('search', None, "ALL") 

        last_email_uid = int(rows[i][3])
        new_email_uid = int(data[0].split()[-1]) 
        
                
        for email_uid in data[0].split():
            if int(email_uid) > last_email_uid:
                result, data = mail.uid('fetch', email_uid, '(RFC822)')
                raw_email = data[0][1]           
                try:
                    email_message = email.message_from_string(raw_email)            
                except TypeError:
                    try:
                        email_message = email.message_from_bytes(raw_email)                       
                        for part in email_message.walk():
                            if "application" in part.get_content_type() :       
                                filename = part.get_filename()
                                filename=str(email.header.make_header(email.header.decode_header(filename)))
                                if "6027108130" and "_Д" in filename:
                                    fp = open(os.path.join(directory +"Дива_Плюс/", filename), 'wb')
                                    fp.write(part.get_payload(decode=1))
                                    fp.close
                                elif "6027149513" and "_УТ" in filename:
                                    fp = open(os.path.join(directory +"Дитрейд/", filename), 'wb')
                                    fp.write(part.get_payload(decode=1))
                                    fp.close
                                elif "6027173812" and "_5ГК" in filename:
                                    fp = open(os.path.join(directory +"Мега_Холод/", filename), 'wb')
                                    fp.write(part.get_payload(decode=1))
                                    fp.close
                                elif "7802548281_РЛ" in filename:
                                    fp = open(os.path.join(directory +"Региональная_Логистика/", filename), 'wb')
                                    fp.write(part.get_payload(decode=1))
                                    fp.close
                                elif "7811215747_ГЛ" in filename:
                                    fp = open(os.path.join(directory +"Глобал_Лоджистикс/", filename), 'wb')
                                    fp.write(part.get_payload(decode=1))
                                    fp.close
                                elif "532111776395_" in filename:
                                    fp = open(os.path.join(directory +"Пр._Никоноров/", filename), 'wb')
                                    fp.write(part.get_payload(decode=1))
                                    fp.close
                                elif "6001000149_" and "_РайпоБежаницы-" in filename:
                                    if ".rnp" in filename:
                                        fp = open(os.path.join(directory + "Пушгоры_МСЗ/" + str(datetime.date.today()) + "/" , filename), 'wb')
                                        fp.write(part.get_payload(decode=1))
                                        fp.close
                                    elif "6001000149_" and "_РайпоБежаницы-Дедовичи" in filename:
                                        fp = open(os.path.join(directory + "Пушгоры_МСЗ/" + str(datetime.date.today()) + "/" , filename + ".rnp"), 'wb')
                                        fp.write(part.get_payload(decode=1))
                                        fp.close
                                    elif "6001000149_" and "_РайпоБежаницы-" in filename:
                                        fp = open(os.path.join(directory + "Пушгоры_МСЗ/" + str(datetime.date.today()) + "/" , filename + "горячий_хлеб.rnp"), 'wb')
                                        fp.write(part.get_payload(decode=1))
                                        fp.close
                    except:
                        continue
                        

        cur = connect_bd.cursor()
        cur.execute("UPDATE EMAILS set LAST = " + str(new_email_uid) + " where RAIPO = " + "'" + str(rows[i][0]) + "'")
        connect_bd.commit()
        cur.execute("SELECT RAIPO,LOGIN,PASSWORD,LAST from EMAILS")
        i+=1 
    #print(cur.fetchall())


def remove_old_files(directory):
    for dir in os.listdir(directory):
        dirs.append(directory + "/" + dir  )        
        for dir in dirs:
            path = str(dir)
            now = time.time()
            for filename in os.listdir(path):                
                if ".rnp" not in filename:
                    if os.path.getmtime(os.path.join(path, filename)) < now - 7 * 86400:
                        if os.path.isdir(os.path.join(path, filename)):
                            shutil.rmtree(str(path + "/" + filename))
                elif os.path.getmtime(os.path.join(path, filename)) < now - 7 * 86400:
                    if os.path.isfile(os.path.join(path, filename)):
                        os.remove(os.path.join(path, filename))
    
           
if __name__ == "__main__":
    import psycopg2, sys , imaplib, email , os, datetime, time, shutil
    directory = r"/volume1/Mail_Exchange/"
    dirs = []
    try:
        today = os.mkdir(directory + "Пушгоры_МСЗ/" + str(datetime.date.today() + "/"))
    except:
        pass

    remove_old_files(directory)
    email_conn(directory)
