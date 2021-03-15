creature_colour = (0, 255, 255)             # Creature Colour
multiple_creature_colour = (255,200,0)      # Multiple occupancy tile colour
no_food_colour = (0,0,0)                    # Blank tile colour
food_colour = (51,204,51)                   # Normal food tile colour
tallfood_colour = (20,82,20)                # Tall food tile colour
bushfood_colour = (112,219,112)             # Bush food tile colour
hazard1_color = (255,0,0)                   # Hazard colour
hazard2_color = (255,50,0)                  # Hazard colour
hazard3_color = (255,100,0)                 # Hazard colour
hazard4_color = (255,150,0)                 # Hazard colour
hazard5_color = (255,200,0)                 # Hazard colour
background_color = (20,20,30)               # Define the background color
grid_color = (50,50,50)                     # Define the grid line color
border_color = (255,255,255)                # Define the line color
key_label_color = (255,255,255)             # Color for the key labels
key_step = 20                               # Step between keys and key labels
slider_color = (255,255,255)                # Slider color
slider_text_color = (255, 255, 255)         # Text color for slider
slider_handle_color = (255, 128, 0)         # Slider handle color
button_bg_color = (255, 255, 255)           # Button Background color
button_hover_color = (128, 128, 128)        # Button hovered over color
button_hit_color = (255, 0, 0)              # Button clicked color

axis_color = (255,255,255)                  # Color for the graph axis
grid_graph_color = (50,50,50)               # Color for the graph grid
grid_X_num = 32                             # Number of X grid lines
grid_Y_num = 10                             # Number of Y grid lines
axis_label_color = (255,255,255)            # Axis label color
axis_space = 20                             # Axis spacing from border
attr1_color = (255,128,128)                 # Attribute 1 graph color
attr1_label = "Neck Length"                 # Attribute 1 graph label
attr2_color = (255,255,128)                 # Attribute 2 graph color
attr2_label = "Strength"                    # Attribute 2 graph label
attr3_color = (255,128,255)                 # Attribute 3 graph color
attr3_label = "Vision"                      # Attribute 3 graph label
attr4_color = (128,128,255)                 # Attribute 4 graph color
attr4_label = "Stamina"                     # Attribute 4 graph label
attr5_color = (128, 255, 128)               # Attribute 5 graph color
attr5_label = "Speed"                       # Attribute 5 graph label


############################################################################################################
# Procedure to draw the grid for the display
############################################################################################################
def draw_grid(pygame, scn, xw, yw, w, h, bdl, bdr, bdt, bdb, drwgrd):
# Clear the current grid
    pygame.draw.rect(scn, background_color, (bdl, bdt, w-bdr-bdl, h-bdb-bdt))
# Draw the grid if required
    if ( drwgrd ):
    # Find the steps for each grid line
        stepx = (w-bdr-bdl)/xw
        stepy = (h-bdt-bdb)/yw
    # Find the start points
        startx=bdl
        starty=bdt
    # Draw the grid
        for x in range(xw):
            pygame.draw.line(scn, grid_color, [startx, bdt], [startx, h-bdb])
            startx += stepx
        for y in range(yw):
            pygame.draw.line(scn, grid_color, [bdl,starty], [w-bdr, starty])
            starty += stepy
############################################################################################################
# Procedure to draw the border for the display
############################################################################################################
def draw_border(pygame, scn, w, h, bdl, bdr, bdt, bdb ):
# Draw the border
    pygame.draw.line(scn, border_color, [bdl, bdt], [bdl, h-bdb])
    pygame.draw.line(scn, border_color, [w-bdr, bdt], [w-bdr, h-bdb])
    pygame.draw.line(scn, border_color, [bdl, bdt], [w-bdr, bdt])
    pygame.draw.line(scn, border_color, [bdl, h-bdb], [w-bdr, h-bdb])
