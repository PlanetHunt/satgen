import random
import math
from deap import creator, base, tools, algorithms

# This line enable maximisation of a fitness function, for minimization
# use (-1.0,)
creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# Helper function to generate pose 3-tuple


def poseGenerator(icls, xmin, xmax, ymin, ymax):
    """Simple function to generate a random robot position and fill the
    *icls* class with it, *icls* must be initializable from an iterable.
    The robot position is generated in 2D (x, y, theta) with
    *xmin* <= x <= *xmax*, *ymin* <= y <= ymax and 0 <= theta <= pi."""
    return icls([random.uniform(xmin, xmax),
                 random.uniform(ymin, ymax),
                 random.uniform(0, 2 * math.pi)])


# Structure initializers
toolbox.register("individual", poseGenerator, creator.Individual,
                 xmin=-2, xmax=2, ymin=-2, ymax=2)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def evalPose(individual):
    """Function that evaluates the fitness value of a pose."""
    return (individual[1],)

toolbox.register("evaluate", evalPose)
toolbox.register("mate", tools.cxTwoPoints)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)


def main():
    # Create a population of 300 individuals
    population = toolbox.population(n=300)
    CXPB, MUTPB, NGEN = 0.6, 0.4, 50

    population, _ = algorithms.eaSimple(population, toolbox, cxpb=CXPB,
                                        mutpb=MUTPB, ngen=NGEN)

    # Find the best individual(s) in the resulting population
    # This returns a list
    bests = tools.selBest(population, k=1)

    # An individual is a complex object containing a fitness,
    # This will return only a three-tuple position (x, y, theta)
    return tuple(bests[0])

if __name__ == "__main__":
    pose = main()
    print pose
    # Send that pose to some other ROS node.
    # ...
