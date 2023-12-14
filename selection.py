from numpy import *

def selection(population , fitness_values):
    probs = fitness_values.copy()
    probs += abs(probs.min()) + 1
    probs = probs / probs.sum()
    length = len(population)
    indices = arange(length)
    selected_indices = random.choice(indices , size = length , p = probs)
    selected_population = population[selected_indices]
    return selected_population




def selection(population, fitness_values, tournament_size):
    selected_parents = []
    
    for _ in range(len(population)):
        # Randomly select individuals for the tournament
        length = len(population)
        indices = arange(length)
        tournament_individuals = random.choice(indices, tournament_size)
        
        # Evaluate fitness for each tournament individual
        tournament_fitness = [fitness_values[individual] for individual in tournament_individuals]
        
        # Select the individual with the highest fitness value as the parent
        selected_parent = tournament_individuals[tournament_fitness.index(max(tournament_fitness))]
        
        selected_parents.append(selected_parent)
        
    selected_population = population[selected_parents]
    return selected_population