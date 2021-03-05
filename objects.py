import random
from operator import attrgetter
############################################################################################################
# Common base class for all creatures.
############################################################################################################
class Creature:
    def __init__(self, long_neck, eagle_eye, speed, max_stamina, remaining_moves, strength, fitness, position):
        self.long_neck = long_neck                  # a float to represent a creatures neck length
        self.eagle_eye = eagle_eye                  # a float to indicate a creatures vision stat
        self.speed = speed                          # a float to determine a creatures speed (Movement order)
        self.max_stamina = max_stamina              # a float that determines a creatures stamina (How many tiles can be moved before the creature can no longer move)
        self.remaining_moves = remaining_moves      # a float that indicates how much stamina a creature has left
        self.strength = strength                    # a float to indicate a creatures strength
        self.fitness = fitness                      # a float to show how fit a specific instance of a creature is (intially set to 0), this is the amount of food they find in a generation.
        self.position = position                    # references a coord position, this is where the creature is currently positioned.
    #function to get position
    def return_positon(self): # returns a creatures current position
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
    def update_stam(self,new_stam):
        self.max_stamina = new_stam
        self.remaining_moves = int((new_stam*255))
    # function to update strength
    def update_str(self, new_str):
        self.strength = new_str
    # function to update fitness
    def update_fitness(self, new_fit):
        self.fitness = new_fit

    # function to determine the best move and then make the move
    def update_position(self, XL, YL, Stop, L_food):
        global can_eat
        can_eat = False
    #     Moves   : 0   1   2   3   4   5   6   7
        xpossible=[-1, -1,  0,  1,  1,  1,  0, -1]
        ypossible=[ 0, -1, -1, -1,  0,  1,  1,  1]
        fpossible=[False,False,False,False,False,False,False,False]
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

            is_food = L_food[potential_x, potential_y].food_type
            if is_food != 0:
                can_eat = self.can_eat_tile(L_food, potential_x, potential_y)
            if can_eat == True:
                fpossible[i] = True

        potential_moves = []
        # creating a list containing ints of all the valid moves
        for i in range(0,7):
            if fpossible[i] == True:
                potential_moves.append(i)
        # if the list of moves that contain food is empty then a direction is randomly selected and ate food is set to false
        if not potential_moves:
            direction = random.randint(0,7)
            ate_food_flag = False
        else:
            #randomly selecting a move from the list of potential moves
            direction = random.choice(potential_moves)
            ate_food_flag = True

    # Create new position
        new_pos_x = self.position[0] + xpossible[direction]
        new_pos_y = self.position[1] + ypossible[direction]
    # Stop at world edge
        if (Stop):
            if (new_pos_x < 0):     new_pos_x = 0
            if (new_pos_x >= XL):   new_pos_x = XL-1
            if (new_pos_y < 0):     new_pos_y = 0
            if (new_pos_y >= YL):   new_pos_y = YL-1
    # Else Wrap around world edges
        else:
            if (new_pos_x < 0):     new_pos_x = XL-1
            if (new_pos_x >= XL):   new_pos_x = 0
            if (new_pos_y < 0):     new_pos_y = YL-1
            if (new_pos_y >= YL):   new_pos_y = 0
    # Update Position
        self.position = (new_pos_x, new_pos_y)
        #L_food[new_pos_x, new_pos_y].update_food_type(0)
        if ate_food_flag:
            self.eat_food(L_food, new_pos_x, new_pos_y)

    # function to check the current tile for food, returns true if it contains any type of food that it can eat
    def can_eat_tile(self, L_food, x_coord, y_coord):
        type_of_current_tile = L_food[x_coord, y_coord].food_type
        if type_of_current_tile == 1:
            return(True)
        if type_of_current_tile == 2:
            return(self.long_neck)
        if type_of_current_tile == 3:
            return(not(self.long_neck))
        else:
            return(False)
    # function to eat the food at a tile passed to it and update the food array and creatures fitness
    def eat_food(self, L_food, x_coord,y_coord):
        self.fitness +=1
        L_food[x_coord, y_coord].update_food_type(0)


#common class for the food(The world is backed by XWorld*YWorld instances of these
class Food:
    def __init__(self, id, food_type):
        self.id = id # xy coords for the tile the food will be located on
        self.food_type = food_type # 0= no food 1= food on land 2= food in a tall tree 3= food in a hole
    #function to get food type
    def return_food_type(self):
        return(self.food_type)
    # function to update food type
    def update_food_type(self, new_food_type):
        self.food_type = new_food_type
    #function to return id ((x,y) coords)
    def return_id(self):
        return(self.id)
#  Class for the specific tiles that make up the world

#function to generate the food onto the world
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

def reset_food(all_coord_combos, L_food):
    for i in range(len(all_coord_combos)):
        p_holder = all_coord_combos[i]
        input_food = Food(p_holder, 0)
        L_food[p_holder[0], p_holder[1]] = input_food

