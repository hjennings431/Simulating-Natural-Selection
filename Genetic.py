import random
from operator import attrgetter
from Objects import *
random.seed(10)

############################################################################################################
# Mutation function
############################################################################################################
def mutation(genome, TurnsPerGen, Mut_chance):
    for i in range(5):
        #roll a number to see if the stat will go up or down if rolled
        plus_minus = random.randint(0,1)
        # roll mutation
        m_roll = random.randint(1,100)
        if m_roll <= Mut_chance:
            # 0 = change neck value
            if i == 0:
                if plus_minus == 1:
                    phold = genome.return_neck_type()*100
                    new_val = phold + 10
                    if new_val > 100:
                        new_val = 100
                    new_val /= 100
                else:
                    phold = genome.return_neck_type()*100
                    new_val = phold - 10
                    if new_val < 10:
                        new_val = 10
                    new_val /= 100
                genome.update_neck(new_val)

            # 1 = change eagle sight value
            if i == 1:
                if plus_minus == 1:
                    phold = genome.return_eagle_eye()*100
                    new_val = phold + 10
                    if new_val > 100:
                        new_val = 100
                    new_val /= 100
                else:
                    phold = genome.return_eagle_eye()*100
                    new_val = phold - 10
                    if new_val < 10:
                        new_val = 10
                    new_val /= 100
                genome.update_sight(new_val)

            # 2 = change speed value
            if i == 2:
                if plus_minus == 1:
                    phold = genome.return_speed()*100
                    new_val = phold + 10
                    if new_val > 100:
                        new_val = 100
                    new_val /= 100
                else:
                    phold = genome.return_speed()*100
                    new_val = phold - 10
                    if new_val < 10:
                        new_val = 10
                    new_val /= 100
                genome.update_speed(new_val)

            # 3 = change stam value
            if i == 3:
                if plus_minus == 1:
                    phold = genome.return_max_stam()*100
                    new_val = phold + 10
                    if new_val > 100:
                        new_val = 100
                    new_val /= 100
                else:
                    phold = genome.return_speed()*100
                    new_val = phold - 10
                    if new_val < 10:
                        new_val = 10
                    new_val /= 100
                genome.update_stam(new_val, TurnsPerGen)
            # 4 = change str value
            if i == 4:
                if plus_minus == 1:
                    phold = genome.return_str()*100
                    new_val = phold + 10
                    if new_val > 100:
                        new_val = 100
                    new_val /= 100
                else:
                    phold = genome.return_speed()*100
                    new_val = phold - 10
                    if new_val < 10:
                        new_val = 10
                    new_val /= 100
                genome.update_str(new_val)
    # return  the mutated 'genome'
    return(genome)
