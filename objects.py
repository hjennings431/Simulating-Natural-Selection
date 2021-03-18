import random
from operator import attrgetter

############################################################################################################
# Common base class for all creatures.
############################################################################################################
class Creature:
    def __init__(self, long_neck, eagle_eye, speed, max_stamina, remaining_moves, strength, fitness, position, can_move, food_ate):
        self.long_neck = long_neck                  # a float to represent a creatures neck length
        self.eagle_eye = eagle_eye                  # a float to indicate a creatures vision stat
        self.speed = speed                          # a float to determine a creatures speed (Movement order)
        self.max_stamina = max_stamina              # a float that determines a creatures stamina (How many tiles can be moved before the creature can no longer move)
        self.remaining_moves = remaining_moves      # a float that indicates how much stamina a creature has left
        self.strength = strength                    # a float to indicate a creatures strength
        self.fitness = fitness                      # an int to show how fit a specific instance of a creature is (intially set to 0), this is the amount of food they find in a generation.
        self.position = position                    # references a coord position, this is where the creature is currently positioned.
        self.can_move = can_move                     # bool that tells the movement function whether it can move
        self.food_ate = food_ate

    #function to get position
    def return_position(self): # returns a creatures current position
        return(self.position)
    #function to get fitness
    def return_fitness(self):
        return(self.fitness)
    # function to return neck type
    def return_neck_type(self):
        return(self.long_neck)
    # returns sight
    def return_eagle_eye(self):
        return(self.eagle_eye)
    # returns speed
    def return_speed(self):
        return(self.speed)
    #returns max stam
    def return_max_stam(self):
        return(self.max_stamina)
    # returns strength
    def return_str(self):
        return(self.strength)
    # returns remaining moves
    def return_remaining_moves(self):
        return(self.remaining_moves)
    #return food ate
    def return_food_ate(self):
        return(self.food_ate)
    # function to update neck
    def update_neck(self,new_neck):
        self.long_neck = new_neck
    # function to update sight
    def update_sight(self, new_sight):
        self.eagle_eye = new_sight
    # function to update speed
    def update_speed(self, new_speed):
        self.speed = new_speed
    # function to update stamina
    def update_stam(self,new_stam, TurnsPerGen):
        self.max_stamina = new_stam
        multiplier = (TurnsPerGen*2) - round((TurnsPerGen * 0.2))
        self.remaining_moves = int(new_stam * multiplier)
    # function to update strength
    def update_str(self, new_str):
        self.strength = new_str
    # function to update fitness
    def update_fitness(self, new_fit):
        if new_fit < 0:
            new_fit = 0
        self.fitness = new_fit
    # updates the remaining moves
    def update_remaining_moves(self, new_moves):
        self.remaining_moves = new_moves
    #update food ate
    def update_food_ate(self, new_val):
        self.food_ate = new_val
    # function to determine the best move and then make the move
    def update_position(self, XL, YL, Stop, L_food, L_hazards):
        potential_x = 0 ; potential_y = 0; direction = 0; ate_food_flag = False
        global can_eat
        can_eat = False
    #     Moves   : 0   1   2   3   4   5   6   7
        xpossible=[-1, -1,  0,  1,  1,  1,  0, -1]
        ypossible=[ 0, -1, -1, -1,  0,  1,  1,  1]
        fpossible=[False,False,False,False,False,False,False,False]
        print("my moves are: ", self.remaining_moves)
        if self.remaining_moves > 0:
        # Pick new move
            for i in range(0,7):
                potential_x = self.position[0] + xpossible[i]
                potential_y = self.position[1] + ypossible[i]
            # Stop at world edge
                if (Stop):
                    if (potential_x < 0):   potential_x = XL-1
                    if (potential_x >= XL): potential_x = 0
                    if (potential_y < 0):   potential_x = YL-1
                    if (potential_y >= YL): potential_y = 0
            # Else Wrap around world edges
                else:
                    if (potential_x < 0):     potential_x = XL - 1
                    if (potential_x >= XL):   potential_x = 0
                    if (potential_y < 0):     potential_y = YL - 1
                    if (potential_y >= YL):   potential_y = 0

            # creating a list containing ints of all the valid moves
                is_food = L_food[potential_x, potential_y].food_type
                if is_food != 0:
                    can_eat = self.can_eat_tile(L_food, potential_x, potential_y)
