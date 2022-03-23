from models.model import Model


class Period(Model):
    table_name = 'periods'
    start_at = None
    end_at = None
    weekday = None
    details = None
    subject_id = None
    location = None

    def __init__(self):
        super().__init__()

    def all(self):
        periods = self.table(self.table_name).fetch_all()
        return self.create_model_collection(periods)

    def get(self):
        periods = self.db_get()
        return self.create_model_collection(periods)

    def where(self, column, value):
        self.table(self.table_name).db_where(column, value)
        return self

    @staticmethod
    def create_model_collection(results):
        collection = []
        for result in results:
            model = Period()
            model.start_at = result[1]
            model.end_at = result[2]
            model.weekday = result[3]
            model.details = result[4]
            model.subject_id = result[5]
            model.location = result[6]
            collection.append(model)
        return collection