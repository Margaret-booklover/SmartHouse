class Device:
    def __init__(self):
        self.id = None
        self.info = None
        self.param = None
        self.state = None

    def change_state(self, new_state):
        self.state = new_state

    def get_param(self):
        return self.param

    def get_state(self):
        return self.state
