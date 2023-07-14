import random

from network import *
from game import *
import pygame
from pygame.locals import *


def initialize_population(POPULATION_SIZE):
    # Create population of random networks
    population = []
    for _ in range(POPULATION_SIZE):
        network = NeuralNetwork()
        population.append(network)
    return population

def select_parents(population, fitnesses):
    # sorted_population = sorted(population, key=lambda x: x.fitness, reverse=True)
    POPULATION_SIZE = len(population)
    zip_list = list(zip(population, fitnesses))
    sorted_zip_list = sorted(zip_list, key=lambda x: x[1], reverse=True)
    sorted_population = [x[0] for x in sorted_zip_list]
    num_elites = int(POPULATION_SIZE * 0.1)
    elites = sorted_population[:num_elites]
    parents = sorted_population[:num_elites + POPULATION_SIZE // 2]
    # new_borns = initialize_population(POPULATION_SIZE - len(parents) - len(elites))
    # parents += new_borns
    return parents, elites

# Crossover
def crossover(parents):
    children = []
    for i in range(0, len(parents)):
        # random select two parents
        parent1 = random.choice(parents)
        parent2 = random.choice(parents)
        while parent1 == parent2:
            parent2 = random.choice(parents)

        # Create child
        child = NeuralNetwork()

        parent1_network_params = [parent1.weights, parent1.biases, parent1.weights_hidden, parent1.biases_hidden,
                          parent1.weights_output, parent1.biases_output]
        parent2_network_params = [parent2.weights, parent2.biases, parent2.weights_hidden, parent2.biases_hidden,
                          parent2.weights_output, parent2.biases_output]
        child_network_params = [child.weights, child.biases, child.weights_hidden, child.biases_hidden,
                          child.weights_output, child.biases_output]

        for item in range(len(parent1_network_params)):
            if random.random() < 0.5:
                child_network_params[item] = parent1_network_params[item]
            else:
                child_network_params[item] = parent2_network_params[item]


        children.append(child)

    return children


def mutate(offspring):

    for child in offspring:
        child_network_params = [child.weights, child.biases, child.weights_hidden, child.biases_hidden,
                                child.weights_output, child.biases_output]

        for item in child_network_params:
            if random.random() < MUTATION_RATE:
                item += np.random.uniform(-0.1,0.1,item.shape)

    return offspring


def evaluate_population(population,screen,screen_font,clock,birds,pillars):

    fitnesses = [0 for _ in population]
    birds_die = [0 for _ in birds]

    best_bird_generation = population[0] #the bird with the highest fitness this generation
    best_fitness_generation = 0 #the highest fitness this generation

    # pygame.init()
    # screen.fill((255,0,0))
    score = 0
    through_flag = False
    through_flag_last = False

    while True:
        clock.tick(60)
        pygame.display.flip()

        screen.fill((255, 255, 255))

        for i,bird in enumerate(birds):
            if birds_die[i]:
                continue
            # Draw each bird
            pygame.draw.circle(screen, (0,0,0),
                               (bird.x, bird.y), bird.width//2)
            # pygame.draw.circle(screen, (0, 0, 0), (bird.x, bird.y), 10)

        for pillar in pillars:
            # Draw pillars
            pygame.draw.rect(screen, (0,255,0), pillar.top)
            pygame.draw.rect(screen, (0,255,0), pillar.bottom)

        #compute score flag
        compute_score_flag = False
        for i, bird in enumerate(birds):
            if birds_die[i]:
                continue
            # Get inputs for network
            pillar = pillars[0]
            dist_to_pillar = pillar.top.x - bird.x
            dist_height1 = pillar.top.y - bird.y
            dist_height2 = pillar.bottom.y - bird.y
            # Get action from network
            action = population[i].predict([dist_to_pillar, dist_height1, dist_height2])
            # print(action)
            if action > 0.5:
                bird.flap()
            # Update physics
            bird.update()
            # Check for collision
            if hit(bird, pillar):
                # fitnesses[i] -= (abs(pillar.top.x - bird.x) + abs((pillar.top.y+pillar.bottom.y)/2 - bird.y))
                # birds.remove(bird)
                birds_die[i] = 1
                continue
            # Increment fitness
            fitnesses[i] += 1
            if not compute_score_flag:
                score,through_flag,through_flag_last = update_score(bird,pillars[0],score,through_flag,through_flag_last)
                compute_score_flag = True
            # draw score
            score_text = screen_font.render(str(score), True, RED)
            screen.blit(score_text, (10, 10))
        # Update pillars
        pillars[0].update()
        if pillar.top.x < -pillar.width:
            pillars.pop(0)
            pillars.append(Pillar(400))
        # End if all birds crashed
        if len(birds) == sum(birds_die):
            break
        if sum(birds_die) == len(birds)-1:
            best_bird_generation = population[birds_die.index(0)]
            best_fitness_generation = fitnesses[birds_die.index(0)]
    return fitnesses, best_bird_generation, best_fitness_generation