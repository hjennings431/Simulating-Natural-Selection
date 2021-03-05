import pygame
import pygame.freetype
import random
import numpy as np
from Display import *
from Objects import *
from pygame_widgets import *

# Variables for the organisms
NoOfBobs = 100              # Number Of Creatures
WldStop=False               # World Boundary - True=stop there, False=Wrap Around
DisplaySpeed = 40          # Display update rate
# Variables for the screen display
Generations = 1000          # Define how many generations to run
MovesPerTurn = 1            # Define how many moves to run per turn
TurnsPerGen = 50            # Define turns per generation
Width=1090; Height=800      # Define width and height of the display (700x700)
XWorld=80; YWorld=80        # Define size fo the world
BdrLeft=210; BdrRight=200   # Define left and right borders
BdrTop=10; BdrBottom=10     # Define top and bottom border
DrawGrid = True             # Draw grid or not
FoodPct = 20                # Percentage chance of food spawning on a tile
TallFoodPct = 10            # Percentage chance food tile being tall food
BushFoodPct = 5             # Percentage chance food tile being bush food

# Set up the screen and set the background color
pygame.init()
Screen = pygame.display.set_mode((Width, Height))
Screen.fill((BackGroundColor))
LblFont = pygame.freetype.SysFont("courier", 16) # Using oldschool courier
# Finally update the display
pygame.display.set_caption("Life Simulator")
# NoOfBobs Slider
NoOfBobs_WhereY = 10
NoOfBobs_slide = Slider(Screen, 10, NoOfBobs_WhereY+30, 190, 3, handleRadius=5, min=1, max=1000, step=10, initial=NoOfBobs, handleColour=(255,150,0), colour=(220,220,220))
NoOfBobs_label = TextBox(Screen, 10, NoOfBobs_WhereY, 100, 24, fontSize=24, colour=(0,0,0), textColour=(255,255,255), borderThickness=0)
NoOfBobs_value = TextBox(Screen, 150, NoOfBobs_WhereY, 50, 24, fontSize=24, colour=(0,0,0), textColour=(255,255,255), borderThickness=0)
# Turns Per Generation Slider
TurnsPerGen_WhereY = 60
TurnsPerGen_slide = Slider(Screen, 10, TurnsPerGen_WhereY+30, 190, 3, handleRadius=5, min=1, max=250, step=10, initial=TurnsPerGen, handleColour=(255,150,0), colour=(220,220,220))
TurnsPerGen_label = TextBox(Screen, 10, TurnsPerGen_WhereY, 100, 24, fontSize=24, colour=(0,0,0), textColour=(255,255,255), borderThickness=0)
TurnsPerGen_value = TextBox(Screen, 150, TurnsPerGen_WhereY, 50, 24, fontSize=24, colour=(0,0,0), textColour=(255,255,255), borderThickness=0)
# Total Food Slider
FoodPct_WhereY = 200
FoodPct_slide = Slider(Screen, 10, FoodPct_WhereY+30, 190, 3, handleRadius=5, min=0, max=100, step=1, initial=FoodPct, handleColour=(255,150,0), colour=(220,220,220))
FoodPct_label = TextBox(Screen, 10, FoodPct_WhereY, 100, 24, fontSize=24, colour=(0,0,0), textColour=(255,255,255), borderThickness=0)
FoodPct_value = TextBox(Screen, 150, FoodPct_WhereY, 50, 24, fontSize=24, colour=(0,0,0), textColour=(255,255,255), borderThickness=0)
# Tall Food Slider
TallFoodPct_WhereY = 250
TallFoodPct_slide = Slider(Screen, 10, TallFoodPct_WhereY+30, 190, 3, handleRadius=5, min=0, max=100, step=1, initial=TallFoodPct, handleColour=(255,150,0), colour=(220,220,220))
TallFoodPct_label = TextBox(Screen, 10, TallFoodPct_WhereY, 100, 24, fontSize=24, colour=(0,0,0), textColour=(255,255,255), borderThickness=0)
TallFoodPct_value = TextBox(Screen, 150, TallFoodPct_WhereY, 50, 24, fontSize=24, colour=(0,0,0), textColour=(255,255,255), borderThickness=0)
# Bush Food Slider
BushFoodPct_WhereY = 300
BushFoodPct_slide = Slider(Screen, 10, BushFoodPct_WhereY+30, 190, 3, handleRadius=5, min=0, max=100, step=1, initial=BushFoodPct, handleColour=(255,150,0), colour=(220,220,220))
BushFoodPct_label = TextBox(Screen, 10, BushFoodPct_WhereY, 100, 24, fontSize=24, colour=(0,0,0), textColour=(255,255,255), borderThickness=0)
BushFoodPct_value = TextBox(Screen, 150, BushFoodPct_WhereY, 50, 24, fontSize=24, colour=(0,0,0), textColour=(255,255,255), borderThickness=0)

