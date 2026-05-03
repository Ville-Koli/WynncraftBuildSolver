from Backend.Item import Item

class Filter():
    def __init__(self, args, predicate):
        self.__args = args
        self.__predicate = predicate
    
    def apply(self, item: Item):
        return self.__predicate(item.get(self.__args))