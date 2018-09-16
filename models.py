from sqlalchemy import Column, Integer, String
from database import Base
import json

class Program(Base):
    __tablename__ = 'programs'
    id = Column(Integer, primary_key=True)
    date = Column(String(10))
    time = Column(String(10))
    title = Column(String(100))

    def __init__(self, date=None, time=None, title=None):
        self.date = date
        self.time = time
        self.title = title

    def __repr__(self):
        return 'Program {} le {} a {}'.format(self.title, self.date, self.time)

    def as_json(self):
        data = {}
        data['date'] = self.date
        data['time'] = self.time
        data['title'] = self.title
        return json.dumps(data, sort_keys=True, indent=4)