############################################################################################################
# Procedure to draw a simple label
############################################################################################################
def simple_label(scn, font, label, value, x, y, tc, BdrTop):
    display_text = label + " = " + str(value)
    font.render_to(scn, (x, BdrTop+y), display_text, tc)
############################################################################################################
# Procedure to draw the food
############################################################################################################
def draw_food(pygame, scn, xw, yw, w, h, bdl, bdr, bdt, bdb, tiles, dg):
    if (dg): size_adj=1
    else: size_adj=0
    stepx = (w-bdr-bdl)/xw
    stepy = (h-bdt-bdb)/yw
# Go through all the tiles
    for i in range(xw):
        for j in range(yw):
        # See if the tile has food
            if tiles[i,j].food_type == 0:
                pass
            else:
            # Pick the food colour accordingly
                fc = food_colour
                if tiles[i, j].food_type == 2:
                    fc = tallfood_colour
                if tiles[i, j].food_type == 3:
                    fc = bushfood_colour
            # Colour the tile based on the selected food type
                xy = (i,j)
                x = bdl + size_adj + (xy[0] * stepx)
                y = bdt + size_adj + (xy[1] * stepy)
                pygame.draw.rect(scn, fc, (x, y, stepx - size_adj, stepy - size_adj))
############################################################################################################
# Procedure to draw the creatures
############################################################################################################
def draw_creatures(pygame, scn, xw, yw, w, h, bdl, bdr, bdt, bdb, pop, dg):
# Adjust the size deoending if there's a grid
    if (dg): size_adj=1
    else: size_adj=0
# Find the steps for each grid line
    stepx = (w-bdr-bdl)/xw
    stepy = (h-bdt-bdb)/yw
# Go through all the Bobs
    for i in range(len(pop)):
    # Get the current position
        xy=pop[i].position
    # Find the square to color in
        x = bdl + size_adj + (xy[0]*stepx)
        y = bdt + size_adj + (xy[1]*stepy)
    # Get the color of the current square and Make the bob white if square already occupied
        current_cc = scn.get_at((int(x), int(y)))
        r=current_cc[0]; g=current_cc[1]; b=current_cc[2]
        if (r==creature_colour[0] and g==creature_colour[1] and b==creature_colour[2]):
            nc = multiple_creature_colour
        else:
            nc = creature_colour
    # Color the square
        pygame.draw.rect(scn, nc, (x,y, stepx-size_adj,stepy-size_adj))
