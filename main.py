import pygame
import pygame.freetype
import random
import numpy as np
from display import *
from objects import *


# Variables for the organisms
NoOfBobs = 100
WldStop=False             # World Boundary - True=stop there, False=Wrap Around

# Variables for the screen display
Generations = 1000          # Define how many generations to run
MovesPerTurn = 1            # Define how many moves to run per turn
TurnsPerGen = 50            # Define turns per generation
Width=700; Height=500       # Define width and height of the display (700x700)
XWorld=80; YWorld=80        # Define size fo the world
BdrLeft=210; BdrRight=10    # Define left and right borders
BdrTop=10; BdrBottom=10     # Define top and bottom border
BGColor = (0,0,0)           # Define display background color
GridColor = (50,50,50)      # Define the line color
BdrColor = (255,255,255)    # Define the line color
LabelColor = (255,255,255)  # Define the label colors
DrawGrid = True             # Draw grid or not
FoodPct = "20%"             # Percentage chance of food spawning on a tile
TallFoodPct = "5%"          # Percentage chance of tall food spawning on a tile (Bush food chance is directly tied to this)




# Set up the screen and set the background color
pygame.init()
Screen = pygame.display.set_mode((Width, Height))
Screen.fill((BGColor))
LblFont = pygame.freetype.SysFont("courier", 16) # Using oldschool courier
# Finally update the display
pygame.display.set_caption("Life Simulator")
# Draw all the labels
SimpLabel(Screen, LblFont, "Creatures", NoOfBobs, 10, 0, LabelColor, BdrTop)
SimpLabel(Screen, LblFont, "World X", XWorld, 10, 30, LabelColor, BdrTop)
SimpLabel(Screen, LblFont, "World Y", YWorld, 10, 60, LabelColor, BdrTop)
SimpLabel(Screen, LblFont, "Generations", Generations, 10, 90, LabelColor, BdrTop)
SimpLabel(Screen, LblFont, "Moves Per Turn", MovesPerTurn, 10, 120, LabelColor, BdrTop)

# Defining lists and 2d array for the world
Population = []
possible_x = []
possible_y = []
L_food = np.empty((XWorld,YWorld), dtype=object)


# adding all possible x and y coords to 2 seperate lists
for i in range(XWorld):
    possible_x.append(i)
for i in range(YWorld):
    possible_y.append(i)

 # creating a list with all possible coord combos
all_coord_combos = [(a,b) for a in possible_x for b in possible_y]

# function to reset all the food tiles so a new set of food can be spawned for the next gen


# initialising the first food and population
reset_food(all_coord_combos, L_food)
generate_food(XWorld, YWorld, "20%", "5%", L_food)
for i in range(NoOfBobs):
    Population.append(Creature(True, 0.5, 1, 1, 0, (random.randint(0, XWorld-1), random.randint(0, YWorld-1))))

# Just keep running until some event(s)
running = True
count = TurnsPerGen
while running:
    for j in range(MovesPerTurn):
        for i in range(NoOfBobs):
            Population[i].update_position(XWorld, YWorld, WldStop, L_food)
        count -=1
    # check the turns per gen hasn't reached 0
    if count == 0:
        reset_food(all_coord_combos, L_food)
        generate_food(XWorld, YWorld, FoodPct, TallFoodPct, L_food)
        count = TurnsPerGen
        # get the fitness of the current pop
        for i in range(len(Population)):
            output_fitness = Population[i].return_fitness()
            print("my fitness is: " + str(output_fitness))
        # delete the old pop and create the new one
        Population = []
        for i in range(NoOfBobs):
            Population.append(Creature(True, 0.5, 1, 1, 0, (random.randint(0, XWorld - 1), random.randint(0, YWorld - 1))))
    # update the screen to match the new state of the world
    draw_grid(pygame, Screen, XWorld, YWorld, Width, Height, BdrLeft, BdrRight, BdrTop, BdrBottom, GridColor, DrawGrid)
    draw_food(pygame, Screen, XWorld, YWorld, Width, Height, BdrLeft, BdrRight, BdrTop, BdrBottom, L_food, DrawGrid)
    draw_creatures(pygame, Screen, XWorld, YWorld, Width, Height, BdrLeft, BdrRight, BdrTop, BdrBottom, Population, DrawGrid)
    draw_border(pygame, Screen, Width, Height, BdrLeft, BdrRight, BdrTop, BdrBottom,BdrColor)
    pygame.display.flip()
    pygame.time.wait(50) # Higher for slower animation
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