############################################################################################################
# CrossOver function
############################################################################################################
def crossover(copy_new_population, XW, YW, TurnsPerGen, Mut_chance, NoOfBobs, len_pop):
    children = []
    temp = len(copy_new_population)
    print(len(copy_new_population))
    iter = temp / 2
    iter = int(iter)
    for i in range(iter):
        r_range = len(copy_new_population) - 1
        p1_index = random.randint(0, r_range)
        p2_index = random.randint(0, r_range)
        while p1_index == p2_index:
            p2_index = random.randint(0, r_range)
        p1 = copy_new_population[p1_index]
        p2 = copy_new_population[p2_index]
        # iterating through for each stat
        for i in range(5):
            # 0-25 = crossover directly 26-49 = mix of parents values 75-100 = crossover directly
            p1_or_2 = random.randint(0,100)
            # neck length
            if i == 0:
                if p1_or_2 >= 75:
                    c1_neck = p2.return_neck_type()
                    c2_neck = p1.return_neck_type()
                if p1_or_2 <= 25:
                    c1_neck = p1.return_neck_type()
                    c2_neck = p2.return_neck_type()
                else:
                    if p1.return_neck_type() <= p2.return_neck_type():
                        range_bot = int((p1.return_neck_type() * 100))
                        range_top = int((p2.return_neck_type() * 100))
                    else:
                        range_bot = int((p2.return_neck_type() * 100))
                        range_top = int((p1.return_neck_type() * 100))
                    c1_neck = random.randint(range_bot, range_top)
                    c2_neck = random.randint(range_bot, range_top)
                    c1_neck = round((c1_neck / 100), 2)
                    c2_neck = round((c2_neck / 100), 2)
            # vision
            if i == 1:
                if p1_or_2 >= 75:
                    c1_sight = p2.return_eagle_eye()
                    c2_sight = p1.return_eagle_eye()
                if p1_or_2 <= 25:
                    c1_sight = p1.return_eagle_eye()
                    c2_sight = p2.return_eagle_eye()
                else:
                    if p1.return_eagle_eye() <= p2.return_eagle_eye():
                        range_bot = int((p1.return_eagle_eye() * 100))
                        range_top = int((p2.return_eagle_eye() * 100))
                    else:
                        range_bot = int((p2.return_eagle_eye() * 100))
                        range_top = int((p1.return_eagle_eye() * 100))
                    c1_sight = random.randint(range_bot, range_top)
                    c2_sight = random.randint(range_bot, range_top)
                    c1_sight = round((c1_sight / 100), 2)
                    c2_sight = round((c2_sight / 100), 2)
            #stamina
            if i == 2:
                if p1_or_2 >= 75:
                    c1_stam = p2.return_max_stam()
                    c2_stam = p1.return_max_stam()
                if p1_or_2 <= 25:
                    c1_stam = p1.return_max_stam()
                    c2_stam = p2.return_max_stam()
                else:
                    if p1.return_max_stam() <= p2.return_max_stam():
                        range_bot = int((p1.return_max_stam() * 100))
                        range_top = int((p2.return_max_stam() * 100))
                    else:
                        range_bot = int((p2.return_max_stam() * 100))
                        range_top = int((p1.return_max_stam() * 100))
                    c1_stam = random.randint(range_bot, range_top)
                    c2_stam = random.randint(range_bot, range_top)
                    c1_stam = round((c1_stam / 100), 2)
                    c2_stam = round((c2_stam / 100), 2)
            # speed
            if i == 3:
                if p1_or_2 >= 75:
                    c1_speed = p2.return_speed()
                    c2_speed = p1.return_speed()

                if p1_or_2 <= 25:
                    c1_speed = p1.return_speed()
                    c2_speed = p2.return_speed()

                else:
                    if p1.return_speed() <= p2.return_speed():
                        range_bot = int((p1.return_speed() * 100))
                        range_top = int((p2.return_speed() * 100))
                    else:
                        range_bot = int((p2.return_speed() * 100))
                        range_top = int((p1.return_speed() * 100))

                    c1_speed = random.randint(range_bot, range_top)
                    c2_speed = random.randint(range_bot, range_top)
                    c1_speed = round((c1_speed / 100), 2)
                    c2_speed = round((c2_speed / 100), 2)
            # strength
            if i == 4:
                if p1_or_2 >= 75:
                    c1_str = p2.return_str()
                    c2_str = p1.return_str()
                if p1_or_2 <=25:
                    c1_str = p1.return_str()
                    c2_str = p2.return_str()
                else:
                    if p1.return_str() <= p2.return_str():
                        range_bot = int((p1.return_str() * 100))
                        range_top = int((p2.return_str() * 100))
                    else:
                        range_bot = int((p2.return_str() * 100))
                        range_top = int((p1.return_str() * 100))
                    c1_str = random.randint(range_bot, range_top)
                    c2_str = random.randint(range_bot, range_top)
                    c1_str = round((c1_str / 100), 2)
                    c2_str = round((c2_str / 100), 2)

        c1 = Creature(c1_neck, c1_sight, c1_speed, c1_stam, c1_stam, c1_str, 0, (random.randint(0, XW - 1), random.randint(0, YW - 1)), True, 0)
        c2 = Creature(c2_neck, c2_sight, c2_speed, c2_stam, c2_stam, c2_str, 0, (random.randint(0, XW - 1), random.randint(0, YW - 1)), True, 0)
        c1 = mutation(c1, TurnsPerGen, Mut_chance)
        c2 = mutation(c2, TurnsPerGen, Mut_chance)
        c1.update_stam(c1.return_max_stam(), TurnsPerGen)
        c2.update_stam(c2.return_max_stam(), TurnsPerGen)
        children.append(c1)
        children.append(c2)
        del copy_new_population[p1_index]
        del copy_new_population[p2_index-1]
    return(children)
