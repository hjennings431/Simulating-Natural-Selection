import numpy as np
creature_colour = (0,255,0)
multiple_creature_colour = (51,204,51)
no_food_colour = (0,0,0)
food_colour = (64,64,64)


############################################################################################################
# Procedure to draw the grid for the display
############################################################################################################
def draw_grid(pygame, scn, xw, yw, w, h, bdl, bdr, bdt, bdb, lc, drwgrd):
# Clear the current grid
    pygame.draw.rect(scn, (0,0,0), (bdl, bdr, w, h))
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
            pygame.draw.line(scn, lc, [startx, bdt], [startx, h-bdb])
            startx += stepx
        for y in range(yw):
            pygame.draw.line(scn, lc, [bdl,starty], [w-bdr, starty])
            starty += stepy
############################################################################################################
# Procedure to draw the border for the display
############################################################################################################
def draw_border(pygame, scn, w, h, bdl, bdr, bdt, bdb, bc):
# Draw the border
    pygame.draw.line(scn, bc, [bdl, bdt], [bdl, h-bdb])
    pygame.draw.line(scn, bc, [w-bdr, bdt], [w-bdr, h-bdb])
    pygame.draw.line(scn, bc, [bdl, bdt], [w-bdr, bdt])
    pygame.draw.line(scn, bc, [bdl, h-bdb], [w-bdr, h-bdt])
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

    for i in range(xw):
        for j in range(yw):
            if tiles[i,j].food_type == 0:
                pass
            else:
                xy = (i,j)
                x = bdl + SizeAdj + (xy[0] * stepx)
                y = bdt + SizeAdj + (xy[1] * stepy)
                pygame.draw.rect(scn, food_colour, (x, y, stepx - SizeAdj, stepy - SizeAdj))

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
        g=current_cc[1]
        if g==255:
            nc = multiple_creature_colour
        else:
            nc = creature_colour
    # Color the square
        pygame.draw.rect(scn, nc, (x,y, stepx-SizeAdj,stepy-SizeAdj))
############################################################################################################
