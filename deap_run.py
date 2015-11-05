import json
import numpy
import random
import argparse
from multiprocessing import Pool, Process
from database import DB
from extrapolate_new import Extrapolate
from deap import creator, base, tools, algorithms
from scoop import futures

parser = argparse.ArgumentParser(description='Deap Run, Runs the ga for the given population.')
parser.add_argument('-a','--sma', nargs=2, help="Semi Major axix")
parser.add_argument('-e','--ecc', nargs=2, help="Eccentricity")
parser.add_argument('-i','--inc', nargs=2, help="Inclination")
parser.add_argument('-m','--mas', nargs=2, help="Mass")
parser.add_argument('-d','--dra', nargs=2, help="Drag Area")
parser.add_argument('-n','--num', help="Number")
# SAT Constraints:
options=parser.parse_args()
options_var=vars(options)
SMA_MAX = float(options_var["sma"][1])
SMA_MIN = float(options_var["sma"][0])
ECC_MAX = float(options_var["ecc"][1])
ECC_MIN = float(options_var["ecc"][0])
INC_MAX = float(options_var["inc"][1])
INC_MIN = float(options_var["inc"][0])
DRA_MAX = float(options_var["dra"][1])
DRA_MIN = float(options_var["dra"][0])
MAS_MAX = float(options_var["mas"][1])
MAS_MIN = float(options_var["mas"][0])
ARG_MIN = 0
ARG_MAX = 0
MEA_MIN = 0
MEA_MAX = 0
RAA_MIN = 0
RAA_MAX = 0
#ARG_ARR = [0, 45, 90, 135, 180, 225, 270, 315]
#MEA_ARR = [0, 45, 90, 135, 180, 225, 270, 315]
#RAA_ARR = [0, 45, 90, 135, 180, 225, 270, 315]
ARG_ARR = [0]
MEA_ARR = [0]
RAA_ARR = [0]
TARGET = 100.0/float(options_var["num"])

if(float(options_var["num"]==4)):
  NGEN = 20
else:
  NGEN = 10

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
    final_tuple = ex.generate_final_tuple(name, years)
    ex.stela_config.db.insert_final_state(final_tuple)
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
            masMin,
	    argMax,
            argMin,
	    meaMax,
	    meaMin,
	    raaMax,
	    raaMin,
            argArr,
	    meaArr,
            raaArr):
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
	    argMax (float) argofPerigee Max
            argMin (float) argofPerigee Min
            meaMax (float) meanAnomaly Max
            meaMin (flaot) meanAnomaly Min
	    raaMax (float) raan Max
	    raaMin (float) raan Min
	    argArr (float) argofPerigee Array
            meaArr (float) meanAnomaly Array
            raaArr (float) raan Array

    Kwargs:
            None

    Return:
            icls (obj)
    """
    return icls([random.uniform(smaMax, smaMin),
                 random.uniform(eccMax, eccMin),
                 random.uniform(draMax, draMin),
                 random.uniform(incMax, incMin),
                 random.uniform(masMax, masMin),
#                random.uniform(argMax, argMin),
#		 random.uniform(meaMax, meaMin),
#		 random.uniform(raaMax, raaMin)]
		 random.choice(argArr),
                 random.choice(meaArr),
		 random.choice(raaArr)])

# Genetic Algorithm part

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)
toolbox = base.Toolbox()


#toolbox.register("map", futures.map)
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
                 masMin=MAS_MIN,
		 argMax=ARG_MAX,
		 argMin=ARG_MIN,
		 meaMax=MEA_MAX,
		 meaMin=MEA_MIN,
		 raaMax=RAA_MAX,
		 raaMin=RAA_MIN,
	         argArr=ARG_ARR,
	         meaArr=MEA_ARR,
		 raaArr=RAA_ARR)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evalPose, target_value=TARGET)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1.0, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)
#toolbox.register("map", futures.map)

def main():
    random.seed(64)

    pool = Pool(processes=1)
    toolbox.register("map", pool.map)
    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=15,
                        stats=stats, halloffame=hof)
    return pop, stats, hof

if __name__ == "__main__":
    pop, stats, hof = main()
    print pop, stats, hof
