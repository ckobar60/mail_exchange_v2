def create_database():
    connect_bd = psycopg2.connect(
    database = input('Введите имя базы данных: '), 
    user=input('Введите имя пользователя: '), 
    password=input('Введите пароль: '), 
    host=input('Введите хост "127.0.0.1": '), 
    port=input('Введите порт "5432": ')
    )
    current = connect_bd.cursor() 
    current.execute('''CREATE TABLE EMAILS  
    (RAIPO TEXT NOT NULL,
    LOGIN TEXT NOT NULL,
    PASSWORD TEXT NOT NULL,
    LAST TEXT NOT NULL);''')

    connect_bd.commit()  
    add_email = "Y"
    while ('N' not in add_email and 'n' not in add_email and 'Н' not in add_email and 'н' not in add_email):
        add_raipo = input('Введите название подразделения: ')
        add_login = input('Введите адрес почты: ')
        add_pass = input('Введите пароль: ')
        current = connect_bd.cursor()
        current.execute(
        "INSERT INTO EMAILS (RAIPO,LOGIN,PASSWORD,LAST) VALUES ('" + str(add_raipo) + "' , '" + str(add_login) + "' , '" + str(add_pass) + "' , '" + "0')"    
        )   
        connect_bd.commit() 
        add_email = input('Добавить почту Y/N: ')

    else:  
        current.execute("SELECT RAIPO,LOGIN,PASSWORD,LAST from EMAILS") 

    #print(current.fetchall())
    connect_bd.close()
            
    
if __name__ == "__main__":
    import psycopg2
    create_database()