import json
import random
from multiprocessing import Pool, Process
from database import DB
from extrapolate_new import Extrapolate
from deap import creator, base, tools, algorithms


# SAT Constraints:
SMA_MAX = 6900
SMA_MIN = 7200
ECC_MAX = 0.01
ECC_MIN = 0.05
INC_MAX = 95
INC_MIN = 100
DRA_MAX = 0.15
DRA_MIN = 0.60
MAS_MAX = 1
MAS_MIN = 5

#proccess_1 = Process(target=qmt.go_on(), args=())
#proccess_1.start()


def evalPose(individual, target_value):
    """
    Evaluate the sattelite extrapolation results.

    Args:
            individual list (6 params)
            target_value float (years of orbit)

    Kwargs:
            None

    Returns:
            tuple (single value)
    """
    ex = Extrapolate("satgen.db")
    name = ex.prepare(individual)
    ex.extrapolate(name)
    years = ex.get_time_diff(name)
    #final_tuple = ex.generate_final_tuple(name, years)
    # ex.stela_config.db.insert_final_state(final_tuple)
    return (abs(years - target_value),)


def initSat(icls,
            smaMax,
            smaMin,
            eccMax,
            eccMin,
            draMin,
            draMax,
            incMax,
            incMin,
            masMax,
            masMin):
    """
    Initiate random satellite from given constraints.

    Args:
            icls (obj)
            smaMax (float) semiMajorAxis Max
            smaMin (float) semiMajorAxis Min
            eccMax (float) eccentricity Max
            eccMin (float) eccentricity Min
            draMax (float) dragArea Max
            draMin (float) dragArea Min
            incMax (float) inclination Max
            incMin (float) inclination Min
            masMax (float) mass Max
            masMin (float) mass Min

    Kwargs:
            None

    Return:
            icls (obj)
    """
    return icls([random.uniform(smaMax, smaMin),
                 random.uniform(eccMax, eccMin),
                 random.uniform(draMax, draMin),
                 random.uniform(incMax, incMin),
                 random.uniform(masMax, masMin)])

# Genetic Algorithm part

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)
toolbox = base.Toolbox()

pool = Pool()
toolbox.register("map", pool.map)

toolbox.register("individual",
                 initSat,
                 creator.Individual,
                 smaMax=SMA_MAX,
                 smaMin=SMA_MIN,
                 eccMax=ECC_MAX,
                 eccMin=ECC_MIN,
                 draMin=DRA_MAX,
                 draMax=DRA_MIN,
                 incMax=INC_MAX,
                 incMin=INC_MIN,
                 masMax=MAS_MAX,
                 masMin=MAS_MIN)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evalPose, target_value=25.0)
toolbox.register("mate", tools.cxTwoPoints)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1.0, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)


def main():
    # Create a population of 300 individuals
    population = toolbox.population(n=300)
    CXPB, MUTPB, NGEN = 0.6, 0.4, 50

    population, _ = algorithms.eaSimple(population, toolbox, cxpb=CXPB,
                                        mutpb=MUTPB, ngen=NGEN)

    # Find the best individual(s) in the resulting population
    bests = tools.selBest(population, k=1)

    # An individual is a complex object containing a fitness,
    return tuple(bests[0])

if __name__ == "__main__":
    pose = main()
    print pose
