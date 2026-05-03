from Backend.Database import Database
from Backend.Build import Build
from Backend.Constants import conversion, unequippable_cost
from typing import List

import random

def evaluate_build(build: Build):
    return build.get_index()

class GeneticAlgorithm():
    def __init__(self, database: Database, population_size, evaluator = evaluate_build):
        self.__database: Database = database
        self.__population_size = population_size
        self.__best_performing = 0
        self.__evaluator = evaluator

        self.__population = [self.generateRandomEntity() for _ in range(0, population_size)]

    def add_seed(self, build: Build):
        self.__population.append(build)
        self.__population_size += 1
    
    def get_population(self): return self.__population

    def generateRandomEntity(self) -> Build:
        data = self.__database.get_tagged_items()
        build = dict()
        for key in conversion:
            data_key = conversion[key]
            build[key] = data[data_key][random.randint(0, len(data[data_key]) - 1)]
        return Build(build)
    
    def evaluateEntity(self, entity: Build) -> float:
        if(entity.has_enough_skill_points()):
            return self.__evaluator(entity)
        return self.__evaluator(entity) * unequippable_cost # cost for not being equippable

    def crossover(self, parentA: Build, parentB: Build) -> Build:
        child_build = dict()
        parent_items = list(parentA.get_items())

        worse_performing_parent = parentA
        best_performing_parent = parentB
        if(self.evaluateEntity(parentA) > self.evaluateEntity(parentB)):
            best_performing_parent = parentA
            worse_performing_parent = parentB

        for key in parent_items:
            if(random.uniform(0, 1) < 0.75):
                child_build[key] = best_performing_parent.get_items()[key]
            else:
                child_build[key] = worse_performing_parent.get_items()[key]
        
        finalized_build = Build(child_build)

        if(random.uniform(0, 1) < 0.05): # during crossover mutation chance
            self.mutation(finalized_build)

        if(random.uniform(0, 1) < 0.01): # during crossover mutation chance
            for _ in range(0, random.randint(2, 5)):
                self.mutation(finalized_build)

        if self.evaluateEntity(finalized_build) >= self.evaluateEntity(parentA):
            return finalized_build
        elif random.uniform(0, 1) < 0.2:  # 20% chance to accept worse child
            return finalized_build
        return random.choice([parentA, parentB])


    def mutation(self, parentA: Build) -> Build:
        items = parentA.get_items()
        key_list = list(conversion)
        random_key = key_list[random.randint(0, len(key_list) - 1)]
        converted_key = conversion[random_key]
        random_item_database = self.__database.get_tagged_items()[converted_key]
        items[random_key] = random_item_database[random.randint(0, len(random_item_database) - 1)]

    def sort_population(self):
        self.__population.sort(
            key=lambda build : self.evaluateEntity(build),
            reverse=True
        )

    def selection(self) -> List[Build]:
        tournament_size = 5
        selected = []
        while len(selected) < self.__population_size // 2:
            candidates = random.sample(self.__population, tournament_size)
            winner = max(candidates, key=lambda b: self.evaluateEntity(b))
            selected.append(winner)
        return selected

    def generation(self) -> List[Build]:
        selected_population = self.selection()

        self.sort_population()

        best = selected_population[0]
        evaluation = self.evaluateEntity(best)
        if(self.__best_performing < evaluation):
            self.__best_performing = evaluation
            print("new best has been found: %s"%(self.__best_performing))

        while(len(selected_population) < self.__population_size):
            parentA: Build = random.choice(selected_population)
            parentB: Build = random.choice(selected_population) # we will not take into account the fact that A can be B by concious decision

            child = self.crossover(parentA, parentB)

            selected_population.append(child)

        for i in range(0, 5): # elitism
            selected_population.append(self.__population[i])
        
        self.__population = selected_population

        # return global best and the average of current generation
        return self.__best_performing, sum([self.evaluateEntity(entity) for entity in selected_population]) / self.__population_size
    
    def generations(self, iterations):
        best_individual = []
        average_individual = []
        x = []
        for i in range(0, iterations):
            x.append(i)
            best, average = self.generation()
            best_individual.append(best)
            average_individual.append(average)
        return x, best_individual, average_individual