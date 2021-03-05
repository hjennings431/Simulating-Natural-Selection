import numpy as np
creature_colour = (0,255,0)                 # Creature Colour
multiple_creature_colour = (255,255,255)    # Multiple occupancy tile colour
no_food_colour = (0,0,0)                    # Blank tile colour
food_colour = (64,64,64)                    # Normal food tile colour
tallfood_colour = (64,0,0)                  # Tall food tile colour
bushfood_colour = (255,32,0)                # Bush food tile colour
BackGroundColor = (0,0,0)                   # Define the background color
GridColor = (50,50,50)                      # Define the grid line color
BorderColor = (255,255,255)                 # Define the line color
key_label_color = (255,255,255)             # Color for the key labels
############################################################################################################
# Procedure to draw the grid for the display
############################################################################################################
def draw_grid(pygame, scn, xw, yw, w, h, bdl, bdr, bdt, bdb, drwgrd):
# Clear the current grid
    pygame.draw.rect(scn, BackGroundColor, (bdl, bdt, w, h))
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
            pygame.draw.line(scn, GridColor, [startx, bdt], [startx, h-bdb])
            startx += stepx
        for y in range(yw):
            pygame.draw.line(scn, GridColor, [bdl,starty], [w-bdr, starty])
            starty += stepy
############################################################################################################
# Procedure to draw the border for the display
############################################################################################################
def draw_border(pygame, scn, w, h, bdl, bdr, bdt, bdb ):
# Draw the border
    pygame.draw.line(scn, BorderColor, [bdl, bdt], [bdl, h-bdb])
    pygame.draw.line(scn, BorderColor, [w-bdr, bdt], [w-bdr, h-bdb])
    pygame.draw.line(scn, BorderColor, [bdl, bdt], [w-bdr, bdt])
    pygame.draw.line(scn, BorderColor, [bdl, h-bdb], [w-bdr, h-bdt])
############################################################################################################
# Simple Label
############################################################################################################
def SimpLabel(scn, font, label, value, x, y, tc, BdrTop):
    DisplayTxt = label + " = " + str(value)
    font.render_to(scn, (x, BdrTop+y), DisplayTxt, tc)
############################################################################################################
# Draw the food
############################################################################################################
def draw_food(pygame, scn, xw, yw, w, h, bdl, bdr, bdt, bdb, tiles, dg):
    if (dg): SizeAdj=1
    else: SizeAdj=0
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
                x = bdl + SizeAdj + (xy[0] * stepx)
                y = bdt + SizeAdj + (xy[1] * stepy)
                pygame.draw.rect(scn, fc, (x, y, stepx - SizeAdj, stepy - SizeAdj))
############################################################################################################
# Draw the creatures
############################################################################################################
def draw_creatures(pygame, scn, xw, yw, w, h, bdl, bdr, bdt, bdb, pop, dg ):
# Adjust the size deoending if there's a grid
    if (dg): SizeAdj=1
    else: SizeAdj=0
# Find the steps for each grid line
    stepx = (w-bdr-bdl)/xw
    stepy = (h-bdt-bdb)/yw
# Go through all the Bobs
    for i in range(len(pop)):
    # Get the current position
        xy=pop[i].position
    # Find the square to color in
        x = bdl + SizeAdj + (xy[0]*stepx)
        y = bdt + SizeAdj + (xy[1]*stepy)
    # Get the color of the current square and Make the bob white if square already occupied
        current_cc = scn.get_at((int(x), int(y)))
        r=current_cc[0]; g=current_cc[1]; b=current_cc[2]
        if (r==creature_colour[0] and g==creature_colour[1] and b==creature_colour[2]):
            nc = multiple_creature_colour
        else:
            nc = creature_colour
    # Color the square
        pygame.draw.rect(scn, nc, (x,y, stepx-SizeAdj,stepy-SizeAdj))
############################################################################################################
# Draw Key
############################################################################################################
def draw_key(pygame, scn, xw, yw, w, h, bdl, bdr, bdt, bdb ):
    stepy = 50
    xx = w-(bdr-20)
    yy = bdt + (stepy/2)
    font = pygame.font.SysFont(None, 24)
    pygame.draw.rect(scn, creature_colour, (xx, yy, 10, 10))
    img = font.render('Creatures', True, key_label_color); scn.blit(img, (xx+20, yy-4))
    yy += stepy; pygame.draw.rect(scn, multiple_creature_colour, (xx, yy, 10, 10))
    img = font.render('Creature Fight', True, key_label_color); scn.blit(img, (xx+20, yy-4))
    yy += stepy; pygame.draw.rect(scn, food_colour, (xx, yy, 10, 10))
    img = font.render('Normal Food', True, key_label_color); scn.blit(img, (xx+20, yy-4))
    yy += stepy; pygame.draw.rect(scn, tallfood_colour, (xx, yy, 10, 10))
    img = font.render('Tree Food', True, key_label_color); scn.blit(img, (xx+20, yy-4))
    yy += stepy; pygame.draw.rect(scn, bushfood_colour, (xx, yy, 10, 10))
    img = font.render('Bush Food', True, key_label_color); scn.blit(img, (xx + 20, yy - 4))
############################################################################################################
