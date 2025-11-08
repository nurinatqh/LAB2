import streamlit as st
import random


POP_SIZE = 300
CHROM_LENGTH = 80
TARGET_ONES = 50
GENERATIONS = 50
MUTATION_RATE = 0.01


def fitness(individual):
    ones = sum(individual)
    if ones == TARGET_ONES:
        return 80
    else:
        return 80 - abs(ones - TARGET_ONES)


def create_population():
    return [[random.randint(0, 1) for _ in range(CHROM_LENGTH)] for _ in range(POP_SIZE)]


def selection(population):
    i1, i2 = random.sample(range(len(population)), 2)
    return population[i1] if fitness(population[i1]) > fitness(population[i2]) else population[i2]


def crossover(parent1, parent2):
    point = random.randint(1, CHROM_LENGTH - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2


def mutate(individual):
    for i in range(CHROM_LENGTH):
        if random.random() < MUTATION_RATE:
            individual[i] = 1 - individual[i]
    return individual

def run_ga():
    population = create_population()
    best_fitness_history = []
    best_ones_history = []

    for gen in range(GENERATIONS):
        new_pop = []

        while len(new_pop) < POP_SIZE:
            p1 = selection(population)
            p2 = selection(population)
            child1, child2 = crossover(p1, p2)

            new_pop.append(mutate(child1))
            if len(new_pop) < POP_SIZE:
                new_pop.append(mutate(child2))

        population = new_pop

        best = max(population, key=fitness)
        best_fitness_history.append(fitness(best))
        best_ones_history.append(sum(best))

    return best, best_fitness_history, best_ones_history


st.title("Genetic Algorithm: Bit Pattern Optimization")
st.write("This app evolves an 80-bit chromosome to reach exactly **50 ones** using a Genetic Algorithm.")

st.sidebar.header("GA Settings")
st.sidebar.write(f"Population Size: {POP_SIZE}")
st.sidebar.write(f"Chromosome Length: {CHROM_LENGTH}")
st.sidebar.write(f"Target Ones: {TARGET_ONES}")
st.sidebar.write(f"Generations: {GENERATIONS}")

if st.button("Run Genetic Algorithm"):
    with st.spinner("Running Genetic Algorithm... Please wait..."):
        best, fitness_history, ones_history = run_ga()

    st.success("Evolution Completed!")

    st.subheader("Best Individual Found")
    st.code("".join(map(str, best)))

    st.write("### Results Summary")
    st.write(f"- **Final Fitness:** {fitness(best)}")
    st.write(f"- **Number of Ones:** {sum(best)}")
    st.write(f"- **Chromosome Length:** {CHROM_LENGTH}")

    st.write("### Fitness Progress Across Generations")
    st.line_chart(fitness_history)

    st.write("### Number of Ones Across Generations")
    st.line_chart(ones_history)

else:
    st.info("Click the button above to start the evolution process.")