# *******************************************************************************************
                if can_eat > 0:
                    fpossible[i] = True

            potential_moves = []
        # creating a list containing ints of all the valid moves
            for i in range(0, 7):
                if fpossible[i] == True:
                    potential_moves.append(i)
            # if the list of moves that contain food is empty then a direction is randomly selected and ate food is set to false
            if not potential_moves:
                direction = random.randint(0, 7)
                ate_food_flag = False
            else:
                # randomly selecting a move from the list of potential moves
                direction = random.choice(potential_moves)
                ate_food_flag = True

        # Create new position
            new_pos_x = self.position[0] + xpossible[direction]
            new_pos_y = self.position[1] + ypossible[direction]

            # Stop at world edge
            if (Stop):
                if (new_pos_x < 0):     new_pos_x = 0
                if (new_pos_x >= XL):   new_pos_x = XL - 1
                if (new_pos_y < 0):     new_pos_y = 0
                if (new_pos_y >= YL):   new_pos_y = YL - 1
            # Else Wrap around world edges
            else:
                if (new_pos_x < 0):     new_pos_x = XL - 1
                if (new_pos_x >= XL):   new_pos_x = 0
                if (new_pos_y < 0):     new_pos_y = YL - 1
                if (new_pos_y >= YL):   new_pos_y = 0
            # Update Position
            self.position = (new_pos_x, new_pos_y)

            if ate_food_flag:
                self.food_ate += 1
                self.eat_food(L_food, new_pos_x, new_pos_y, can_eat)
            # Resolves hazards on new tile
            self.check_hazard(L_hazards, new_pos_x, new_pos_y)
            if self.speed <= 0.2:
                pass
            if self.speed >= 0.7:
                self.remaining_moves -=2
            else:
                self.remaining_moves -=1

            if self.remaining_moves <= 0:
                self.can_move = False

    # function to check current tile for hazards
    def check_hazard(self, L_hazards, x_coord, y_coord):
        hazard_type = L_hazards[x_coord, y_coord].hazard_type
        if hazard_type == 0:
            pass
        if hazard_type == 1: # Thorns
            if self.speed >= 0.7:
                self.fitness -= 1

        if hazard_type == 2: # Tar pits that affect creatures with higher stamina more
            if self.max_stamina >=0.7:
                self.fitness -= 1

        if hazard_type == 3: # Gas
            if self.eagle_eye >=0.7:
                self.fitness -= 1

        if hazard_type == 4: # Land Predators
            if self.strength >=0.7:
                self.fitness -= 1

# *******************************************************************************************
        if hazard_type == 5:  # Tree predators
            if self.long_neck >= 0.7:
                self.fitness -= ((self.long_neck - 0.7) / 0.3) * 4

# *******************************************************************************************
    # function to check the current tile for food, returns true if it contains any type of food that it can eat
    def can_eat_tile(self, L_food, x_coord, y_coord):
        type_of_current_tile = L_food[x_coord, y_coord].food_type
        neck_val = self.return_neck_type()
        if type_of_current_tile == 1:
            if neck_val < 0.5:
                return (1 - (neck_val - 0.5) / 0.5)
        if type_of_current_tile == 2:
            if neck_val >= 0.7:
                return ((neck_val - 0.7) / 0.3)
        if type_of_current_tile == 3:
            if 0.5 <= neck_val < 0.7:
                return ((neck_val - 0.5) / 0.2)
        return (0.0)

# *******************************************************************************************
    # function to eat the food at a tile passed to it and update the food array and creatures fitness
    def eat_food(self, L_food, x_coord, y_coord, food_weight):
        self.fitness += food_weight
        L_food[x_coord, y_coord].update_food_type(0)
############################################################################################################
# Common class for the food
############################################################################################################
class Food:
    def __init__(self, id, food_type):
        self.id = id # xy coords for the tile the food will be located on
        self.food_type = food_type # 0= no food 1= food on land 2= food in a tall tree 3= food in bush
    #function to get food type
    def return_food_type(self):
        return(self.food_type)
    # function to update food type
    def update_food_type(self, new_food_type):
        self.food_type = new_food_type