############################################################################################################
# Procedure to draw key
############################################################################################################
def draw_key(pygame, scn, xw, yw, w, h, bdl, bdr, bdt, bdb ):
    stepy = key_step
    xx = w-(bdr-20)
    yy = bdt + (stepy/2)
    font = pygame.font.SysFont(None, 24)
    pygame.draw.rect(scn, creature_colour, (xx, yy, 10, 10))
    img = font.render('Creatures', True, key_label_color); scn.blit(img, (xx+20, yy-4))
    yy += stepy; pygame.draw.rect(scn, multiple_creature_colour, (xx, yy, 10, 10))
    img = font.render('Multiple Creatures', True, key_label_color); scn.blit(img, (xx+20, yy-4))
    yy += stepy; pygame.draw.rect(scn, food_colour, (xx, yy, 10, 10))
    img = font.render('Normal Food', True, key_label_color); scn.blit(img, (xx+20, yy-4))
    yy += stepy; pygame.draw.rect(scn, tallfood_colour, (xx, yy, 10, 10))
    img = font.render('Tree Food', True, key_label_color); scn.blit(img, (xx+20, yy-4))
    yy += stepy; pygame.draw.rect(scn, bushfood_colour, (xx, yy, 10, 10))
    img = font.render('Bush Food', True, key_label_color); scn.blit(img, (xx + 20, yy - 4))
    yy += stepy;
    pygame.draw.line(scn, hazard1_color, [xx, yy], [xx+10, yy]);       pygame.draw.line(scn, hazard1_color, [xx+10, yy], [xx+10, yy+10])
    pygame.draw.line(scn, hazard1_color, [xx+10, yy+10], [xx, yy+10]); pygame.draw.line(scn, hazard1_color, [xx, yy+10], [xx, yy])
    img = font.render('Thorns', True, key_label_color); scn.blit(img, (xx + 20, yy - 4))
    yy += stepy;
    pygame.draw.line(scn, hazard2_color, [xx, yy], [xx+10, yy]);       pygame.draw.line(scn, hazard2_color, [xx+10, yy], [xx+10, yy+10])
    pygame.draw.line(scn, hazard2_color, [xx+10, yy+10], [xx, yy+10]); pygame.draw.line(scn, hazard2_color, [xx, yy+10], [xx, yy])
    img = font.render('Tar Pits', True, key_label_color); scn.blit(img, (xx + 20, yy - 4))
    yy += stepy;
    pygame.draw.line(scn, hazard3_color, [xx, yy], [xx+10, yy]);       pygame.draw.line(scn, hazard3_color, [xx+10, yy], [xx+10, yy+10])
    pygame.draw.line(scn, hazard3_color, [xx+10, yy+10], [xx, yy+10]); pygame.draw.line(scn, hazard3_color, [xx, yy+10], [xx, yy])
    img = font.render('Gas', True, key_label_color); scn.blit(img, (xx + 20, yy - 4))
    yy += stepy;
    pygame.draw.line(scn, hazard4_color, [xx, yy], [xx+10, yy]);       pygame.draw.line(scn, hazard4_color, [xx+10, yy], [xx+10, yy+10])
    pygame.draw.line(scn, hazard4_color, [xx+10, yy+10], [xx, yy+10]); pygame.draw.line(scn, hazard4_color, [xx, yy+10], [xx, yy])
    img = font.render('Predators', True, key_label_color); scn.blit(img, (xx + 20, yy - 4))
    yy += stepy;
    pygame.draw.line(scn, hazard5_color, [xx, yy], [xx+10, yy]);       pygame.draw.line(scn, hazard5_color, [xx+10, yy], [xx+10, yy+10])
    pygame.draw.line(scn, hazard5_color, [xx+10, yy+10], [xx, yy+10]); pygame.draw.line(scn, hazard5_color, [xx, yy+10], [xx, yy])
    img = font.render('Tree Predators', True, key_label_color); scn.blit(img, (xx + 20, yy - 4))
###########################################################################################################
# Procedure to draw the stats of the fittest creature
############################################################################################################
def draw_fittest(pygame,scn, xw, yw, w, h, bdl, bdr, bdt, bdb, fittest):
    xx = w-(bdr-15)
    yy = bdt + 450
# Clear the existing
    pygame.draw.rect(scn, background_color, (xx, yy, bdr+20, 150))
