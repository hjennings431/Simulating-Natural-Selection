import pygame
import pygame.freetype
from pygame.locals import *
import random
import numpy as np
from Display import *
from Objects import *
from pygame_widgets import *
from operator import attrgetter
from pymsgbox import *
random.seed(10)
running = True
run_sim = True
stop_sim = True
pause_sim = False
############################################################################################################
# Button Press handlers (need to be here for the correct name scope)
#############################################################################################################
def starthit():
    global run_sim; run_sim = True
    global pause_sim
    global last_plot1; global last_plot2; global last_plot3; global last_plot4; global last_plot5
    global gens_left
    global Population
    global graph_points
    global count
# For a restart reset everything you need here
    if not pause_sim:
        last_plot1 = (-1, -1)
        last_plot2 = (-1, -1)
        last_plot3 = (-1, -1)
        last_plot4 = (-1, -1)
        last_plot5 = (-1, -1)
        draw_axis(pygame, Screen, Width, Height, BdrRight, BdrBottom)
        Population = generate_creatures(NoOfBobs, XWorld, YWorld, Population, True, TurnsPerGen, False)
        reset_hazards(all_coord_combos, L_hazards)
        gens_left = Generations
        count = TurnsPerGen
        graph_points = (Generations/10)
        reset_fittest()
        random.seed(10)
    pause_sim = False

def stophit():
    global run_sim; run_sim=False
    global stop_sim; stop_sim=True
    global pause_sim; pause_sim = False

def pausehit():
    global pause_sim; pause_sim=True
def reset_fittest():
    global fittest_creature; fittest_creature = Creature(0.7, 0.8, 0.8, 0.9, 59, 0.5, 0, (0, 0), False, 0)
