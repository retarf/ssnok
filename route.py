from query import Query

class RouteError(Exception):
    pass

class Route():

    def __init__(self, _id):
        self.id = _id
        self.query = Query()
        self.data = self.query.find_mileage(self.id)
        if len(self.data) == 0:
            raise RouteError(f'Mileage with id = {self.id} does not exists.')
        self.mileage = self.data[0]
        self.length = 4
        self.list = self.get_route()

    def get_route(self):
        mileage_list = []
        mileage = self.mileage
        for i in range(self.length):
            mileage_list.append(mileage)
            try:
                mileage = self.query.find_mileage(start=mileage[2])[0]
            except IndexError:
                break

        return mileage_list
