import enum

class Status(enum.Enum):
    ACTIVE = 'A'
    INACTIVE = 'I'
    
    def option(self):
        # self is the member here
        return self.value, self.name
