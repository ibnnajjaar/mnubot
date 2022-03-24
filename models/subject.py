from database.DB import DB


class Subject(DB):

    id = None
    name = None
    code = None
    lecturer = None
    description = None

    def __init__(self):
        super().__init__()

    def all(self):
        query = '''SELECT * FROM subjects'''
        self.cursor.execute(query)
        subjects = self.cursor.fetchall()
        return self.create_model_collection(subjects)

    def create_model_collection(self, results):
        collection = []
        for result in results:
            model = self.create_model(result)
            collection.append(model)
        return collection

    @staticmethod
    def create_model(data_array):
        model = Subject()
        model.id = data_array[0]
        model.name = data_array[1]
        model.code = data_array[2]
        model.lecturer = data_array[3]
        model.description = data_array[4]
        return model