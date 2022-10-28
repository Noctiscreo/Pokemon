class Pokemon:
    def __init__(self):
        self.name = None
        self.artwork = None
        self.attack = None
        self.defence = None
        self.type1 = None
        self.type2 = None

    def tojson(self):
        return {
            "name": self.name,
            "artwork": self.artwork,
            "attack": self.attack,
            "defence": self.defence,
            "type1": self.type1,
            "type2": self.type2
        }
