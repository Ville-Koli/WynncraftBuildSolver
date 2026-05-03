from Backend.Constants import skill_point_tags, skill_point_tags_conversion, percentage_conversion, inverse_percentage_conversion, skill_tags
from Backend.Attribute import Attribute, Requirements

class Item():
    def __init__(self, jsonObject, indexEvaluator):
        self.__jsonObject = jsonObject
        self.__index = indexEvaluator(self)
        self.__requirements = Requirements(self.__jsonObject['requirements'])
        self.__attributes = Attribute()
        
        if('identifications' in self.__jsonObject):
            identifications = self.__jsonObject['identifications']
            for key in skill_point_tags:
                if key in identifications:
                    value = identifications[key]
                    converted_key = skill_point_tags_conversion[key]
                    if type(value) is dict:
                        self.__attributes.add(converted_key, identifications[key]['raw'])
                    elif type(value) is int:
                        self.__attributes.add(converted_key, identifications[key])

    def get_attributes(self):
        return self.__attributes

    def get(self, args):
        key = self.__jsonObject
        for arg in args:
            if arg in key:
                key = key[arg]
            else:
                return None
        return key
    
    def get_combination(self, aargs, weights={}):
        combined = 0
        for arg in aargs:
            value = self.get(arg)
            multiplicative_value = 1
            if(value == None):
                continue
            key = arg[-1]
            weight = 1

            if(key in percentage_conversion):
                conversion_value = self.get(percentage_conversion[key])
                if(conversion_value != None):
                    multiplicative_value = conversion_value
            if(key in inverse_percentage_conversion):
                conversion_value = self.get(inverse_percentage_conversion[key])
                if(conversion_value != None):
                    multiplicative_value = conversion_value
            if(key in weights):
                weight = weights[key]
            if(type(value) is dict):
                if(key in skill_tags):
                    combined += (min(130, value['max'])) * weight * multiplicative_value
                else:
                    combined += value['max'] * weight * multiplicative_value
            elif(type(value) is int):
                if(key in skill_tags):
                    combined += min(130, value) * weight * multiplicative_value
                else:
                    combined += value * weight * multiplicative_value
        return combined
    
    def get_index(self): return self.__index
    
    def requirements(self):
        return self.__requirements
    
    def __str__(self):
        return "%s"%(self.__jsonObject['displayName'])