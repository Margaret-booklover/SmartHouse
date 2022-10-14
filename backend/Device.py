class Device():
    def __init__(self):
        self.id = None
        self.info = None
        self.param = None
        self.state = None

    def change_state(self):
        pass

    def get_param(self):
        pass

    def get_state(self):
        return self.state
