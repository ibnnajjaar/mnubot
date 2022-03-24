from database.DB import DB
from support.SubscriberStatus import SubscriberStatus


class Subscriber(DB):

    id = None
    telegram_id = None
    notify = False
    notification_time = None
    status = SubscriberStatus.INACTIVE.value

    def __init__(self):
        super().__init__()

    def all(self):
        query = '''SELECT * FROM subscribers'''
        self.cursor.execute(query)
        subscribers = self.cursor.fetchall()
        return self.create_model_collection(subscribers)

    def get(self, telegram_id):
        query = '''
        SELECT * FROM subscribers
        WHERE telegram_id = :telegram_id
        '''
        self.cursor.execute(query, {'telegram_id': telegram_id})
        subscriber = self.cursor.fetchone()
        if subscriber:
            return self.create_model(subscriber)
        return None

    def register(self, telegram_id):
        subscriber = self.get(telegram_id)
        if subscriber:
            return "User is already registered!"
        else:
            self.create(telegram_id)
            return "User registered successfully!"

    def create(self, telegram_id):
        query = '''
        INSERT INTO subscribers
        (telegram_id, status)
        VALUES 
        (:telegram_id, :status)
        '''
        self.cursor.execute(query, {'telegram_id': telegram_id, 'status': SubscriberStatus.ACTIVE.value})
        self.connection.commit()

    def create_model_collection(self, results):
        collection = []
        for result in results:
            model = self.create_model(result)
            collection.append(model)
        return collection

    @staticmethod
    def create_model(data_array):
        model = Subscriber()
        model.id = data_array[0]
        model.telegram_id = data_array[1]
        model.notify = data_array[2]
        model.notification_time = data_array[3]
        model.status = data_array[4]
        return model