# draw
    pygame.draw.line(scn, key_label_color, [xx-5, yy-5], [w-10, yy-5])
    pygame.draw.line(scn, key_label_color, [w-10, yy-5], [w-10, yy+150])
    pygame.draw.line(scn, key_label_color, [w-10, yy+150], [xx-5, yy+150])
    pygame.draw.line(scn, key_label_color, [xx-5, yy+150], [xx-5, yy-5])
    pygame.draw.rect(scn, key_label_color, (xx-5, yy-5, bdr-20, 30))

    font = pygame.font.SysFont(None, 32)
    img = font.render('Fittest Creature', True, (0,0,0)); scn.blit(img, (xx, yy)); yy+=30
    font = pygame.font.SysFont(None, 24)
    img = font.render('Neck', True, key_label_color); scn.blit(img, (xx, yy));
    img = font.render('{0:>8.2f}'.format(fittest.return_neck_type()), True, key_label_color);
    xx1=w-img.get_width()-20; scn.blit(img, (xx1, yy));
    yy += 20
    img = font.render('Vision', True, key_label_color); scn.blit(img, (xx, yy));
    img = font.render('{0:>8.2f}'.format(fittest.return_eagle_eye()), True, key_label_color);
    xx1=w-img.get_width()-20; scn.blit(img, (xx1, yy));
    yy += 20
    img = font.render('Speed', True, key_label_color); scn.blit(img, (xx, yy));
    img = font.render('{0:>8.2f}'.format(fittest.return_speed()), True, key_label_color);
    xx1=w-img.get_width()-20; scn.blit(img, (xx1, yy));
    yy += 20
    img = font.render('Stamina', True, key_label_color); scn.blit(img, (xx, yy));
    img = font.render('{0:>8.2f}'.format(fittest.return_max_stam()), True, key_label_color);
    xx1=w-img.get_width()-20; scn.blit(img, (xx1, yy));
    yy += 20
    img = font.render('Strength', True, key_label_color); scn.blit(img, (xx, yy));
    img = font.render('{0:>8.2f}'.format(fittest.return_str()), True, key_label_color);
    xx1=w-img.get_width()-20; scn.blit(img, (xx1, yy));
    yy += 20
    img = font.render('Fitness', True, key_label_color); scn.blit(img, (xx, yy));
    img = font.render('{0:>8.2f}'.format(int(fittest.return_fitness())), True, key_label_color);
    xx1=w-img.get_width()-20; scn.blit(img, (xx1, yy));
############################################################################################################
# Procedure to draw graph axis
############################################################################################################
def draw_axis(pygame, scn, w, h, bdr, bdb):
# Clear the current graph
    pygame.draw.rect(scn, background_color, (axis_space,h-bdb, w, h))
# Draw The graph grid
    grid_X_step = int((w-bdr-axis_space)/grid_X_num)
    for i in range(axis_space, (w-bdr), (grid_X_step)):
        pygame.draw.line(scn, grid_graph_color, [i, h-bdb+axis_space], [i, h - axis_space])  # Y Grid
    grid_Y_step = int((bdb-axis_space-axis_space)/(grid_Y_num))
    for i in range(axis_space, (bdb-axis_space), grid_Y_step):
        pygame.draw.line(scn, grid_graph_color, [axis_space, h-i], [w-bdr, h-i])  # X Grid
# Draw the axis
    pygame.draw.line(scn, axis_color, [axis_space, h-axis_space],  [w-bdr, h-axis_space])           # X Left axis
    pygame.draw.line(scn, axis_color, [axis_space, h-bdb+axis_space], [axis_space, h-axis_space])   # Y Left Axis
# Draw Graph Labels
    stepy = key_step # Distance to space axis labels
    xx = w-(bdr-20)
    yy = h-bdb+axis_space
# Attribute 1 Label
    font = pygame.font.SysFont(None, 24)
    pygame.draw.rect(scn, attr1_color, (xx, yy, 10, 10))
    img = font.render(attr1_label, True, axis_label_color); scn.blit(img, (xx+20, yy-4))
# Attribute 2 Label
    yy+=stepy
    pygame.draw.rect(scn, attr2_color, (xx, yy, 10, 10))
    img = font.render(attr2_label, True, axis_label_color)
    scn.blit(img, (xx + 20, yy - 4))
# Attribute 3 Label
    yy += stepy
    pygame.draw.rect(scn, attr3_color, (xx, yy, 10, 10))
    img = font.render(attr3_label, True, axis_label_color)
    scn.blit(img, (xx + 20, yy - 4))
# Attribute 4 Label
    yy += stepy
    pygame.draw.rect(scn, attr4_color, (xx, yy, 10, 10))
    img = font.render(attr4_label, True, axis_label_color)
    scn.blit(img, (xx + 20, yy - 4))
# Attribute 5 Label
    yy += stepy
    pygame.draw.rect(scn, attr5_color, (xx, yy, 10, 10))
    img = font.render(attr5_label, True, axis_label_color)
    scn.blit(img, (xx + 20, yy - 4))
