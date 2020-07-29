from query import Query
from mileage import Mileage

class Generator():

    def __init__(self, _id):
        self.id = _id
        self.query = Query()
        self.mileage = self.query.search(self.id)[0]

    def next_dict(self, m):
        return {m: self.query.search(start=m.end.name)}

    def generate(self):
        result = []
        v = self.next_dict(self.mileage)
        if len(v) > 0:
            result.append(v)
            for i in v[self.mileage]:
                a = self.next_dict(i)
                if len(a[i]) > 0:
                    result.append(a)
                    for y in a[i]:
                        f = self.next_dict(y)
                        if len(f[y]) > 0:
                            result.append(f)
                            for e in f[y]:
                                g = self.next_dict(e)
                                if len(g[e]) > 0:
                                    result.append(g)
        return result