# Variables for the organisms
NoOfBobs = 100              # Number Of Creatures
WldStop=False               # World Boundary - True=stop there, False=Wrap Around
DisplaySpeed = 0            # Display update rate
# Variables for the screen display
Generations = 1000          # Define how many generations to run
MovesPerTurn = 1            # Define how many moves to run per turn
TurnsPerGen = 50            # Define turns per generation
Width=1010; Height=810      # Define width and height of the display (700x700)
XWorld=60; YWorld=60        # Define size of the world
BdrLeft=210; BdrRight=200   # Define left and right borders
BdrTop=10; BdrBottom=200    # Define top and bottom border
DrawGrid = True             # Draw grid or not
FoodPct = 20                # Percentage chance of food spawning on a tile
TallFoodPct = 10            # Percentage chance food tile being tall food
BushFoodPct = 5             # Percentage chance food tile being bush food
HazardPct = 5               # Hazard Percentage
HazardTypes = 5             # Number of Hazard types
Mut_chance = 3              # Mutation chance
# Set up the screen and set the background color
pygame.init()
Screen = pygame.display.set_mode((Width, Height))
Screen.fill((background_color))
LblFont = pygame.freetype.SysFont("courier", 16) # Using oldschool courier
# Finally update the display
game_icon = pygame.image.load('life_icon32.png')
pygame.display.set_icon(game_icon)
pygame.display.set_caption("Natural Selection Simulator")
# NoOfBobs Slider
NoOfBobs_WhereY = 10
NoOfBobs_slide = Slider(Screen, 10, NoOfBobs_WhereY+30, 190, 3, handleRadius=5, min=10, max=1000, step=10, initial=NoOfBobs, handleColour=(slider_handle_color), colour=(slider_color))
NoOfBobs_label = TextBox(Screen, 10, NoOfBobs_WhereY, 100, 24, fontSize=24, colour=(background_color), textColour=slider_text_color, borderThickness=0)
NoOfBobs_value = TextBox(Screen, 150, NoOfBobs_WhereY, 50, 24, fontSize=24, colour=(background_color), textColour=slider_text_color, borderThickness=0)
# Turns Per Generation Slider
TurnsPerGen_WhereY = 60
TurnsPerGen_slide = Slider(Screen, 10, TurnsPerGen_WhereY+30, 190, 3, handleRadius=5, min=5, max=260, step=10, initial=TurnsPerGen, handleColour=(slider_handle_color), colour=(slider_color))
TurnsPerGen_label = TextBox(Screen, 10, TurnsPerGen_WhereY, 100, 24, fontSize=24, colour=(background_color), textColour=slider_text_color, borderThickness=0)
TurnsPerGen_value = TextBox(Screen, 150, TurnsPerGen_WhereY, 50, 24, fontSize=24, colour=(background_color), textColour=slider_text_color, borderThickness=0)
# Display Speed
DisplaySpeed_WhereY = 110
DisplaySpeed_slide = Slider(Screen, 10, DisplaySpeed_WhereY+30, 190, 3, handleRadius=5, min=0, max=100, step=5, initial=DisplaySpeed,  handleColour=(slider_handle_color), colour=(slider_color))
DisplaySpeed_label = TextBox(Screen, 10, DisplaySpeed_WhereY, 100, 24, fontSize=24, colour=(background_color), textColour=slider_text_color, borderThickness=0)
DisplaySpeed_value = TextBox(Screen, 150, DisplaySpeed_WhereY, 50, 24, fontSize=24, colour=(background_color), textColour=slider_text_color, borderThickness=0)
# Total Food Slider
FoodPct_WhereY = 200
FoodPct_slide = Slider(Screen, 10, FoodPct_WhereY+30, 190, 3, handleRadius=5, min=5, max=100, step=1, initial=FoodPct,  handleColour=(slider_handle_color), colour=(slider_color))
FoodPct_label = TextBox(Screen, 10, FoodPct_WhereY, 100, 24, fontSize=24, colour=(background_color), textColour=slider_text_color, borderThickness=0)
FoodPct_value = TextBox(Screen, 150, FoodPct_WhereY, 50, 24, fontSize=24, colour=(background_color), textColour=slider_text_color, borderThickness=0)
# Tall Food Slider
TallFoodPct_WhereY = 250
TallFoodPct_slide = Slider(Screen, 10, TallFoodPct_WhereY+30, 190, 3, handleRadius=5, min=0, max=100, step=1, initial=TallFoodPct,  handleColour=(slider_handle_color), colour=(slider_color))
TallFoodPct_label = TextBox(Screen, 10, TallFoodPct_WhereY, 100, 24, fontSize=24, colour=(background_color), textColour=slider_text_color, borderThickness=0)
TallFoodPct_value = TextBox(Screen, 150, TallFoodPct_WhereY, 50, 24, fontSize=24, colour=(background_color), textColour=slider_text_color, borderThickness=0)
# Bush Food Slider
BushFoodPct_WhereY = 300
BushFoodPct_slide = Slider(Screen, 10, BushFoodPct_WhereY+30, 190, 3, handleRadius=5, min=0, max=100, step=1, initial=BushFoodPct,  handleColour=(slider_handle_color), colour=(slider_color))
BushFoodPct_label = TextBox(Screen, 10, BushFoodPct_WhereY, 100, 24, fontSize=24, colour=(background_color), textColour=slider_text_color, borderThickness=0)
BushFoodPct_value = TextBox(Screen, 150, BushFoodPct_WhereY, 50, 24, fontSize=24, colour=(background_color), textColour=slider_text_color, borderThickness=0)
# Mutation Slider
HazardPct_WhereY = 350
MutationPct_slide = Slider(Screen, 10, HazardPct_WhereY+30, 190, 3, handleRadius=5, min=1, max=100, step=1, initial=Mut_chance,  handleColour=(slider_handle_color), colour=(slider_color))
MutationPct_label = TextBox(Screen, 10, HazardPct_WhereY, 100, 24, fontSize=24, colour=(background_color), textColour=slider_text_color, borderThickness=0)
MutationPct_value = TextBox(Screen, 150, HazardPct_WhereY, 50, 24, fontSize=24, colour=(background_color), textColour=slider_text_color, borderThickness=0)
# Hazard slider
MutationPct_WhereY = 400
HazardPct_slide = Slider(Screen, 10, MutationPct_WhereY+30, 190, 3, handleRadius=5, min=0, max = 100, step = 1, initial=HazardPct, handleColour=(slider_handle_color), colour=(slider_color))
HazardPct_label = TextBox(Screen, 10, MutationPct_WhereY, 100, 24, fontSize=24, colour=(background_color), textColour=slider_text_color, borderThickness=0)
HazardPct_value = TextBox(Screen, 150, MutationPct_WhereY, 50, 24, fontSize=24, colour=(background_color), textColour=slider_text_color, borderThickness=0)
# *********************************************************************************************************************