# tournament selection: picks 2 random solutions and returns the best one to parents and removes it from future selections
def selection(copy, cutoff):
    parents = []
    t_size = 5 # amount of participants in each tourney
    cutoff *= 4
    for i in range(cutoff):
        tourney_participants = []
        tourney_indexes = []
        length = (len(copy) - 1)
        for j in range(1,t_size):
            index = random.randint(0,length) # random gen indexes and check for dupes
            while index in tourney_indexes:
                index = random.randint(0, length)
            tourney_participants.append(copy[index])
        tourney_participants.sort(key=attrgetter('fitness'), reverse=True)
        parents.append(tourney_participants[0])
    return(parents)
############################################################################################################
# Genetic Algorithm to get a new Population
############################################################################################################
def genetic(Population, NoOfBobs, fittest, XW, YW, TurnsPerGen, Mut_chance, max_divest):
    new_population = []
    copy2 = []
    parents = []
    copy_for_selection = []
    # sort the pop based on fitness
    Population.sort(key = attrgetter('fitness'), reverse=True)
    #check for new best
    if Population[0].return_fitness() > fittest.return_fitness():
        fittest = Creature(Population[0].return_neck_type(), Population[0].return_eagle_eye(), Population[0].return_speed(), Population[0].return_max_stam(), 0, Population[0].return_str(), Population[0].return_fitness(), (0,0), False, 0)
    cutoff = round(NoOfBobs / 5)
    if NoOfBobs > len(Population):
        creatures_to_add = NoOfBobs - len(Population)
        Population = generate_creatures(creatures_to_add, XW, YW, Population, False, TurnsPerGen, False, max_divest)
    # using elitist selection and passing the top 50% solutions down to the next generation (They survived)
    for i in range(cutoff):
        new_population.append(Population[i])
    # Using tournament selection to get parents
    copy_for_selection = Population
    parents = selection(copy_for_selection, cutoff)
    # mutate the parents if they have eaten no food to avoid stagnation
    for i in range(len(new_population)):
        # if a creature in the top 50% gets no food, mutates their neck so that we can push the pop in a direction that will provide a vioable solution
        if new_population[i].return_food_ate() == 0:
            new_population = mutate_neck(new_population, Mut_chance)
    # performing crossover and mutation to get the last 50% of the population
    len_pop = len(Population)
    children = crossover(parents, XW, YW,TurnsPerGen, Mut_chance, NoOfBobs, len_pop)
    # convert genomes in children to creatures in new pop
    for i in range(len(children)):
        new_population.append(children[i])
    for i in range(len(new_population)):
        stam_val = new_population[i].return_max_stam()
        new_population[i].update_stam(stam_val, TurnsPerGen)
    #replacing the old pop
    Population = new_population
    for i in range(len(Population)):
        Population[i].balance_stats(max_divest, TurnsPerGen)
    return(Population, fittest)


############################################################################################################
# Function to mutate neck types if creatures are getting unable to reach any food
############################################################################################################
def mutate_neck(Population, Mut_chance):
    m_roll = random.randint(1,100)
    if Mut_chance != 1:
        Mut_chance = int(Mut_chance/2)
    if m_roll <= Mut_chance:
        for i in range(len(Population)):
            plus_minus = random.randint(0,1)
            if plus_minus == 1:
                phold = Population[i].return_neck_type() * 100
                new_val = phold + 5
                if new_val > 100:
                    new_val = 100
                new_val /= 100
            else:
                phold = Population[i].return_neck_type() * 100
                new_val = phold - 5
                if new_val < 10:
                    new_val = 10
                new_val /= 100
            Population[i].update_neck(new_val)
    return (Population)
