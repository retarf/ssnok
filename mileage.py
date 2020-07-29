
class State():
    SX = "SX"
    S1 = "S1"

class Mileage():
    def __init__(self, data: tuple):
        self.id = data[0]
        self.start = Semaphore(data[1])
        self.end = Semaphore(data[2])

    def __str__(self):
        return f'M(id={self.id})'

    def __repr__(self):
        return f'M(id={self.id})'

class Semaphore():

    def __init__(self, name: str):
        self.name = name
        self.__state = None

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, state: str):
        valid_states = (State.SX, State.S1)
        if state not in valid_states:
            raise Exception(f"Semaphore state is not valid. Valid states: " \
                f"{valid_states}")
        self.__state = state

    def __repr__(self):
        return f"{self.name}: {self.state}"