############################################################################################################
# Procedure to update the graph
############################################################################################################
def update_graph(pygame, scn, w, h, bdr, bdb, total_gens, gens_left, attr, attr_color, last_plot):
# Calculate the scale for the X and Y axis
    x_scale = w-bdr-axis_space
    y_scale = bdb-axis_space-axis_space
# Using the scale determine the next plot point
# NOTE: for the Y attribute value it is expected to be in the range 0.0 to 1.0
    x_plot = int(((gens_left)/(total_gens)) * x_scale)
    x_plot += axis_space
    x_plot = ((w - bdr+axis_space) - x_plot)
    y_plot = int((attr) * y_scale)
    y_plot = (h-axis_space) - y_plot
# Plot a simple point
    if (last_plot[0] != -1 and last_plot[1] != -1): # Draw line if not first point
        pygame.draw.aaline(scn, attr_color, [last_plot[0], last_plot[1]], [x_plot, y_plot-2])
# Need to flip here to ensure the last point is added
    pygame.display.flip()
# Return the last plot point
    return (x_plot, y_plot-2)
############################################################################################################
# Procedure to draw the food
############################################################################################################
def draw_hazard(pygame, scn, xw, yw, w, h, bdl, bdr, bdt, bdb, tiles, dg):
    stepx = (w-bdr-bdl)/xw
    stepy = (h-bdt-bdb)/yw
# Go through all the tiles
    for i in range(xw):
        for j in range(yw):
        # See if the tile has a hazard
            if tiles[i,j].hazard_type < 1:
                pass
            else:
            # Draw a border around the hazard square
                hazard_color = hazard1_color
                if (tiles[i, j].hazard_type == 2): hazard_color = hazard2_color
                if (tiles[i, j].hazard_type == 3): hazard_color = hazard3_color
                if (tiles[i, j].hazard_type == 4): hazard_color = hazard4_color
                if (tiles[i, j].hazard_type == 5): hazard_color = hazard5_color
                xy = (i,j)
                x = bdl + (xy[0] * stepx)
                y = bdt + (xy[1] * stepy)
                pygame.draw.line(scn, hazard_color, [x, y], [x+stepx, y])
                pygame.draw.line(scn, hazard_color, [x+stepx, y], [x+stepx, y+stepy])
                pygame.draw.line(scn, hazard_color, [x+stepx, y+stepy], [x, y+stepy])
                pygame.draw.line(scn, hazard_color, [x, y+stepy], [x, y])
############################################################################################################
# Simple CheckBox class
############################################################################################################
class checkbox():
    def __init__(self, pygame, color, x, y, width, height, outline=1, check=False, text="", size=24, font=None, textGap=2):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.outline = outline
        self.color = color
        self.check = check
        self.text = text
        self.font = pygame.font.SysFont(font, size)
        self.size = size
        self.textGap = textGap

    # Draws the checkbox
    def draw(self, pygame, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), self.outline)

        if self.text != "":
            text = self.font.render(self.text, 1, self.color)
            win.blit(text,
                     (self.x + self.width + self.textGap, self.y + (self.height / 2 - text.get_height() / 2)))

        if self.check:
            pygame.draw.line(win, self.color, (self.x, self.y),
                             (self.x + self.width - self.outline, self.y + self.height - self.outline))
            pygame.draw.line(win, self.color, (self.x - self.outline + self.width, self.y),
                             (self.x, self.y + self.height - self.outline))

    # Returns true if the given pos (either tuple or list) is over the box
    def isOver(self, pos):
        return pos[0] > self.x and pos[0] < self.x + self.width and pos[1] > self.y and pos[1] < self.y + self.height

    # Returns wHether the box is checked or not
    def isChecked(self):
        return self.check

    # Checks or unchecks the box
    def convert(self):
        self.check = not self.check
