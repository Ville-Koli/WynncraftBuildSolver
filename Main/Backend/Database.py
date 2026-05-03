from Backend.Constants import conversion
from Backend.Filter import Filter
from Backend.Item import Item
from Backend.Build import Build
from typing import Dict, List, Any

import json

def load_items(filepath: str = 'Backend/compress.json') -> List[Dict[str, Any]]:
    """Load raw items from the WynnBuilder compress.json dataset."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

class Database():
    def __init__(self, indexEvaluator, weapon):
        self.__database = load_items()
        self.__itemDatabase = [Item(item, indexEvaluator) for item in self.__database]
        self.__stat_table = self.calculate_stat_table()
        self.__inverse_stat_table = self.calculate_inverse_stat_table()
        self.__stat_list = self.calculate_list_of_stats()
        self.__stat_list.sort()
        self.__sorted_tagged_database = {
            "helmets": self.get_by_subtype("helmet"),
            "chestplates": self.get_by_subtype("chestplate"),
            "leggings": self.get_by_subtype("leggings"),
            "boots": self.get_by_subtype("boots"),
            "rings": self.get_by_subtype("ring"),
            "bracelets": self.get_by_subtype("bracelet"),
            "necklaces": self.get_by_subtype("necklace"),
        }

        plural = weapon + "s"
        self.__sorted_tagged_database[plural] = self.get_by_subtype(weapon)
        conversion["weapon"] = plural

        for key in self.__sorted_tagged_database:
            self.__sorted_tagged_database[key].sort(
                key = lambda v : v.get_index(),
                reverse=True
            )
    
    def find_item(self, name):
        for item in self.__itemDatabase:
            if(item.get(['displayName']) == name):
                return item
        return None
    
    def calculate_stat_table(self):
        pathed = {
            'base' : set(),
            'identifications' : set()
        }
        for item in self.__itemDatabase:
            for element in list(pathed):
                value = item.get([element])
                if value == None: continue
                for id in value:
                    pathed[element].add(id)
        return pathed
    
    def calculate_inverse_stat_table(self):
        stat_table = self.__stat_table
        inverse_table = dict()
        for type in stat_table:
            for element in stat_table[type]:
                inverse_table[element] = type
        return inverse_table
    
    def calculate_list_of_stats(self):
        stat_table = self.__stat_table
        ls = set()
        for type in stat_table:
            for element in stat_table[type]:
                ls.add(element)
        return list(ls)

    def get_stat_table(self):
        return self.__stat_table

    def get_inverse_stat_table(self):
        return self.__inverse_stat_table
    
    def get_stat_list(self):
        return self.__stat_list
    
    def get_weapon_table(self):
        all_weapons = set()
        for item in self.__itemDatabase:
            value = item.get(['type'])
            if(value == None or value != "weapon"): continue
            all_weapons.add(item.get(['subType']))
        return all_weapons
    
    def get_armour_table(self):
        all_armour = set()
        for item in self.__itemDatabase:
            value = item.get(['type'])
            if(value == None or value != "armour"): continue
            all_armour.add(item.get(['subType']))
        return all_armour
    
    def get_accessory_table(self):
        all_accessories = set()
        for item in self.__itemDatabase:
            value = item.get(['type'])
            if(value == None or value != "accessory"): continue
            all_accessories.add(item.get(['subType']))
        return all_accessories

    def generate_build(self, args) -> Build:
        build = dict()
        for key in args:
            found = self.find_item(args[key])
            if(found == None): continue
            build[key] = found
        return Build(build)

    def get_items(self):
        return self.__itemDatabase

    def get_items(self, index):
        return self.__itemDatabase[index]
    
    def filter_by(self, filters: List[Filter]):
        return [item for item in self.__itemDatabase  if all([filter.apply(item) for filter in filters])]
    
    def get_by_subtype(self, typeName):
        return self.filter_by([
            Filter(['subType'], lambda value : value == typeName),
            Filter(['requirements', 'level'], lambda value : value > 70)
        ])

    def get_tagged_items(self):
        return self.__sorted_tagged_database