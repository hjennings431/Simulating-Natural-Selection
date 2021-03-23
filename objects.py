import random
random.seed(10)
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
        self.can_move = can_move                    # bool that tells the movement function whether it can move
        self.food_ate = food_ate                    # references the amount of food a creature has eaten, used to determine neck growth/decline

    #function to get a creatures current position
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
        multiplier = round((TurnsPerGen))
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

    def balance_stats(self, max_divest, TurnsPerGen):
        total = self.strength + self.speed + self.max_stamina

        if total > max_divest:
            diff = (total*100) - (max_divest * 100); diff = round(diff/3)
            new_str = (self.strength*100) - diff; new_str = round(new_str/ 100, 2)
            new_speed = (self.speed * 100) - diff; new_speed = round(new_speed / 100, 2)
            new_stamina = (self.max_stamina * 100) - diff; new_stamina = round(new_stamina / 100, 2)
            total = new_str + new_stamina + new_speed
            self.update_str(new_str)
            self.update_stam(new_stamina, TurnsPerGen)
            self.update_speed(new_speed)

############################################################################################################
# function to determine a creatures move and update its position as well as resolve all hazards and food
############################################################################################################
    def update_position(self, XL, YL, L_food, L_hazards):
        potential_x = 0 ; potential_y = 0; direction = 0; ate_food_flag = False
        global can_eat
        can_eat = False
    #     Moves   : 0   1   2   3   4   5   6   7
        xpossible=[-1, -1,  0,  1,  1,  1,  0, -1]
        ypossible=[ 0, -1, -1, -1,  0,  1,  1,  1]
        fpossible=[False, False, False, False, False, False, False, False]

        if self.remaining_moves > 0:
        # Pick new move
            for i in range(0,7):
                potential_x = self.position[0] + xpossible[i]
                potential_y = self.position[1] + ypossible[i]
                potential_x, potential_y = wrap_edge(potential_x, potential_y, XL, YL)

            # creating a list containing ints of all the valid moves
                is_food = L_food[potential_x, potential_y].food_type
                if is_food != 0:
                    can_eat = self.can_eat_tile(L_food, potential_x, potential_y)
                if can_eat > 0:
                    fpossible[i] = True

            potential_moves = []
        # creating a list containing ints of all the valid moves
            for i in range(0, 7):
                if fpossible[i] == True:
                    potential_moves.append(i)
            # if the list of moves that contain food is empty then a direction is randomly selected and ate food is set to false
            if not potential_moves:
                ate_food_flag = False
                direction = random.randint(0, 7)
                if self.eagle_eye >= 0.6:
                    not_food = True
                    f_totals = self.eagle_scan(L_food, XL, YL)
                    for i in range(0, 7):
                        if f_totals[i] != 0:
                            not_food = False
                    if not not_food:
                        direction = f_totals.index(max(f_totals))
                    if not_food:
                        direction = random.randint(0,7)
                    self.remaining_moves -= round(4-(self.eagle_eye*2))
                    if self.remaining_moves < 0:
                        self.remaining_moves = 0
                        self.can_move = False
            else:
                direction = random.choice(potential_moves)
                ate_food_flag = True

                # randomly selecting a move from the list of potential moves

            # Create new position
            new_pos_x = self.position[0] + xpossible[direction]
            new_pos_y = self.position[1] + ypossible[direction]
            # Stop at world edge
            new_pos_x, new_pos_y = wrap_edge(new_pos_x, new_pos_y, XL, YL)
            # Update Position
            self.position = (new_pos_x, new_pos_y)

            if ate_food_flag:
                self.food_ate += 1
                self.eat_food(L_food, new_pos_x, new_pos_y, can_eat)
            # Resolves hazards on new tile
            self.check_hazard(L_hazards, new_pos_x, new_pos_y)
            if self.speed >= 0.7:
                self.remaining_moves -=1
            else:
                self.remaining_moves -=1

            if self.remaining_moves <= 0:
                self.can_move = False

