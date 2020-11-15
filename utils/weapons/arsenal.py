
class Arsenal(object):
    def __init__(self, default):
        self.guns = [default]
        self.active = 0

    def shoot(self):
        pass

    def add_gun(self, gun):
        self.guns.append(gun)

    def swap(self):
        self.active += 1
        self.active = self.active % len(self.guns)
