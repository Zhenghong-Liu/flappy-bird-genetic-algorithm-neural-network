from game import *
from geneticAlgorithm import *
from network import *
import sys


def main():
    # Parameters
    POPULATION_SIZE = 500

    SCREEN_WIDTH = 400
    SCREEN_HEIGHT = 600


    BG_COLOR = (255,255, 255)

    # Pygame init
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    score_font = pygame.font.Font('arial.ttf', 32)


    # Initialize population
    population = initialize_population(POPULATION_SIZE)

    best_bird = None  # the bird with the highest fitness
    best_fitness = 0

    while True:
        screen.fill((255, 255, 255))
        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # print("len of population",len(population))

        birds = [Bird() for _ in range(POPULATION_SIZE)]
        pillars = [Pillar(400)]

        # Evaluate population fitness
        fitnesses,best_bird_generation,best_fitness_generation = evaluate_population(population,screen,score_font,clock,birds,pillars)

        if best_fitness_generation >= best_fitness:
            best_bird = best_bird_generation
            best_fitness = best_fitness_generation
        # print("type of best bird",type(best_bird))
        # print("best fitness",best_fitness)
        # print("type of best_bird_generation",type(best_bird_generation))

        # Selection, crossover, mutation
        parents, elites = select_parents(population, fitnesses)
        # print(len(parents),len(elites))
        # Create offspring via crossover
        offspring = crossover(parents)
        # Mutate offspring
        offspring = mutate(offspring)
        #new born birds
        new_borns = initialize_population(POPULATION_SIZE - len(parents) - len(elites) - 1)
        # Replace population with offspring
        population = offspring + elites +new_borns + [best_bird]


        # Update display
        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()