# Hazard Type check boxes
HazardA = checkbox(pygame, (255,255,255), 10, 470, 15, 15, check=True, text="Thorns")
HazardB = checkbox(pygame, (255,255,255), 110, 470, 15, 15, check=True, text="Tar Pits")
HazardC = checkbox(pygame, (255,255,255), 10, 490, 15, 15, check=True, text="Gas")
HazardD = checkbox(pygame, (255,255,255), 110, 490, 15, 15, check=True, text="Predators")
HazardE = checkbox(pygame, (255,255,255), 10, 510, 15, 15, check=True, text="Tree Pred.")
HazardF = checkbox(pygame, (255,255,255), 110, 510, 15, 15, check=True, text="Snakes")
hazard_toggles = []
hazard_toggles.append(HazardA); hazard_toggles.append(HazardB); hazard_toggles.append(HazardC); hazard_toggles.append(HazardD); hazard_toggles.append(HazardE); hazard_toggles.append(HazardF)
draw_key(pygame, Screen, XWorld, YWorld, Width, Height, BdrLeft, BdrRight, BdrTop, BdrBottom)

# Set to -1 to restart graph plot
last_plot1 = (-1, -1); last_plot2 = (-1, -1); last_plot3 = (-1, -1); last_plot4 = (-1, -1); last_plot5 = (-1, -1)
draw_axis(pygame, Screen, Width, Height, BdrRight, BdrBottom)

# Draw the buttons
StartButton = Button(Screen, 10, Height-BdrBottom-20, 60, 20, text='Start', fontSize=24, inactiveColour=button_bg_color, pressedColour=button_hit_color, radius=4, onClick=lambda: starthit())
StopButton = Button(Screen, 75, Height-BdrBottom-20, 60, 20, text='Stop', fontSize=24, inactiveColour=button_bg_color, pressedColour=button_hit_color, radius=4, onClick=lambda: stophit())
PauseButton = Button(Screen, 140, Height-BdrBottom-20, 60, 20, text='Pause', fontSize=24, inactiveColour=button_bg_color, pressedColour=button_hit_color, radius=4, onClick=lambda: pausehit())
ResetFittestButton = Button(Screen, 10, Height-BdrBottom-60, 190, 30, text='Reset Fittest', fontSize=32, inactiveColour=button_bg_color, pressedColour=button_hit_color, radius=4, onClick=lambda: reset_fittest())
# Defining lists and 2d array for the world
Population = []
possible_x = []
possible_y = []
L_food = np.empty((XWorld,YWorld), dtype=object)
# setting up a dummy fittest creature for the genetic algorithm to compare to
fittest_creature = Creature(0.7, 0.8, 0.8, 0.9, 59, 0.5, 0, (0, 0), False, 0)
# adding all possible x and y coords to 2 seperate lists
for i in range(XWorld):
    possible_x.append(i)
for i in range(YWorld):
    possible_y.append(i)

# Creating a list with all possible coord combos
all_coord_combos = [(a,b) for a in possible_x for b in possible_y]

# function to reset all the food tiles so a new set of food can be spawned for the next gen
# initialising the first food and population
reset_food(all_coord_combos, L_food)
generate_food(all_coord_combos, FoodPct, TallFoodPct, BushFoodPct, L_food)

# Generate Population
#Population = generate_creatures(NoOfBobs, XWorld, YWorld, Population, True, TurnsPerGen, False)
multiplier = round((TurnsPerGen * 1.5) - (TurnsPerGen * 0.2))
for i in range(NoOfBobs):
    Population.append(Creature(0.5, 0.5, 0.5, 0.5, int(0.5*multiplier), 0.5, 0, (random.randint(0, XWorld - 1),random.randint(0, YWorld - 1)), True, 0))

# Generate Hazards
L_hazards = np.empty((XWorld,YWorld), dtype=object)
reset_hazards(all_coord_combos, L_hazards)
generate_hazards(all_coord_combos, HazardPct, HazardTypes, L_hazards, hazard_toggles)