############################################################################################################
# Function to generate the food onto the world
############################################################################################################
def generate_food(all_coord_combos, food_pct, tall_food_pct, bush_food_pct, L_food):
# For all tiles
    for i in range(len(all_coord_combos)):
        food_type = 0
        has_food = random.randint(1,100)
    # Decide if the tile has food
        if (has_food <= food_pct) :
            food_type=1
        # See if it has tall food
            has_tallfood = random.randint(1,100)
            if (has_tallfood <= tall_food_pct) :
                food_type=2
        # See if it has bush food
            has_bushfood = random.randint(1,100)
            if (has_bushfood <= bush_food_pct) :
                food_type=3
    # Update the food
        p_holder = all_coord_combos[i]
        L_food[p_holder[0], p_holder[1]].update_food_type(food_type)
############################################################################################################
# Function to reset the food
############################################################################################################
def reset_food(all_coord_combos, L_food):
    for i in range(len(all_coord_combos)):
        p_holder = all_coord_combos[i]
        input_food = Food(p_holder, 0)
        L_food[p_holder[0], p_holder[1]] = input_food

############################################################################################################
# Common class for the hazards
############################################################################################################
class Hazards:
    def __init__(self, id, hazard_type):
        self.id = id # xy coords for the tile the food will be located on
        self.hazard_type = hazard_type
    #function to get the hazards
    def return_hazard(self):
        return(self.hazard_type)
    # function to update hazards
    def update_hazard(self, new_hazard_type):
        self.hazard_type = new_hazard_type
############################################################################################################
# Function to generate the set of hazards
############################################################################################################
def generate_hazards(all_coord_combos, hazard_pct, hazard_types,  L_hazards, hazard_toggles):
    ################### Thorns, Tar Pit, Gas, Predators, Tree predators ####################################
    potential_hazards = [False, False, False, False, False]
    hazard_index = []
    num_of_toggles = 0
    hazard_type = 0
    for i in range(5):
        if hazard_toggles[i].isChecked() == True:
            potential_hazards[i] == True
            num_of_toggles += 1
            hazard_index.append(i)
# For all tiles
    for i in range(len(all_coord_combos)):
        has_hazard = random.randint(1,100)
    # Decide if the tile has a hazard and what type it is
        if num_of_toggles == 0:
            pass
        else:
            hazard_type = 0
            if (has_hazard <= hazard_pct):
                hazard_type_temp = random.randint(0, (num_of_toggles-1))
                hazard_type = hazard_index[hazard_type_temp]
                hazard_type += 1
    # Update the food
        p_holder = all_coord_combos[i]
        L_hazards[p_holder[0], p_holder[1]].update_hazard(hazard_type)
############################################################################################################
# Function to reset all hazards
############################################################################################################
def reset_hazards(all_coord_combos, L_hazards):
    for i in range(len(all_coord_combos)):
        p_holder = all_coord_combos[i]
        input_hazard = Hazards(p_holder, 0)
        L_hazards[p_holder[0], p_holder[1]] = input_hazard
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
def crossover(copy_new_population, XW, YW, TurnsPerGen, Mut_chance):
    children = []
    for i in range(int(len(copy_new_population)/2)):
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
                        range_bot = int((p2.return_neck_type() *100))
                        range_top = int((p1.return_neck_type() *100))
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
                    if c1_stam >= 0.7:
                        if c1_speed >= 0.6:
                            c1_speed = ((c1_speed*100)-10) / 100
                    if c2_stam >= 0.7:
                        if c2_speed >= 0.6:
                            c2_speed = ((c2_speed*100)-10) / 100

                if p1_or_2 <= 25:
                    c1_speed = p1.return_speed()
                    c2_speed = p2.return_speed()
                    if c1_stam >= 0.7:
                        if c1_speed >= 0.6:
                            c1_speed = ((c1_speed*100)-10) / 100
                    if c2_stam >= 0.7:
                        if c2_speed >= 0.6:
                            c2_speed = ((c2_speed*100)-10) / 100
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
                    if c1_stam >= 0.7:
                        if c1_speed >= 0.6:
                            c1_speed = round(((c1_speed*100)-15) / 100)
                    if c2_stam >= 0.7:
                        if c2_speed >= 0.6:
                            c2_speed = round(((c2_speed*100)-15) / 100)

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

