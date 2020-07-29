from query import Query
from mileage import Mileage, Route


class Generator():

    def __init__(self):
        self.query = Query()

    def next_mileage(self, _id):
        m = self.query.search(_id)[0]
        return self.query.search(start=m.end.name)[0]

    def generate_route(self, _id):
        start = self.query.search(_id)[0]
        li = [start]
        m = start
        for i in range(3):
            m = self.next_mileage(m.id)
            li.append(m)

        return Route(li)
