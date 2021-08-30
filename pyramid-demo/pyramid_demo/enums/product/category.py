import enum

class Category(enum.Enum):
    FOOD = 1
    BEAUTY = 2
    HEALTH = 3
    OTHER = 4
    
    def option(self):
        # self is the member here
        return self.value, self.name