# Defining lists and 2d array for the world
Population = []
possible_x = []
possible_y = []
L_food = np.empty((XWorld,YWorld), dtype=object)
# setting up a dummy fittest creature for the genetic algorithm to compare to
fittest_creature =Creature(0.8, 0.8, 0.8, 0.9, 59, 0.5, 0,(0,0))
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
generate_food(all_coord_combos, FoodPct, TallFoodPct, BushFoodPct, L_food)
Population = generate_creatures(NoOfBobs, XWorld, YWorld, Population)
#for i in range(NoOfBobs):
 #   Population.append(Creature(True, 0.5, 1, 1, 0, (random.randint(0, XWorld-1), random.randint(0, YWorld-1))))

# Just keep running until some event(s)
running = True
count = TurnsPerGen
slider_update = False
while running:
    for j in range(MovesPerTurn):
        for i in range(len(Population)):
            Population[i].update_position(XWorld, YWorld, WldStop, L_food)
        count -=1
    # check the turns per gen hasn't reached 0 or sliders have been updated
    if (count == 0) :
    # Get the latest values from the sliders
        NoOfBobs = NoOfBobs_slide.getValue()
        TurnsPerGen = TurnsPerGen_slide.getValue()
        FoodPct = FoodPct_slide.getValue()
        TallFoodPct = TallFoodPct_slide.getValue()
        BushFoodPct = BushFoodPct_slide.getValue()

        reset_food(all_coord_combos, L_food)
        generate_food(all_coord_combos, FoodPct, TallFoodPct, BushFoodPct, L_food)
        count = TurnsPerGen
        # get the fitness of the current pop
        for i in range(len(Population)):
            output_fitness = Population[i].return_fitness()
        # delete the old pop and create the new one
        Population, fittest_creature = genetic(Population, fittest_creature, XWorld, YWorld)
        print()
        #for i in range(NoOfBobs):
         #   Population.append(Creature(True, 0.5, 1, 1, 0, (random.randint(0, XWorld - 1), random.randint(0, YWorld - 1))))

    # update the screen to match the new state of the world
    draw_grid(pygame, Screen, XWorld, YWorld, Width, Height, BdrLeft, BdrRight, BdrTop, BdrBottom, DrawGrid)
    draw_food(pygame, Screen, XWorld, YWorld, Width, Height, BdrLeft, BdrRight, BdrTop, BdrBottom, L_food, DrawGrid)
    draw_creatures(pygame, Screen, XWorld, YWorld, Width, Height, BdrLeft, BdrRight, BdrTop, BdrBottom, Population, DrawGrid)
    draw_border(pygame, Screen, Width, Height, BdrLeft, BdrRight, BdrTop, BdrBottom )
    draw_key(pygame, Screen, XWorld, YWorld, Width, Height, BdrLeft, BdrRight, BdrTop, BdrBottom)
    pygame.display.flip()
    pygame.time.wait(DisplaySpeed) # Higher for slower animation

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Handle the NoOfBobs Slider
        pygame.draw.rect(Screen, BackGroundColor, (0, NoOfBobs_WhereY, BdrLeft, 45))
        NoOfBobs_slide.listen(event); NoOfBobs_slide.draw()
        NoOfBobs_value.setText(NoOfBobs_slide.getValue()); NoOfBobs_value.draw()
        NoOfBobs_label.setText("Creatures"); NoOfBobs_label.draw()
    # Handle the TurnPerGen Slider
        pygame.draw.rect(Screen, BackGroundColor, (0, TurnsPerGen_WhereY, BdrLeft, 45))
        TurnsPerGen_slide.listen(event); TurnsPerGen_slide.draw()
        TurnsPerGen_value.setText(TurnsPerGen_slide.getValue()); TurnsPerGen_value.draw()
        TurnsPerGen_label.setText("Turns"); TurnsPerGen_label.draw()
    # Handle the Food Percentage Slider
        pygame.draw.rect(Screen, BackGroundColor, (0, FoodPct_WhereY, BdrLeft, 45))
        FoodPct_slide.listen(event); FoodPct_slide.draw()
        FoodPct_value.setText(FoodPct_slide.getValue()); FoodPct_value.draw()
        FoodPct_label.setText("Total Food %"); FoodPct_label.draw()
    # Handle the Tall Food Slider
        pygame.draw.rect(Screen, BackGroundColor, (0, TallFoodPct_WhereY, BdrLeft, 45))
        TallFoodPct_slide.listen(event); TallFoodPct_slide.draw()
        TallFoodPct_value.setText(TallFoodPct_slide.getValue()); TallFoodPct_value.draw()
        TallFoodPct_label.setText("Tree Food %"); TallFoodPct_label.draw()
    # Handle the Tall Food Slider
        pygame.draw.rect(Screen, BackGroundColor, (0, BushFoodPct_WhereY, BdrLeft, 45))
        BushFoodPct_slide.listen(event); BushFoodPct_slide.draw()
        BushFoodPct_value.setText(BushFoodPct_slide.getValue()); BushFoodPct_value.draw()
        BushFoodPct_label.setText("Bush Food %"); BushFoodPct_label.draw()