# function that mutates just the neck length (Only used if creatures are unable to reach any food at all.
def mutate_neck(Population, Mut_chance):
    m_roll = random.randint(1,100)
    if Mut_chance != 1:
        Mut_chance = int(Mut_chance/2)
    if m_roll <= Mut_chance:
        for i in range(len(Population)):
            plus_minus = random.randint(0,1)
            if plus_minus == 1:
                phold = Population[i].return_neck_type() * 100
                new_val = phold + 10
                if new_val > 100:
                    new_val = 100
                new_val /= 100
            else:
                phold = Population[i].return_neck_type() * 100
                new_val = phold - 10
                if new_val < 10:
                    new_val = 10
                new_val /= 100
            Population[i].update_neck(new_val)
    return (Population)
############################################################################################################
# Genetic Algorithm to get a new Population
############################################################################################################
def genetic(Population, NoOfBobs, fittest, XW, YW, TurnsPerGen, Mut_chance):
    stop = False
    new_population = []
    copy = []
    copy2 = []
    # sort the pop based on fitness
    Population.sort(key = attrgetter('fitness'), reverse=True)
    #check for new best
    if Population[0].return_fitness() > fittest.return_fitness():
        fittest = Creature(Population[0].return_neck_type(), Population[0].return_eagle_eye(), Population[0].return_speed(), Population[0].return_max_stam(), 0, Population[0].return_str(), Population[0].return_fitness(), (0,0), False, 0)
    cutoff = round(NoOfBobs / 2)
    if NoOfBobs > len(Population):
        creatures_to_add = NoOfBobs - len(Population)
        Population = generate_creatures(creatures_to_add, XW, YW, Population, False, TurnsPerGen, False)
    # passing the top 50% solutions down to the next generation (They survived)
    for i in range(cutoff):
        new_population.append(Population[i])
        # mutate the parents if they have a low fitness to avoid stagnation
    for i in range(len(new_population)):
        # if a creature in the top 50% gets no food, mutates their neck so that we can push the pop in a direction that will provide a vioable solution
        if new_population[i].return_food_ate() == 0:
            new_population = mutate_neck(new_population, Mut_chance)
    # performing crossover and mutation to get the last 50% of the population
    for i in range(len(new_population)):
        copy.append(new_population[i])
    children = crossover(copy, XW, YW,TurnsPerGen, Mut_chance)
    # convert genomes in children to creatures in new pop
    for i in range(len(children)):
        new_population.append(children[i])
    for i in range(len(new_population)):
        stam_val = new_population[i].return_max_stam()
        new_population[i].update_stam(stam_val, TurnsPerGen)
    #replacing the old pop
    Population = new_population
    return(Population, fittest, stop)
############################################################################################################
# Function to generate a set of random creatures
############################################################################################################
def generate_creatures(num_of_creatures, XW, YW, Population, reset, TurnsPerGen, Juiced):
    shortlist = []
    for i in range(num_of_creatures): # standard creature weights
        #### CREATURE INTIIAL STATS CAN BE WEIGHTED HERE ####
        #neck
        neck_roll = random.randint(1,100)
        if neck_roll <=40:
            neck_val = random.randint(1,3) / 10
        if neck_roll >= 95:
            neck_val = random.randint(7,10) / 10
        else:
            neck_val = random.randint(4,6) / 10

        #sight
        sight_roll = random.randint(1, 100)
        if sight_roll <= 40:
            sight_val = random.randint(1, 3) / 10
        if sight_roll >= 95:
            sight_val = random.randint(7, 10) / 10
        else:
            sight_val = random.randint(4, 6) / 10

        #stam
        stam_roll = random.randint(1,100)
        if stam_roll <=40:
            stam_val = random.randint(1,3) / 10
        if stam_roll >= 95:
            stam_val = random.randint(7,10) / 10
        else:
            stam_val = random.randint(4,6) / 10

        if stam_val >= 0.7:
            max_speed_roll = 65
        else:
            max_speed_roll = 100

        # speed
        speed_roll = random.randint(1,max_speed_roll)
        if speed_roll <=40:
            speed_val = random.randint(1,3) / 10
        if speed_roll >= 95:
            speed_val = random.randint(7,10) / 10
        else:
            speed_val = random.randint(4,6) / 10

        #str
        str_roll = random.randint(1,100)
        if str_roll <=40:
            str_val = random.randint(1,3) / 10
        if str_roll >= 95:
            str_val = random.randint(7,10) / 10
        else:
            str_val = random.randint(4,6) / 10

        shortlist.append(Creature(neck_val, sight_val, speed_val, stam_val, 0, str_val, 0, (random.randint(0, XW - 1),random.randint(0, YW - 1)), True, 0))
    if reset == True:
        Population = []
    for i in range(len(shortlist)):
        shortlist[i].update_stam(shortlist[i].return_max_stam(), TurnsPerGen)
        Population.append(shortlist[i])
    return Population
