class Room():
    def __init__(self, pin):
        self.all_users = []
        self.ready_users = {}
        self.pending_users = {}
        self.pin = pin
    
    def add_user(self, name):
        self.pending_users[name] = User(name)
        self.all_users.append(name)
    
    def remove_user(self, name):
        if name in self.pending_users:
            self.all_users.remove(name)
            del self.pending_users[name]
        elif name in self.ready_users:
            self.all_users.remove(name)
            del self.ready_users[name]
    
    def change_user_ready_state(self, name):
        # print("Ready: " + str(self.ready_users))
        # print("Pending: " + str(self.pending_users))
        if name in self.pending_users:
            self.ready_users[name] = self.pending_users[name]
            del self.pending_users[name]
        elif name in self.ready_users:
            self.pending_users[name] = self.ready_users[name]
            del self.ready_users[name]


class User():
    def __init__(self, name):
        self.score = 0
        self.name = name