############################################################################################################
# function to scan all adjacent tiles to a creatures current adjacent tiles
############################################################################################################
    def eagle_scan(self, L_food, XW, YW):
        global can_eat
        xpossible= [-1, -1,  0,  1,  1,  1,  0, -1]
        ypossible= [ 0, -1, -1, -1,  0,  1,  1,  1]
        f_totals = []
        # iterate for all 8 possible moves and all 8 possible moves from them
        for i in range(0,7):
            total = 0
            input_x = self.position[0] + xpossible[i]
            input_y = self.position[1] + ypossible[i]
            for j in range(0, 7):
                possible_x = input_x + xpossible[j]
                possible_y = input_y + ypossible[j]
                possible_x, possible_y = wrap_edge(possible_x, possible_y, XW, YW)
                is_food = L_food[possible_x, possible_y].food_type
                # check for food and update totals if neccessary
                if is_food != 0:
                    can_eat = self.can_eat_tile(L_food, possible_x, possible_y)
                if can_eat > 0:
                    total += 1
            f_totals.append(total)
        # return the totals so that a move can be determined
        return(f_totals)

############################################################################################################
# function to check the current tile for hazards and resolve them proportionally
############################################################################################################
    def check_hazard(self, L_hazards, x_coord, y_coord):
        hazard_type = L_hazards[x_coord, y_coord].hazard_type
        if hazard_type == 0:
            pass
        if hazard_type == 1: # Thorns
            if self.speed >= 0.7:
                self.fitness -= ((self.speed - 0.7) / 0.3) * 4

        if hazard_type == 2: # Tar pits that affect creatures with higher stamina more
            if self.max_stamina >=0.7:
                self.fitness -= ((self.max_stamina - 0.7) / 0.3) * 4

        if hazard_type == 3: # Gas
            if self.eagle_eye >=0.7:
                self.fitness -= ((self.eagle_eye - 0.7) / 0.3) * 4

        if hazard_type == 4: # Land Predators
            if self.strength >=0.7:
                self.fitness -= ((self.strength - 0.7) / 0.3) * 4

        if hazard_type == 5:  # Tree predators
            if self.long_neck >= 0.7:
                self.fitness -= ((self.long_neck - 0.7) / 0.3) * 4

        if hazard_type == 6: # Snakes
            if self.long_neck <= 0.5:
                self.fitness -= ((0.5 - self.long_neck) / 0.3) * 4

############################################################################################################
# function to check the current tile for food, returns an int based on sustinence creature would gain
############################################################################################################
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
    ################### Thorns, Tar Pit, Gas, Predators, Tree predators Snakes #############################
    potential_hazards = [False, False, False, False, False, False]
    hazard_index = []
    num_of_toggles = 0
    hazard_type = 0
    for i in range(6):
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
# function to check if a given coord is outside the world and wrap back around if it is
############################################################################################################
    def wrap_edge(possible_x, possible_y, XW, YW):
        if (possible_x < 0):     possible_x = XW - 1
        if (possible_x >= XW):   possible_x = 0
        if (possible_y < 0):     possible_y = YW - 1
        if (possible_y >= YW):   possible_y = 0

############################################################################################################
# Function to generate a set of random creatures
############################################################################################################
def generate_creatures(num_of_creatures, XW, YW, Population, reset, TurnsPerGen, Juiced, max_divest):
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


        # speed
        speed_roll = random.randint(1,100)
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
    for i in range(len(Population)):
        Population[i].balance_stats(max_divest, TurnsPerGen)
    return Population

def wrap_edge(possible_x, possible_y, XW, YW):
    if (possible_x < 0):     possible_x = XW - 1
    if (possible_x >= XW):   possible_x = 0
    if (possible_y < 0):     possible_y = YW - 1
    if (possible_y >= YW):   possible_y = 0

    return(possible_x, possible_y)
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
############################################################################################################
# Function to resolves the fights on a given fight card
############################################################################################################
def creature_fight(Population, fight_card):
    # get all the values for the fighting creatures#
    if Population[fight_card[0]].can_move and Population[fight_card[1]].can_move:
        c_mod = 0
        creature1_str = round((Population[fight_card[0]].return_str()*100))
        creature2_str = round((Population[fight_card[1]].return_str()*100))
        c1_fit = Population[fight_card[0]].return_fitness()
        c2_fit = Population[fight_card[1]].return_fitness()
        c1_moves = Population[fight_card[0]].return_remaining_moves()
        c2_moves = Population[fight_card[1]].return_remaining_moves()
        # get the total roll and roll for a probability that determines the winner
        total = creature1_str + creature2_str
        if creature1_str > creature2_str:
            total -= 20
        if creature2_str > creature1_str:
            total += 20
        roll = random.randint(1, total)
        # c1 winner
        if roll <= creature1_str:
            # winner +1 fit -2 moves
            #diff = abs(round(creature1_str)-(round(creature2_str)))
            #diff /= 100
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
    else:
        pass

    return(Population)
