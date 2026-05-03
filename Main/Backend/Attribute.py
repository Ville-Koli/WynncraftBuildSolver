from Backend.Constants import skill_tags

class Attribute():
    def __init__(self, json_object = {}):
        self.__attributes = dict()
        for key in skill_tags:
            if key in json_object:
                if(key not in self.__attributes):
                    self.__attributes[key] = json_object[key]
                else:
                    self.__attributes[key] += json_object[key]
            else:
                self.__attributes[key] = 0
    
    def get_attributes(self):
        return self.__attributes
    
    def total_amount_of_skill_points(self):
        total_sum = 0
        for key in self.__attributes:
            total_sum += self.__attributes[key]
        return total_sum
    
    def expand(self, other: Attribute) -> Attribute: # the change between collapse
        delta = Attribute()
        for key in other.__attributes:
            if key in self.__attributes:
                if(self.__attributes[key] >= other.__attributes[key]):
                    self.__attributes[key] = self.__attributes[key]
                    delta.add(key, 0)
                else:
                    delta.add(key, abs(self.__attributes[key] - other.__attributes[key]))
                    self.__attributes[key] = other.__attributes[key]
            else:
                self.__attributes[key] = other.__attributes[key]
                delta.add(key, other.__attributes[key])
        return delta
    
    def as_requirement(self):
        requirement = Requirements(self)
        return requirement

    def collapse(self, other: Attribute): # collapses negative values at 0
        for key in other.__attributes:
            if key in self.__attributes:
                self.__attributes[key] = max(self.__attributes[key] - other.__attributes[key], 0)
        return self

    def add(self, stat: str, value: float):
        if(stat in self.__attributes):
            self.__attributes[stat] += value
        return self

    def sub(self, stat: str, value: float):
        if(stat in self.__attributes):
            self.__attributes[stat] -= value
        return self

    def __add__(self, other: Attribute):
        for key in other.__attributes:
            if key in self.__attributes:
                self.__attributes[key] += other.__attributes[key]
        return self

    def __sub__(self, other: Attribute):
        for key in other.__attributes:
            if key in self.__attributes:
                self.__attributes[key] -= other.__attributes[key]
        return self

    def __str__(self):
            return str(self.__attributes)

class Requirements():
    def __init__(self, json):
        self.__attribute = Attribute(json)

    def add(self, requirement: Requirements):
        self.__attribute.expand(requirement.__attribute)
        return self
    
    def total_sum(self):
        return self.__attribute.total_amount_of_skill_points()
    
    def get_as_attributes(self) -> Attribute:
        return self.__attribute
    
    def __str__(self):
        return str(self.__attribute)