############################################################################################################
# Get average neck length
############################################################################################################
def get_average_neck(Population):
    avg = 0
    for i in range(len(Population)):
        avg += Population[i].return_neck_type()
    avg /= len(Population)
    return(avg)
############################################################################################################
# Get average speed
############################################################################################################
def get_average_speed(Population):
    avg = 0
    for i in range(len(Population)):
        avg += Population[i].return_speed()
    avg /= len(Population)
    return(avg)
############################################################################################################
# Get average strength
############################################################################################################
def get_average_str(Population):
    avg = 0
    for i in range(len(Population)):
        avg += Population[i].return_str()
    avg /= len(Population)
    return(avg)
############################################################################################################
# Get average stamina
############################################################################################################
def get_average_stam(Population):
    avg = 0
    for i in range(len(Population)):
        avg += Population[i].return_max_stam()
    avg /= len(Population)
    return(avg)
############################################################################################################
# Get fitness
############################################################################################################
def get_average_fitness(Population):
    avg = 0
    for i in range(len(Population)):
        avg += Population[i].return_fitness()
    avg /= len(Population)
    return(avg)
############################################################################################################
# Get average vision
############################################################################################################
def get_average_vision(Population):
    avg = 0
    for i in range(len(Population)):
        avg += Population[i].return_eagle_eye()
    avg /= len(Population)
    return(avg)
############################################################################################################
# Fight Club; finds all the fights when given a pop
############################################################################################################
def fight_club(Population):
# Go through the list of creatures
    for i in range(len(Population)-1):
    # Get the position
        first_creature_pos = Population[i].position
    # Clear the fight card and append with current creature position
        fight_card=[]
        fight_card.append(i)
    # Go through the remaining population and add to fight if creature on same square
        for j in range(i+1, len(Population)):
            if (first_creature_pos[0] == Population[j].position[0] and first_creature_pos[1] == Population[j].position[1]):
                fight_card.append(j)
    # Resolve the fight card
        if (len(fight_card)>1):
            Population = creature_fight(Population, fight_card)

    return(Population)
#######################################################################################

def creature_fight(Population, fight_card):
    # get all the values for the fighting creatures
    creature1_str = round((Population[fight_card[0]].return_str()*100))
    creature2_str = round((Population[fight_card[1]].return_str()*100))
    c1_fit = Population[fight_card[0]].return_fitness()
    c2_fit = Population[fight_card[1]].return_fitness()
    c1_moves = Population[fight_card[0]].return_remaining_moves()
    c2_moves = Population[fight_card[1]].return_remaining_moves()
    # get the total roll and roll for a probability that determines the winner
    total = creature1_str + creature2_str
    roll = random.randint(1, total)
    # c1 winner
    if roll <= creature1_str:
        # winner +1 fit -2 moves
        c1_fit += 1; c1_moves -= 2; c2_fit -= 1; c2_moves -= 1
        Population[fight_card[0]].update_fitness(c1_fit)
        Population[fight_card[0]].update_remaining_moves(c1_moves)
        #loser -1 fit - 1 move
        Population[fight_card[1]].update_fitness(c2_fit)
        Population[fight_card[1]].update_remaining_moves(c2_moves)
    #c2 winner
    else:
        c2_fit += 1; c2_moves -= 2; c1_fit -= 1; c1_moves -= 1
        # winner +1 fit -2 moves
        Population[fight_card[1]].update_fitness(c2_fit)
        Population[fight_card[1]].update_remaining_moves(c2_moves)
        #loser -1 fit - 1 move
        Population[fight_card[0]].update_fitness(c1_fit)
        Population[fight_card[0]].update_remaining_moves(c1_moves)

    return(Population)
