from database.DB import DB

def migrate_subscribers_table():
    db = DB()
    query = '''
    CREATE TABLE subscribers (
        id integer,
        telegram_id integer,
        notify boolean,
        notification_time integer,
        status varchar(255)
    )
    '''
    db.cursor.execute(query)
    db.connection.commit()
    db.connection.close()