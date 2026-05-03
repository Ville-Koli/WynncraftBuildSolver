from typing import Dict, List, Any, Optional
from Backend.Constants import build_items
from copy import deepcopy
from Backend.Attribute import Attribute, Requirements
from Backend.Item import Item
import json

class Build():
    def __init__(self, slots: Dict[str, Item]):
        self.__stat_map: Dict[str, float] = dict()
        self.__slots = slots
        self.__equip_order = self.calculate_best_equip_order()

        self.update_build()

    def update_build(self):
        self.__stat_map: Dict[str, float] = dict()
        self.__equip_order = self.calculate_best_equip_order()
        if(len(self.__slots) > 0):
            self.__requirements = Requirements(json.loads("{}"))
            for slot in self.__slots:
                item = self.__slots[slot]
                self.update_stat_block(item)

        for key in build_items:
            if key not in self.__slots:
                self.__slots[key] = "EMPTY"
        
        self.__index = sum([self.__slots[key].get_index() for key in self.__slots])


    def get_build_order(self):
        return self.__equip_order

    def calculate_best_equip_order(self):
        list_of_items = list(self.__slots)
        list_of_items.sort(
            key = lambda k : self.__slots[k].requirements().total_sum()
        )
        return list_of_items

    def get_all_stats(self):
        return self.__stat_map
    
    def calculate_skill_points(self):
        attributes = Attribute()
        total_skill_points = 200
        for item_slot in self.get_build_order():
            item = self.__slots[item_slot]
            delta = attributes.expand(item.requirements().get_as_attributes())
            total_skill_points -= delta.total_amount_of_skill_points()
            attributes = attributes + item.get_attributes()

        return total_skill_points

    def get_total_requirements(self):
        attributes = Attribute()
        for item_slot in self.get_build_order():
            item = self.__slots[item_slot]
            attributes.expand(item.requirements().get_as_attributes())
        return attributes

    def get_added_attributes(self):
        attributes = Attribute()
        for item_slot in self.get_build_order():
            item = self.__slots[item_slot]
            attributes = attributes + item.get_attributes()
        return attributes

    def get_cached_skill_points(self):
        return self.__points
    
    def update_stat_block(self, item: Item):
        self.__requirements.add(item.requirements())
        base_stats = item.get(['base'])
        if(base_stats != None):
            for stat in base_stats:
                key = str(stat)
                if key not in self.__stat_map:
                    self.__stat_map[key] = deepcopy(base_stats[stat])
                else:
                    self.__stat_map[key] += base_stats[stat]
        identifications = item.get(['identifications'])
        if(identifications != None):
            for id in identifications:
                key = str(id)
                if key not in self.__stat_map:
                    self.__stat_map[key] = deepcopy(identifications[id])
                else:
                    identification = identifications[id]
                    if type(identification) is dict and type(self.__stat_map[key]) is dict:
                        self.__stat_map[key]["min"] += float(identification["min"])
                        self.__stat_map[key]["raw"] += float(identification["raw"])
                        self.__stat_map[key]["max"] += float(identification["max"])
                    elif type(identification) is int and type(self.__stat_map[key]) is int:
                        self.__stat_map[key] += identification
        return 200 # success
    
    def has_enough_skill_points(self):
        return self.calculate_skill_points() >= 0
    
    def get_stats(self):
        return self.__stat_map
    
    def get_items(self):
        return self.__slots
    
    def get_index(self):
        return self.__index

    def __str__(self):
        return """
        helmet: %s
        chestplate: %s
        leggings: %s
        boots: %s

        ring1: %s
        ring2: %s
        bracelet: %s
        necklace: %s

        weapon: %s

        Can be equipped: %s
        Requirements: %s
        Added attributes: %s
        Left over skill points: %s
        """%(
            self.__slots['helmet'],
            self.__slots['chestplate'],
            self.__slots['leggings'],
            self.__slots['boots'],

            self.__slots['ring1'],
            self.__slots['ring2'],
            self.__slots['bracelet'],
            self.__slots['necklace'],

            self.__slots['weapon'],

            self.has_enough_skill_points(),
            self.get_total_requirements(),
            self.get_added_attributes(),
            self.calculate_skill_points()
        )
