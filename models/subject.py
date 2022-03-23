from models.model import Model


class Subject(Model):
    table_name = 'subjects'
    name = None
    code = None
    lecturer = None
    description = None

    def __init__(self):
        super().__init__()

    def where(self, column, value):
        self.table(self.table_name).db_where(column, value)
        return self

    def all(self):
        subjects = self.table(self.table_name).fetch_all()
        return self.create_model_collection(subjects)

    def get(self):
        subjects = self.db_get()
        return self.create_model_collection(subjects)

    def first(self):
        subject = self.table(self.table_name).fetch_one()
        return self.create_model(subject)

    def create_model_collection(self, results):
        collection = []
        for result in results:
            model = self.create_model(result)
            collection.append(model)
        return collection

    @staticmethod
    def create_model(data_array):
        model = Subject()
        model.name = data_array[1]
        model.code = data_array[2]
        model.lecturer = data_array[3]
        model.description = data_array[4]
        return model