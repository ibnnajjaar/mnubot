from collections import defaultdict
from datetime import date

from database.DB import DB


class Period(DB):
    table_name = 'periods'
    id = None
    start_at = None
    end_at = None
    weekday = None
    details = None
    subject_id = None
    location = None
    subject_name = None

    def __init__(self):
        super().__init__()

    def all(self):
        query = '''
        SELECT 
        periods.id, start_at, end_at, weekday, details, subject_id, location, subjects.name  
        FROM periods
        INNER JOIN subjects ON periods.subject_id = subjects.id
        '''
        self.cursor.execute(query)
        periods = self.cursor.fetchall()
        return self.create_model_collection(periods)

    def today(self):
        today = date.today().strftime('%A')
        return self.for_day(today)

    def for_day(self, weekday):
        query = '''
        SELECT
        periods.id, start_at, end_at, weekday, details, subject_id, location, subjects.name
        FROM periods
        INNER JOIN subjects ON periods.subject_id = subjects.id
        WHERE weekday = :weekday
        '''
        self.cursor.execute(query, {'weekday': weekday})
        periods = self.cursor.fetchall()
        return self.create_model_collection(periods)

    @staticmethod
    def sort_by_weekday(unsorted_periods):
        sorted_periods = defaultdict(list)
        for period in unsorted_periods:
            sorted_periods[period.weekday].append(period)
        return sorted_periods

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
            model.subject_name = result[7] if len(result) >= 7 else None
            collection.append(model)
        return collection