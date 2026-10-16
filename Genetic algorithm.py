
subjects = ["Java", "DBMS", "AI"]


population = [
    ["Java", "Java", "AI"],
    ["DBMS", "Java", "AI"],
    ["AI", "DBMS", "Java"],
    ["Java", "DBMS", "AI"]
]


def fitness(chromosome):
    score = 0
    for subject in subjects:
        if chromosome.count(subject) == 1:
            score += 1
    return score


def repair(child):
    missing = [s for s in subjects if s not in child]
    seen = []

    for i in range(len(child)):
        if child[i] in seen:
            child[i] = missing.pop(0)
        else:
            seen.append(child[i])

    return child


for generation in range(5):
    population.sort(key=fitness, reverse=True)

    print("Generation:", generation + 1)

    for timetable in population:
        print(timetable, "Fitness:", fitness(timetable))


    if fitness(population[0]) == len(subjects):
        break

    parent1 = population[0][:]
    parent2 = population[1][:]

 
    child = parent1[:2] + parent2[2:]
    child = repair(child)

  
    child[0], child[2] = child[2], child[0]

   
    population[-1] = child

 
population.sort(key=fitness, reverse=True)
best = population[0]

print("\nFinal Timetable")
for time, subject in zip(
    ["9 AM", "10 AM", "11 AM"], best
):
    print(time, "-", subject)

print("Fitness:", fitness(best), "/", len(subjects))
