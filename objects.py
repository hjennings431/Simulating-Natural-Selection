import random


############################################################################################################
# Common base class for all creatures.
############################################################################################################
class Creature:
    def __init__(self, long_neck, speed, max_stamina, remaining_stamina, fitness, position):
        self.long_neck = long_neck                  # a bool to determine if a creature has a long or short neck
        self.speed = speed                          # an int to determine a creatures speed (Movement order)
        self.max_stamina = max_stamina              # an int that determines a creatures stamina (How many tiles can be moved before the creature can no longer move)
        self.remaining_stamina = remaining_stamina  # an int that indicates how much stamina a creature has left
        self.fitness = fitness                      # an int to show how fit a specific instance of a creature is (intially set to 0), this is the amount of food they find in a generation.
        self.position = position                    # references a coord position, this is where the creature is currently positioned.
    #function to get position
    def return_positon(self): # returns a creatures current position
        return(self.position)
    #function to get fitness
    def return_fitness(self):
        return(self.fitness)

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
            if potential_x >= XL:
                potential_x = 0
            if potential_y >= YL:
                potential_y = 0
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



#simple function to work out a %
def percent(expression):
    if "%" in expression:
        expression = expression.replace("%","/100")
    return eval(expression)

#function to generate the food onto the world
def generate_food(WX, WY, food_pct, tall_food_pct, L_food): # food_pct and tall_food_pct must be strings with a % after the number
    number_of_tiles = WX*WY
    pass_to_pct_food = str(number_of_tiles) + "*" + food_pct
    number_of_food = round(percent(pass_to_pct_food))
    pass_to_pct_tall_food = str(number_of_food) + "*" + tall_food_pct
    number_of_tall_food = round(percent(pass_to_pct_tall_food))
    tall_food_pct = int(tall_food_pct[:-1])
    bush_food_pct = str(tall_food_pct/2) + "%"
    number_of_bush_food = round(percent(bush_food_pct))
    update_food_tiles(WX, WY, number_of_food, 1, L_food)
    update_food_tiles(WX, WY, number_of_tall_food, 2, L_food)
    update_food_tiles(WX, WY, number_of_bush_food, 3, L_food)

def update_food_tiles(WX, WY, num_of_food, food_type, L_food):
    WX -=1
    WY -=1
    while num_of_food != 0:
        random_x = random.randint(0,WX)
        random_y = random.randint(0,WY)
        checker = L_food[random_x, random_y]
        checker.return_food_type()
        if checker.food_type == 0:
            L_food[random_x, random_y].update_food_type(food_type)
            num_of_food -= 1
        else: pass

def reset_food(all_coord_combos, L_food):
    for i in range(len(all_coord_combos)):
        p_holder = all_coord_combos[i]
        input_food = Food(p_holder, 0)
        L_food[p_holder[0], p_holder[1]] = input_food