# mutation function
def mutation(genome):
    for i in range(5):
        #roll a number to see if the stat will go up or down if rolled
        plus_minus = random.randint(0,1)
        # mut chance at 0.5%
        m_chance = random.randint(1,1000)
        if m_chance <= 1000:
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
                    genome.update_stam(new_val)
            # 1 = change str value
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

def crossover(copy_new_population, XW, YW):
    children = []
    for i in range(int(len(copy_new_population)/2)):
        r_range = len(copy_new_population) - 1
        p1_index = random.randint(0, r_range)
        p2_index = random.randint(0, r_range)
        while p1_index == p2_index:
            p2_index = random.randint(0, r_range)
        p1 = copy_new_population[p1_index]
        p2 = copy_new_population[p2_index]
    # selecting a crossover point
        c_point = random.randint(1,4)
        move_multi = float(255)
        for i in range(5):
            # 0-49 = no crossover 50-100 = crossover
            p1_or_2 = random.randint(0,100)
            # neck length
            if i == 0:
                if p1_or_2 >= 50:
                    c1_neck = p2.return_neck_type()
                    c2_neck = p1.return_neck_type()
                else:
                    c1_neck = p1.return_neck_type()
                    c2_neck = p2.return_neck_type()
            # vision
            if i == 1:
                if p1_or_2 >= 50:
                    c1_sight = p2.return_eagle_eye()
                    c2_sight = p1.return_eagle_eye()
                else:
                    c1_sight = p1.return_eagle_eye()
                    c2_sight = p2.return_eagle_eye()
            # speed
            if i == 2:
                if p1_or_2 >= 50:
                    c1_speed = p2.return_speed()
                    c2_speed = p1.return_speed()
                else:
                    c1_speed = p1.return_speed()
                    c2_speed = p2.return_speed()
            # stamina
            if i == 3:
                if p1_or_2 >= 50:
                    c1_stam = p2.return_max_stam()
                    c2_stam = p1.return_max_stam()
                else:
                    c1_stam = p1.return_max_stam()
                    c2_stam = p2.return_max_stam()
            # strength
            if i == 4:
                if p1_or_2 >= 50:
                    c1_str = p2.return_str()
                    c2_str = p1.return_str()
                else:
                    c1_str = p1.return_str()
                    c2_str = p2.return_str()
        c1 = Creature(c1_neck, c1_sight, c1_speed, c1_stam, (c1_stam*move_multi), c1_str, 0, (random.randint(0, XW - 1), random.randint(0, YW - 1)))
        c2 = Creature(c2_neck, c2_sight, c2_speed, c2_stam, (c2_stam * move_multi), c2_str, 0, (random.randint(0, XW - 1), random.randint(0, YW - 1)))
        c1 = mutation(c1)
        c2 = mutation(c2)
        children.append(c1)
        children.append(c2)
        del copy_new_population[p1_index]
        del copy_new_population[p2_index-1]
    return(children)

#gen algo to get a new pop
def genetic(Population, fittest_creature, XW, YW):
    new_population = []
    copy = []
    # sort the pop based on fitness
    Population.sort(key = attrgetter('fitness'), reverse=True)
    #check for new best
    if Population[0].return_fitness() > fittest_creature.return_fitness():
        fittest_creature = Population[0]
        print("I'm the fittest!")
        print("neck", fittest_creature.return_neck_type())
        print("sight", fittest_creature.return_eagle_eye())
        print("speed", fittest_creature.return_eagle_eye())
        print("stamina", fittest_creature.return_max_stam())
        print("strength", fittest_creature.return_str())
    cutoff = round(len(Population) / 2)
    # passing the top 50% solutions down to the next generation (They survived)
    for i in range(cutoff):
        new_population.append(Population[i])
        new_population[i].update_fitness(0)
    #performing crossover and mutation to get the last 50% of the population
    for i in range(len(new_population)):
        copy.append(new_population[i])
    children = crossover(copy, XW, YW)
    # convert genomes in children to creatures in new pop
    for i in range(len(children)):
        new_population.append(children[i])
    for i in range(len(new_population)):
        stam_val = new_population[i].return_max_stam()
        new_population[i].update_stam(stam_val)
    #replacing the old pop
    Population = new_population
    return(Population, fittest_creature)

def generate_creatures(num_of_creatures, XW, YW, Population):
    shortlist = []
    for i in range(num_of_creatures):
        neck_val = random.randint(1,10) / 10
        sight_val = random.randint(1,10) / 10
        speed_val = random.randint(1,10) / 10
        stam_val = random.randint(1,10) / 10
        str_val = random.randint(1,10) / 10
        shortlist.append(Creature(neck_val, sight_val, speed_val, stam_val, (stam_val*255), str_val, 0,(random.randint(0, XW - 1),random.randint(0, YW - 1))))
    for i in range(len(shortlist)):
        Population.append(shortlist[i])
    return Population