# Just keep running until some event(s)
count = TurnsPerGen
gens_left = Generations
graph_points = Generations/10
stop_count = 0
while running:
    if (run_sim and not pause_sim):
        Population.sort(key=attrgetter('speed'), reverse=True)
        for j in range(MovesPerTurn):
            for i in range(len(Population)):
                Population[i].update_position(XWorld, YWorld, WldStop, L_food, L_hazards)
            count -=1
        # find any instances where a creature fight will occur and resolve them
        Population = fight_club(Population)
        # check the turns per gen hasn't reached 0 or sliders have been updated
        if count < 0:
            # Get the latest values from the sliders
            NoOfBobs = NoOfBobs_slide.getValue()
            TurnsPerGen = TurnsPerGen_slide.getValue()
            FoodPct = FoodPct_slide.getValue()
            TallFoodPct = TallFoodPct_slide.getValue()
            BushFoodPct = BushFoodPct_slide.getValue()
            HazardPct = HazardPct_slide.getValue()
            Mut_chance = MutationPct_slide.getValue()
            # delete the old pop and create the new one
            Population, fittest_creature = genetic(Population, NoOfBobs, fittest_creature, XWorld, YWorld, TurnsPerGen, Mut_chance, TallFoodPct)
            # reset fitness and food eaten vals for the pop
            for i in range(len(Population)):
                Population[i].update_fitness(0)
                Population[i].update_food_ate(0)
        # Reset the food
            reset_food(all_coord_combos, L_food)
            generate_food(all_coord_combos, FoodPct, TallFoodPct, BushFoodPct, L_food)
        # Reset the Hazards
            reset_hazards(all_coord_combos, L_hazards)
            generate_hazards(all_coord_combos, HazardPct, HazardTypes, L_hazards, hazard_toggles)
            count = TurnsPerGen
            gens_left -= 1
            if (gens_left <= 0):
                run_sim = False
            # reset graph pop
            graph_pop = []
            # sort pop on fitness
            Population.sort(key=attrgetter('fitness'), reverse=True)
            # append the top 10% to graph pop
            for i in range(round((len(Population)/10))):
                graph_pop.append(Population[i])
            # draw the new graph points
            attr1 = get_average_neck(graph_pop)
            last_plot1 = update_graph(pygame, Screen, Width, Height, BdrRight, BdrBottom,(Generations/10), graph_points, attr1, attr1_color, last_plot1)
            attr2 = get_average_str(graph_pop)
            last_plot2 = update_graph(pygame, Screen, Width, Height, BdrRight, BdrBottom, (Generations/10), graph_points, attr2, attr2_color, last_plot2)
            attr3 = get_average_vision(graph_pop)
            last_plot3 = update_graph(pygame, Screen, Width, Height, BdrRight, BdrBottom, (Generations/10), graph_points, attr3, attr3_color, last_plot3)
            attr4 = get_average_stam(graph_pop)
            last_plot4 = update_graph(pygame, Screen, Width, Height, BdrRight, BdrBottom, (Generations/10), graph_points, attr4, attr4_color, last_plot4)
            attr5 = get_average_speed(graph_pop)
            last_plot5 = update_graph(pygame, Screen, Width, Height, BdrRight, BdrBottom, (Generations/10), graph_points, attr5, attr5_color, last_plot5)
            graph_points -= 1
        # reset the graph if the graph has reached the edge
        if graph_points <= 0:
            if gens_left <= 0:
                last_plot1 = (-1, -1); last_plot2 = (-1, -1); last_plot3 = (-1, -1); last_plot4 = (-1, -1); last_plot5 = (-1, -1)
            else:
                last_plot1 = (-1, -1); last_plot2 = (-1, -1); last_plot3 = (-1, -1); last_plot4 = (-1, -1); last_plot5 = (-1, -1)
                draw_axis(pygame, Screen, Width, Height, BdrRight, BdrBottom)
                graph_points = Generations / 10

        # update the screen to match the new state of the world
        draw_grid(pygame, Screen, XWorld, YWorld, Width, Height, BdrLeft, BdrRight, BdrTop, BdrBottom, DrawGrid)
        draw_food(pygame, Screen, XWorld, YWorld, Width, Height, BdrLeft, BdrRight, BdrTop, BdrBottom, L_food, DrawGrid)
        draw_hazard(pygame, Screen, XWorld, YWorld, Width, Height, BdrLeft, BdrRight, BdrTop, BdrBottom, L_hazards, DrawGrid)
        draw_creatures(pygame, Screen, XWorld, YWorld, Width, Height, BdrLeft, BdrRight, BdrTop, BdrBottom, Population, DrawGrid)
        draw_border(pygame, Screen, Width, Height, BdrLeft, BdrRight, BdrTop, BdrBottom )
        draw_fittest(pygame, Screen, XWorld, YWorld, Width, Height, BdrLeft, BdrRight, BdrTop, BdrBottom, fittest_creature)

    pygame.display.flip()
    pygame.time.wait(DisplaySpeed) # Higher for slower animation

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not pause_sim:
        # Handle the NoOfBobs Slider
            pygame.draw.rect(Screen, background_color, (0, NoOfBobs_WhereY, BdrLeft, 45))
            NoOfBobs_slide.listen(event); NoOfBobs_slide.draw()
            NoOfBobs_value.setText(NoOfBobs_slide.getValue()); NoOfBobs_value.draw()
            NoOfBobs_label.setText("Creatures"); NoOfBobs_label.draw()
        # Handle the TurnPerGen Slider
            pygame.draw.rect(Screen, background_color, (0, TurnsPerGen_WhereY, BdrLeft, 45))
            TurnsPerGen_slide.listen(event); TurnsPerGen_slide.draw()
            TurnsPerGen_value.setText(TurnsPerGen_slide.getValue()); TurnsPerGen_value.draw()
            TurnsPerGen_label.setText("Turns"); TurnsPerGen_label.draw()
            pygame.draw.rect(Screen, background_color, (0, DisplaySpeed_WhereY, BdrLeft, 45))
            #display speed slider
            DisplaySpeed_slide.listen(event); DisplaySpeed_slide.draw()
            DisplaySpeed_value.setText(DisplaySpeed_slide.getValue()); DisplaySpeed_value.draw()
            DisplaySpeed_label.setText("Display Speed"); DisplaySpeed_label.draw()
            DisplaySpeed = DisplaySpeed_slide.getValue()
            # Handle the Food Percentage Slider
            pygame.draw.rect(Screen, background_color, (0, FoodPct_WhereY, BdrLeft, 45))
            FoodPct_slide.listen(event); FoodPct_slide.draw()
            FoodPct_value.setText(FoodPct_slide.getValue()); FoodPct_value.draw()
            FoodPct_label.setText("Total Food %"); FoodPct_label.draw()
        # Handle the Tall Food Slider
            pygame.draw.rect(Screen, background_color, (0, TallFoodPct_WhereY, BdrLeft, 45))
            TallFoodPct_slide.listen(event); TallFoodPct_slide.draw()
            TallFoodPct_value.setText(TallFoodPct_slide.getValue()); TallFoodPct_value.draw()
            TallFoodPct_label.setText("Tree Food %"); TallFoodPct_label.draw()
        # Handle the Bush Food Slider
            pygame.draw.rect(Screen, background_color, (0, BushFoodPct_WhereY, BdrLeft, 45))
            BushFoodPct_slide.listen(event); BushFoodPct_slide.draw()
            BushFoodPct_value.setText(BushFoodPct_slide.getValue()); BushFoodPct_value.draw()
            BushFoodPct_label.setText("Bush Food %"); BushFoodPct_label.draw()
        # Handle the Hazards Slider
            pygame.draw.rect(Screen, background_color, (0, HazardPct_WhereY, BdrLeft, 45))
            MutationPct_slide.listen(event); MutationPct_slide.draw()
            MutationPct_value.setText(MutationPct_slide.getValue()); MutationPct_value.draw()
            MutationPct_label.setText("Mutation %"); MutationPct_label.draw()
        # Handle the hazard % slider
            pygame.draw.rect(Screen, background_color, (0,MutationPct_WhereY, BdrLeft, 45))
            HazardPct_slide.listen(event); HazardPct_slide.draw()
            HazardPct_value.setText(HazardPct_slide.getValue()); HazardPct_value.draw()
            HazardPct_label.setText("Hazard %"); HazardPct_label.draw()
        # Handle the Hazard checkboxes
            pygame.draw.rect(Screen, background_color, (10, 470, BdrLeft-10, 60) )
            HazardA.draw(pygame, Screen); HazardB.draw(pygame, Screen)
            HazardC.draw(pygame, Screen); HazardD.draw(pygame, Screen)
            HazardE.draw(pygame, Screen); HazardF.draw(pygame, Screen)
            if event.type == MOUSEBUTTONDOWN:
                if (HazardA.isOver(event.pos)): HazardA.convert()
                if (HazardB.isOver(event.pos)): HazardB.convert()
                if (HazardC.isOver(event.pos)): HazardC.convert()
                if (HazardD.isOver(event.pos)): HazardD.convert()
                if (HazardE.isOver(event.pos)): HazardE.convert()
                if (HazardF.isOver(event.pos)): HazardF.convert()
    # Handle the Start Button
        StartButton.listen(event); StartButton.draw()
    # Handle the Stop Button
        StopButton.listen(event); StopButton.draw()
    # Handle the Pause Button
        PauseButton.listen(event); PauseButton.draw()
        #handle the fittest button
        ResetFittestButton.listen(event) ; ResetFittestButton.draw()
