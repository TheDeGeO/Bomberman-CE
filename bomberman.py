import pygame
import random
import time

pygame.init()

#Colors
grey = (75, 75, 75)

#Create rects with pictures
def img_block(img, size, coords, bg=grey, margin=20):
    img = pygame.transform.scale(img, size)
    img_rect = img.get_rect()

    block_sf = pygame.Surface((img_rect.width + margin, img_rect.height + margin))
    block_rect = block_sf.get_rect(center = coords)

    block_sf.fill(bg)
    block_sf.blit(img, (margin//2, margin//2))

    return (block_sf, block_rect)

#Create rects with text
def text_block(text, size, coords, bg=grey, fg=(250, 250, 250), margin=20):

    #Set monogram font (free on itch.io by datagoblin)
    monogram = pygame.font.Font("monogram.ttf", size)

    text_sf = monogram.render(text, False, fg)
    text_rect = text_sf.get_rect(center = coords)

    block_sf = pygame.Surface((text_rect.width + margin, text_rect.height + margin))
    block_rect = block_sf.get_rect(center = coords)
    block_sf.fill(bg)

    block_sf.blit(text_sf, (margin//2, margin//2))

    return(block_sf, block_rect)

#Create Buttons
def button(text, size, coords, bg=grey, fg=(250, 250, 250), margin=20):

    block = text_block(text, size, coords, bg, fg, margin)
    block_rect = block[1]
    #Make background darker if cursor and button are colliding
    dark_factor = 0.5
    if block_rect.collidepoint(cursor_cords):
        bg = (bg[0] * dark_factor, bg[1] * dark_factor, bg[2] * dark_factor)
        
    return text_block(text, size, coords, bg, fg, margin)

#Create text inputs
def text_input(text, size, coords, value, bg=grey, fg=(190, 190, 190), margin=20):
    
    block = text_block(text, size, coords, bg, fg, margin)
    block_rect = block[1]
    dark_factor = 1

    if not value:
        if block_rect.collidepoint(cursor_cords):
            dark_factor = 0.5
    
    else:
        text += "_"
        dark_factor = 0.35

    bg = (bg[0] * dark_factor, bg[1] * dark_factor, bg[2] * dark_factor)

    return text_block(text, size, coords, bg, fg, margin)
    

#Load images with custom size
def img_load(file_name, sub_folder, size):
    path = "images/" + sub_folder + "/" + file_name
    result = pygame.image.load(path)
    result = pygame.transform.scale(result, size)
    return result

#Play a song
def play_song(song, volume):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(song)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)
    
#Draw background repeting one tile
def draw_bg(img, tile_size, surface):
    width = surface.get_width()
    height = surface.get_height()

    def draw_bg_aux(img, tile_size, surface, width, height, x=0, y=0):
        if x >= width:
            x = 0
            y += tile_size
        elif y >= height:
            return 

        surface.blit(img, (x, y))
        x += tile_size

        return draw_bg_aux(img, tile_size, surface, width, height, x, y)

    return draw_bg_aux(img, tile_size, surface, width, height)

#Draw top bar with player name, lives, amount of bombs, points and time
def draw_top_bar(height, width, lives, name, bombs_amount, time, points, surface):
    top_bar_rect = pygame.Rect(0, 0, width, height)
    top_bar_sf = pygame.Surface((width, height))
    top_bar_sf.fill(grey)

    lives_block = text_block("Lives:" + str(lives), 30, (width*30//100, height*50//100))
    top_bar_sf.blit(lives_block[0],lives_block[1])

    name_block = text_block(name, 30, (width*10//100, height*50//100))
    top_bar_sf.blit(name_block[0],name_block[1])

    bombs_block = text_block("Bombs:" + str(bombs_amount), 30, (width*70//100, height*50//100))
    top_bar_sf.blit(bombs_block[0],bombs_block[1])

    time_block = text_block("Time:" + str(time), 30, (width*90//100, height*50//100))
    top_bar_sf.blit(time_block[0],time_block[1])

    points_block = text_block("Points:" + str(points), 30, (width*50//100, height*50//100))
    top_bar_sf.blit(points_block[0],points_block[1])

    surface.blit(top_bar_sf, top_bar_rect)

#Tilemap 21x16. Tile size = 32
tile_size = 32
tilemap = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

#Create random barriers
def add_barriers(tmap, surface, chance):
    rows = len(tmap) 
    cols = len(tmap[0]) 
    def add_barriers_aux(tmap, rows, cols, surface, chance, row=0, col=0, barriers=[]):
        if row >= rows:
            row = 0
            col += 1
        if col >= cols:
            return barriers

        randomizer = random.randint(0, chance)
        if ((row == 1 or row == 2) and (col == 1 or col == 2)):
            pass
        elif tmap[row][col] == 0 and randomizer == 0:
            y_c = row * tile_size + 64
            x_c = col * tile_size 
            barrier_rect = barrier_img.get_rect(y = y_c, x = x_c)
            #surface.blit(barrier_img, barrier_rect)
            #barrier_c = barrier_rect.center
            #barrier_rect.width -=10
            #barrier_rect.height -=10
            #barrier_rect.center = (barrier_c[0] - 5, barrier_c[1] - 5)

            barriers.append(barrier_rect)
            
        return add_barriers_aux(tmap, rows, cols, surface, chance, row+1, col, barriers)

    return add_barriers_aux(tmap, rows, cols, surface, chance)

#Draw barriers in barrier list
def draw_barriers(barriers, surface):
    n_of_barriers = len(barriers)
    def draw_barriers_aux(barriers, surface, n_of_barriers, pos=0):
        if pos >= n_of_barriers:
            return
        surface.blit(barrier_img, barriers[pos])

        return draw_barriers_aux(barriers, surface, n_of_barriers, pos+1)
    
    return draw_barriers_aux(barriers, surface, n_of_barriers)

#Add a key in relation to barriers index and assign it a rect
def add_key(barriers):
    n_of_barriers = len(barriers) - 2
    game_key = random.randint(0, n_of_barriers)
    game_key_rect = barriers[game_key]
    return game_key, game_key_rect, False
    

#Block images
block_img = img_load("wall.png", "icons", (32, 32))
barrier_img = img_load("barrier.png", "icons", (32, 32))

#Draw tilemap
def draw_tile_map(tmap, surface):
    rows = len(tmap)
    cols = len(tmap[0])

    def sub_draw_map(tmap, cols, rows, surface, col=0, row=0, blocks=[]):
        if row >= rows:
            row = 0
            col +=1
        if col >= cols:
            return blocks
        
        if tmap[row][col] == 1:
            y_c = row * tile_size + 64
            x_c = col * tile_size

            block_rect = block_img.get_rect(y = y_c, x = x_c)
            surface.blit(block_img, block_rect)
            #block_c = block_rect.center
            #block_rect.width -=10
            #block_rect.height -=10
            #block_rect.center = (block_c[0] - 5, block_c[1] - 5)
            blocks.append(block_rect)
        
        #elif tmap[row][col] == 0:
        row +=1
        return sub_draw_map(tmap, cols, rows, surface, col, row)
    
    return sub_draw_map(tmap, cols, rows, surface)

#Check for collitions with blocks
def collideblock(rect, blocks):
    n_of_c = len(blocks)

    def sub_collideblock(rect, blocks, n, pos=0):
        if pos >= n:
            return False
        if rect.colliderect(blocks[pos]):
            return True
        else:
            return sub_collideblock(rect, blocks, n, pos+1)
    
    return sub_collideblock(rect, blocks, n_of_c)

#Load sounds with volume
def load_sound(sound, volume):
    result = pygame.mixer.Sound("sounds/sfx/" + sound)
    result.set_volume(volume)

    return result

#Add a puntiation the ranks
def rank_points(top_points, point, nametag):
    n_of_times = len(top_points)

    def rank_points_aux(top_points, point, n_of_times, nametag, count=0):
        if count >= n_of_times:
            return top_points
        
        current_rank = top_points[count][0]
        if point > current_rank or current_rank == 0:
            top_points.insert(count, [point, nametag])
            return top_points
        else:
            return rank_points_aux(top_points, point, n_of_times, nametag, count+1)
        
    return rank_points_aux(top_points, point, n_of_times, nametag)

#Add points around map
def add_points(tmap, chance):
    rows = len(tmap)
    cols = len(tmap[0])

    def add_points_aux(tmap, chance, rows, cols, row=0, col=0, points_list=[]):
        if row >= rows:
            row = 0
            col += 1
        if col >= cols:
            return points_list
        
        randomizer = random.randint(0, chance)
        if randomizer == 0:
            point_rect = points_img.get_rect()
            point_rect.x = col * tile_size
            point_rect.y = row * tile_size + top_bar_height
            points_list.append(point_rect)
        
        return add_points_aux(tmap, chance, rows, cols, row+1, col, points_list)
    
    return add_points_aux(tmap, chance, rows, cols)
        
#Draw points in points list
def draw_points(surface, points_list):
    n_of_points = len(points_list) 

    def draw_points_aux(surface, points_list, n_of_points, counter=0):
        if counter >= n_of_points:
            return

        surface.blit(points_img, points_list[counter])

        return draw_points_aux(surface, points_list, n_of_points, counter+1)

    return draw_points_aux(surface, points_list, n_of_points)


        

#Clock
clock = pygame.time.Clock()

#Window data
window_width = 672
window_height = 480
#window_width = 800
#window_height = 600
top_bar_height = 64
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('BOMBERMAN')

#Images
title_screen_tile = img_load("title_bg.png", "bgs", (tile_size * 3, tile_size * 3))
settings_screen_tile = img_load("setting_bg.png", "bgs", (tile_size * 3, tile_size * 3))
stage_1_bg = img_load("wall.png", "icons", (tile_size * 3, tile_size * 3))
stage_2_bg = img_load("wall2.png", "icons", (tile_size * 3, tile_size * 3))
stage_3_bg = img_load("wall3.png", "icons", (tile_size * 3, tile_size * 3))

grass = img_load("grass.jpg", "bgs", (tile_size, tile_size))

coder_img = img_load("coder.jpg", "about", (500, 500))

#Default settings
volume = 0.1
skin = "brown"
default_nametag = "Ningen"
nametag = default_nametag

#Sounds and Music
title_music = "sounds/music/waltz2.mp3"
stage_1_music = "sounds/music/paranoid.mp3"
stage_2_music = "sounds/music/hole.mp3"
stage_3_music = "sounds/music/moonlight.mp3"

win_music = "sounds/music/Fancy.mp3"
game_over_music = "sounds/music/Erase This.mp3"

click_sound1 = load_sound("button_click1.wav", volume)
click_sound2 = load_sound("button_click2.wav", volume)

step_sound = load_sound("step.wav", volume)

explosion_sound = load_sound("explosion1.wav", volume)

death_sound = load_sound("died.wav", volume)

key_sound = load_sound("key.wav", volume)
point_sound = load_sound("point.wav", volume)

hurt_sound = load_sound("hurt.wav", volume)

door_sound = load_sound("door.wav", volume)

#Icons
bomb_img = img_load("bomb.png", "icons", (32, 32))
game_key_img = img_load("key.png", "icons", (32, 32))
lock_img = img_load("lock.png", "icons", (32, 32))
points_img = img_load("coffee.png", "icons", (32, 32))

music_on_icon = img_load("music_on.png", "icons", (32, 32))
music_off_icon = img_load("music_off.png", "icons", (32, 32))
music_icon = music_on_icon

#Explosion size and animation sprites
explosion_size = 2.75
explosion_img_1 = img_load("explosion1.png", "animation/explosion", (32*explosion_size, 32*explosion_size))
explosion_img_2 = img_load("explosion2.png", "animation/explosion", (32*explosion_size, 32*explosion_size))
explosion_img_3 = img_load("explosion3.png", "animation/explosion", (32*explosion_size, 32*explosion_size))
explosion_img_4 = img_load("explosion4.png", "animation/explosion", (32*explosion_size, 32*explosion_size))

#Load global player sprites
def load_skin(skin):
    global player_down, player_down1, player_down2
    global player_up, player_up1, player_up2
    global player_left, player_left1, player_left2
    global player_right, player_right1, player_right2
    global player_img, last_direction, player, player_default

    player_down = img_load("down.png", "player/" + skin, (tile_size, tile_size))
    player_down1 = img_load("down1.png", "player/" + skin, (tile_size, tile_size))
    player_down2 = img_load("down2.png", "player/" + skin, (tile_size, tile_size))

    player_up = img_load("up.png", "player/" + skin, (tile_size, tile_size))
    player_up1 = img_load("up1.png", "player/" + skin, (tile_size, tile_size))
    player_up2 = img_load("up2.png", "player/" + skin, (tile_size, tile_size))

    player_left = img_load("left.png", "player/" + skin, (tile_size, tile_size))
    player_left1 = img_load("left1.png", "player/" + skin, (tile_size, tile_size))
    player_left2 = img_load("left2.png", "player/" + skin, (tile_size, tile_size))

    player_right = pygame.transform.flip(player_left, True, False)
    player_right1 = pygame.transform.flip(player_left1, True, False)
    player_right2 = pygame.transform.flip(player_left2, True, False)

    player_img = player_down
    last_direction = player_down

    player_default = player_down.get_rect(x = tile_size, y = tile_size + top_bar_height)

    player_default = player_default.inflate(-10, -10)

    player = player_default

load_skin(skin)

#Load enemy sprites
##Scout
scout_down = img_load("down.png", "scout", (32, 32))
scout_down1 = img_load("down1.png", "scout", (32, 32))
scout_down2 = img_load("down2.png", "scout", (32, 32))

scout_up = img_load("up.png", "scout", (32, 32))
scout_up1 = img_load("up1.png", "scout", (32, 32))
scout_up2 = img_load("up2.png", "scout", (32, 32))

scout_left = img_load("left.png", "scout", (32, 32))
scout_left1 = img_load("left1.png", "scout", (32, 32))
scout_left2 = img_load("left2.png", "scout", (32, 32))

scout_right = pygame.transform.flip(scout_left, True, False)
scout_right1 = pygame.transform.flip(scout_left1, True, False)
scout_right2 = pygame.transform.flip(scout_left2, True, False)

scout_img = scout_down
scour_last_direction = scout_down

##Conjurer 
conjurer_down = img_load("down.png", "conjurer", (32, 32))
conjurer_down1 = img_load("down1.png", "conjurer", (32, 32))
conjurer_down2 = img_load("down2.png", "conjurer", (32, 32))

conjurer_up = img_load("up.png", "conjurer", (32, 32))
conjurer_up1 = img_load("up1.png", "conjurer", (32, 32))
conjurer_up2 = img_load("up2.png", "conjurer", (32, 32))

conjurer_left = img_load("left.png", "conjurer", (32, 32))
conjurer_left1 = img_load("left1.png", "conjurer", (32, 32))
conjurer_left2 = img_load("left2.png", "conjurer", (32, 32))

conjurer_right = pygame.transform.flip(conjurer_left, True, False)
conjurer_right1 = pygame.transform.flip(conjurer_left1, True, False)
conjurer_right2 = pygame.transform.flip(conjurer_left2, True, False)

conjurer_img = conjurer_down
conjurer_last_direction = conjurer_down

##Add scouts
def add_scouts(tmap, blocks, chance):
    rows = len(tmap)
    cols = len(tmap[0])

    def add_scouts_aux(tmap, blocks, chance, rows, cols, scouts=[], row=0, col=0):
        if row >= rows:
            row = 0
            col += 1
        if col >= cols:
            return scouts
        
        scout_x = col * tile_size
        scout_y = row * tile_size + top_bar_height
        scout_rect = scout_img.get_rect(x = scout_x, y = scout_y)
        if collideblock(scout_rect, blocks):
            pass
        elif ((row in range(1, 3)) and (col in range (1, 3))):
            pass
        else:
            if random.randint(0, chance) == 0:
                scouts.append(scout_rect)

        return add_scouts_aux(tmap, blocks, chance, rows, cols, scouts, row+1, col)
    
    return add_scouts_aux(tmap, blocks, chance, rows, cols)

#Draw scouts in scouts list
def draw_scouts(scouts, scouts_img, surface):
    n_of_scouts = len(scouts)

    def draw_scouts_aux(scouts, surface, n_of_scouts, counter):
        if counter >= n_of_scouts:
            return
        
        surface.blit(scouts_img[counter], scouts[counter])
        return draw_scouts_aux(scouts, surface, n_of_scouts, counter + 1)
    
    return draw_scouts_aux(scouts, surface, n_of_scouts, 0)

#Add conjurers
def add_conjurers(tmap, blocks, chance):
    rows = len(tmap)
    cols = len(tmap[0])

    def add_conjurers_aux(tmap, blocks, chance, rows, cols, conjs=[], row=0, col=0):
        if row >= rows:
            row = 0
            col += 1
        if col >= cols:
            return conjs
        
        conjurer_x = col * tile_size
        conjurer_y = row * tile_size + top_bar_height
        conjurer_rect = conjurer_img.get_rect(x = conjurer_x, y = conjurer_y)
        if collideblock(conjurer_rect, blocks):
            pass
        elif ((row in range(1, 3)) and (col in range (1, 3))):
            pass
        else:
            if random.randint(0, chance) == 0:
                conjs.append(conjurer_rect)

        return add_conjurers_aux(tmap, blocks, chance, rows, cols, conjs, row+1, col)
    
    return add_conjurers_aux(tmap, blocks, chance, rows, cols)

#Draw conjurers in conjs list
def draw_conjurers(conjs, conjs_imgs, surface):
    n_of_conjs = len(conjs)

    def draw_conjurers_aux(conjs, surface, n_of_conjs, counter):
        if counter >= n_of_conjs:
            return
        
        surface.blit(conjs_imgs[counter], conjs[counter])
        return draw_conjurers_aux(conjs, surface, n_of_conjs, counter + 1)
    
    return draw_conjurers_aux(conjs, surface, n_of_conjs, 0)


#Randomly move enemies

def move_scouts(speed, scouts, blocks):
    n_of_scouts = len(scouts)

    def move_scouts_aux(speed, scouts, blocks, n_of_scouts, scouts_imgs, count=0):
        if count >= n_of_scouts:
            return scouts
        
        current_scout = scouts[count]
        randomizer = random.randint(1, 150)
        if randomizer == 1:
            current_scout.move_ip(speed, 0)
            scouts_imgs[count] = scout_right
            if collideblock(current_scout, blocks):
                current_scout.move_ip(speed*-1, 0)
        elif randomizer == 2:
            current_scout.move_ip(0, speed)
            scouts_imgs[count] = scout_down
            if collideblock(current_scout, blocks):
                current_scout.move_ip(0, speed*-1)
        elif randomizer == 3:
            current_scout.move_ip(speed*-1, 0)
            scouts_imgs[count] = scout_left
            if collideblock(current_scout, blocks):
                current_scout.move_ip(speed, 0)
        elif randomizer == 4:
            current_scout.move_ip(0, speed*-1)
            scouts_imgs[count] = scout_up
            if collideblock(current_scout, blocks):
                current_scout.move_ip(0, speed)
        

        return move_scouts_aux(speed, scouts, blocks, n_of_scouts, scouts_imgs, count+1)
    
    return move_scouts_aux(speed, scouts, blocks, n_of_scouts, scouts_imgs)

#Randomly move conjurers
def move_conjurers(speed, conjs, blocks):
    n_of_conjs = len(conjs)

    def move_conjurers_aux(speed, conjs, blocks, n_of_conjs, conjs_imgs, count=0):
        if count >= n_of_conjs:
            return conjs
        
        current_conj = conjs[count]
        randomizer = random.randint(1, 150)
        if randomizer == 1:
            current_conj.move_ip(speed, 0)
            conjs_imgs[count] = conjurer_right
            if collideblock(current_conj, blocks):
                current_conj.move_ip(speed*-1, 0)
        elif randomizer == 2:
            current_conj.move_ip(0, speed)
            conjs_imgs[count] = conjurer_down
            if collideblock(current_conj, blocks):
                current_conj.move_ip(0, speed*-1)
        elif randomizer == 3:
            current_conj.move_ip(speed*-1, 0)
            conjs_imgs[count] = conjurer_left
            if collideblock(current_conj, blocks):
                current_conj.move_ip(speed, 0)
        elif randomizer == 4:
            current_conj.move_ip(0, speed*-1)
            conjs_imgs[count] = conjurer_up
            if collideblock(current_conj, blocks):
                current_conj.move_ip(0, speed)
        
        return move_conjurers_aux(speed, conjs, blocks, n_of_conjs, conjs_imgs, count+1)
    
    return move_conjurers_aux(speed, conjs, blocks, n_of_conjs, conjs_imgs)
        
    


#Player data
player_speed = 3
last_movement_time = 0
lives = 5
bombs_amount = 100
player_has_key = False

#Bombs data
bombs = []
bomb_cooldown = 1000
bomb_time = 0
explosion_cooldown = 200
explosion_state = 0
explosion_time = 0

#Add a bomb at playr location
def add_bombs(player_rect, bombs):
    bomb_rect = bomb_img.get_rect(center = player_rect.center)
    bombs.append(bomb_rect)

#Draw bombs in bomb list
def draw_bombs(bombs, surface):
    n_of_bombs = len(bombs)

    def draw_bombs_aux(bombs, surface, n_of_bombs, counter):
        if counter >= n_of_bombs:
            return
        
        surface.blit(bomb_img, bombs[counter])
        return draw_bombs_aux(bombs, surface, n_of_bombs, counter + 1)
    
    return draw_bombs_aux(bombs, surface, n_of_bombs, 0)

#Destroy barriers in explosion radius and update key found value
def destroy_barriers(explosion, barriers, game_key_rect, game_key_found):
    #nonlocal game_key, game_key_found

    n_of_barriers = len(barriers) 

    def destroy_barriers_aux(explosion, barriers, n_of_barriers, count, game_key_rect, game_key_found):
        
        if count >= n_of_barriers:
            return game_key_found

        if explosion.colliderect(barriers[count]):
            current_barrier = barriers[count]
            barriers.pop(barriers.index(current_barrier))
            n_of_barriers -= 1
            if current_barrier == game_key_rect:
                game_key_found = True
        else:
            count += 1
        
        return destroy_barriers_aux(explosion, barriers, n_of_barriers, count, game_key_rect, game_key_found)
    
    return destroy_barriers_aux(explosion, barriers, n_of_barriers, 0, game_key_rect, game_key_found)

#Destroy enemies in explosion radius
def destroy_enemies(explosion, enemies):
    n_of_enemies = len(enemies)

    def destroy_enemies_aux(explosion, enemies, n_of_enemies, count):
        if count >= n_of_enemies:
            return
        
        if explosion.colliderect(enemies[count]):
            enemies.pop(enemies.index(enemies[count]))
            n_of_enemies -= 1
        else:
            count += 1
        
        return destroy_enemies_aux(explosion, enemies, n_of_enemies, count)
    
    return destroy_enemies_aux(explosion, enemies, n_of_enemies, 0)

#Collect points
def collect_points(points_list, points, player_rect):
    n_of_points = len(points_list)

    def collect_points_aux(points_list, points, player_rect, n_of_points, count=0):
        if count >= n_of_points:
            return points
        
        if player_rect.colliderect(points_list[count]):
            points_list.pop(points_list.index(points_list[count]))
            n_of_points -= 1
            points += 1
            point_sound.play()
        else:
            count += 1
        
        return collect_points_aux(points_list, points, player_rect, n_of_points, count)
    
    return collect_points_aux(points_list, points, player_rect, n_of_points)


#Main loop
screen = "title"
stage = 1
song = "none"
top_points = [[0, "Fulano"], [0, "Mengano"], [0, "Zutano"], [0, "Perengano"], [0, "Citano"]]

run = True
while run:

    #Get cursor cords, events and time
    cursor_cords = pygame.mouse.get_pos()
    event = pygame.event.poll()
    current_time = pygame.time.get_ticks()

    #Title screen
    if screen == "title":

        #play title song
        if song != "title":
            song = "title"
            play_song(title_music, volume)

        #Set background
        window.fill((0, 0, 0))
        draw_bg(title_screen_tile, tile_size * 3, window)

        #Add title
        title = text_block("BOMBERMAN", 50, (window_width//2, 100))
        window.blit(title[0], title[1])

        #Add Play button
        play = button("Play", 30, (window_width//2, 225))
        window.blit(play[0], play[1])

        #Add Settings Button
        settings = button("Settings", 30, (window_width//2, 290))
        window.blit(settings[0], settings[1])

        #Add Rank button
        ranks = button("Ranks", 30, (window_width//2, 355))
        window.blit(ranks[0], ranks[1])

        #Add About button
        about = button("About", 30, (window_width//2, 420))
        window.blit(about[0], about[1])

        #Title screen event handler
        if event.type == pygame.MOUSEBUTTONDOWN:
            if settings[1].collidepoint(cursor_cords):
                click_sound1.play()
                screen = "settings"
            elif play[1].collidepoint(cursor_cords):
                click_sound1.play()
                screen = "game"
                game_start_time = current_time
            elif ranks[1].collidepoint(cursor_cords):
                click_sound1.play()
                screen = "ranks"
            elif about[1].collidepoint(cursor_cords):
                click_sound1.play()
                screen = "about"

    #Settings screen
    elif screen == "settings":
        #Set background
        window.fill((0, 0, 0))
        draw_bg(settings_screen_tile, tile_size * 3, window)

        #Set settings text
        settins_text = text_block("SETTINGS", 50, (window_width//2, window_height//2 - 200))
        window.blit(settins_text[0], settins_text[1])

        #Add back button
        back = button("Back", 30, (window_width//2, window_height - 50))
        window.blit(back[0], back[1])

        #Add skin settings
        skin_text = text_block("Skin:", 30, (200, 175))
        window.blit(skin_text[0], skin_text[1])

        #Set interactive skin display
        skin_display = img_block(player_down, (60, 60), (200, 250))
        window.blit(skin_display[0], skin_display[1])

        #Set next skin buttons
        change_skin = button("Next", 40, (200, 325))
        window.blit(change_skin[0], change_skin[1])

        #Add player name settings
        name_text = text_block("Nametag:", 30, (325, 175))
        window.blit(name_text[0], name_text[1])

        #Set interactive name display
        if "nametag_value" not in globals():
            nametag_value = False
        if not nametag and nametag_value == False:
            nametag = default_nametag
        nametag_box = text_input(nametag, 30, (325, 250), nametag_value)
        window.blit(nametag_box[0], nametag_box[1])

        #Add sound settings
        music_text = text_block("Music", 30, (450, 175))
        window.blit(music_text[0], music_text[1])

        #Set interactive music settings
        music_icon_display = img_block(music_icon, (60, 60), (450, 250))
        window.blit(music_icon_display[0], music_icon_display[1])

        if volume == 0:
            music_text = "Off"
        else:
            music_text = "On"
        music_button = button(music_text, 40, (450, 325))
        window.blit(music_button[0], music_button[1])


    #Settings event handler
        if event.type == pygame.MOUSEBUTTONDOWN:
            #Back button
            if back[1].collidepoint(cursor_cords):
                click_sound2.play()
                nametag_value = False
                nametag_value = False
                screen = "title"
            #Skin button
            elif change_skin[1].collidepoint(cursor_cords):
                if skin == "brown":
                    click_sound1.play()
                    skin = "blue"
                elif skin == "blue":
                    click_sound1.play()
                    skin = "pink"
                else:
                    click_sound2.play()
                    skin = "brown"
                load_skin(skin)
            #Nametag box
            elif nametag_box[1].collidepoint(cursor_cords):
                click_sound1.play()
                nametag_value = True
                nametag = ""
            elif nametag_value and not nametag_box[1].collidepoint(cursor_cords):
                click_sound2.play()
                nametag_value = False
            elif music_button[1].collidepoint(cursor_cords):
                if volume > 0:
                    click_sound2.play()
                    volume = 0
                    music_text = "Off"
                    music_icon = music_off_icon
                else:
                    click_sound1.play()
                    volume = 0.1
                    music_text = "On"
                    music_icon = music_on_icon
                pygame.mixer.music.set_volume(volume)
        #Nametag input
        if event.type == pygame.KEYDOWN:
            if nametag_value:
                if event.key == pygame.K_RETURN:
                    click_sound1.play()
                    nametag_value = False
                    nametag_value = False
                elif event.key == pygame.K_BACKSPACE:
                    nametag =  nametag[:-1]
                else:
                    nametag += event.unicode


    #Game screen
    elif screen == "game":

        #End game if player has no lifes left
        if lives <= 0 or bombs_amount <= 0:
            death_sound.play()
            screen = "game over"

        #Get match time
        game_time = current_time - game_start_time

        #Stage 1 intro screen
        if song == "title":
            #Play music
            play_song(stage_1_music, volume/3)
            song = "stage 1"
            stage = 1

            #Set background and text
            window.fill((0, 0, 0))
            draw_bg(stage_1_bg, tile_size * 3, window)
            stage_text = text_block("Stage 1", 50, (window_width//2, window_height//2))
            window.blit(stage_text[0], stage_text[1])

            pygame.display.update()
            time.sleep(2)

        #Set background
        window.fill((0, 0, 0))
        bg = draw_bg(grass, tile_size, window)
        #window.blit(bg, (0,top_bar))

        #Add points around map
        if "points_list" not in globals():
            points = 0
            points_list = add_points(tilemap, 8)
        
        #Draw points
        draw_points(window, points_list)

        #Draw top bar
        top_bar = draw_top_bar(top_bar_height, window_width, lives, nametag, bombs_amount, game_time//1000, points, window)
        

        #Draw tilemap
        blocks = draw_tile_map(tilemap, window)

        #Draw barriers
        if "barriers" not in globals():
            barriers = add_barriers(tilemap, window, 3)
        draw_barriers(barriers, window)

        #Add key
        if "game_key" not in globals():
            game_key, game_key_rect, game_key_found = add_key(barriers)
        
        #Draw key
        if game_key_found and not player_has_key:
            window.blit(game_key_img, game_key_rect)

        #Draw door
        if "door_rect" not in globals():
            door_rect = barriers[-1]
            barriers.pop(-1)

        window.blit(lock_img, door_rect)


        #Draw player
        player_fk_rect = player.inflate(10, 10)
        window.blit(player_img, player_fk_rect)

        #Define all obstacles
        obstacles = blocks + barriers

        #Add enemies
        if "scouts" not in globals():
            scouts = add_scouts(tilemap, obstacles, 10)
            scouts_imgs = [scout_down] * len(scouts)
            scout_speed = 32

            conjurer_speed = 32
            conjurers = []
            conjs_imgs = []

        #Move scouts
        scouts = move_scouts(scout_speed, scouts, obstacles)
        conjurers = move_conjurers(conjurer_speed, conjurers, blocks)

        #Draw scouts
        draw_scouts(scouts, scouts_imgs, window)
        draw_conjurers(conjurers, conjs_imgs, window)

        #Draw bombs
        draw_bombs(bombs, window)

        #Explode bombs
        if not bombs:
            pass
        elif current_time - bomb_time < bomb_cooldown:
            pass
        else:
            explosion_sound.play()
            #Create explosion rect
            explosion = explosion_img_1.get_rect()
            explosion.center = bombs[0].center
            #Check if explosion hurts player
            if player.colliderect(explosion):
                hurt_sound.play()
                lives -= 1
                player.x = tile_size
                player.y = tile_size + top_bar_height
            #Set values for explosion animation
            explosion_state = 1
            bomb_time = current_time
            #Remove bomb
            bombs.pop(0)
            #Destroy barriers, scouts and conjurers, and update game_key_found
            game_key_found = destroy_barriers(explosion, barriers, game_key_rect, game_key_found)
            destroy_enemies(explosion, scouts)
            destroy_enemies(explosion, conjurers)


        #Draw explosion
        #End of explosion
        if explosion_state == 0:
            pass
        #First sprite
        elif explosion_state == 1:
            window.blit(explosion_img_1, explosion)
            if current_time - explosion_time > explosion_cooldown:
                explosion_state = 2
                explosion_time = current_time
        #Second sprite
        elif explosion_state == 2:
            window.blit(explosion_img_2, explosion)
            if current_time - explosion_time > explosion_cooldown:
                explosion_state = 3
                explosion_time = current_time
        #Third sprite
        elif explosion_state == 3:
            window.blit(explosion_img_3, explosion)
            if current_time - explosion_time > explosion_cooldown:
                explosion_state = 4
                explosion_time = current_time
        #Fourth sprite
        elif explosion_state == 4:
            window.blit(explosion_img_4, explosion)
            if current_time - explosion_time > explosion_cooldown:
                explosion_state = 0
                explosion_time = current_time


        #Player movement
        key = pygame.key.get_pressed()
        #Up movement
        if key[pygame.K_w]:
            player.move_ip(0,player_speed*-1)
            if current_time - last_movement_time > 300:
                if player_img == player_up1:
                    player_img = player_up2
                else:
                    player_img = player_up1
                step_sound.play()
                last_movement_time = pygame.time.get_ticks()
            last_direction = player_up
            if collideblock(player, obstacles):
                player.move_ip(0,player_speed)

        #Down movement 
        elif key[pygame.K_s]:
            player.move_ip(0,player_speed)
            if current_time - last_movement_time > 300:
                if player_img == player_down1:
                    player_img = player_down2
                else:
                    player_img = player_down1
                step_sound.play()
                last_movement_time = pygame.time.get_ticks()
            last_direction = player_down
            if collideblock(player, obstacles):
                player.move_ip(0,player_speed*-1)

        #Left movement
        elif key[pygame.K_a]:
            player.move_ip(player_speed*-1,0)
            if current_time - last_movement_time > 300:
                if player_img == player_left1:
                    player_img = player_left2
                else:
                    player_img = player_left1
                last_movement_time = pygame.time.get_ticks()
            last_direction = player_left
            if collideblock(player, obstacles):
                player.move_ip(player_speed,0)

        #Right movement
        elif key[pygame.K_d]:
            player.move_ip(player_speed,0)
            if current_time - last_movement_time > 300:
                if player_img == player_right1:
                    player_img = player_right2
                else:
                    player_img = player_right1
                step_sound.play()
                last_movement_time = pygame.time.get_ticks()
            last_direction = player_right
            if collideblock(player, obstacles):
                player.move_ip(player_speed*-1,0)

        else:
            player_img = last_direction
        
        #Collect key
        if player.colliderect(game_key_rect):
            #play sound for key
            if not player_has_key:
                key_sound.play()
            player_has_key = True

        #Enemies hurt player
        if "hurt_time" not in globals():
            hurt_time = current_time
            hurt_cooldown = 1000
        all_enemies = scouts + conjurers
        if collideblock(player, all_enemies) and current_time - hurt_time > hurt_cooldown:
            hurt_sound.play()
            hurt_time = current_time
            lives -= 1
            player.x = tile_size
            player.y = tile_size + top_bar_height
        
        #Player can collect points
        points = collect_points(points_list, points, player)
        

        
        #Level progression
        if player.colliderect(door_rect) and player_has_key:
            #play sound for door
            door_sound.play()

            #From stage 1 to stage 2
            if stage == 1:

                stage = 2

                #Reduce max lives
                if lives < 4:
                    lives = 4

                #Reduce max bombs
                if bombs_amount > 70:
                    bombs_amount = 70

                #Play stage 2 music
                play_song(stage_2_music, volume)

                #Load stage 2 assets
                block_img = img_load("wall2.png", "icons", (tile_size, tile_size))
                barrier_img = img_load("barrier2.png", "icons", (tile_size, tile_size))
                grass = img_load("grass2.png", "bgs", (tile_size, tile_size))

                #Add new points
                points_list = add_points(tilemap, 8)

                #Add new barriers
                barriers = add_barriers(tilemap, window, 2)
                
                #Add new door
                door_rect = barriers[-1]
                barriers.pop(-1)

                #Add new key
                player_has_key = False
                game_key, game_key_rect, game_key_found = add_key(barriers)

                #Reset player position
                player.x = tile_size
                player.y = tile_size + top_bar_height

                #Add new enemies
                scouts = add_scouts(tilemap, obstacles, 20)
                conjurers = add_conjurers(tilemap, obstacles, 20)
                scouts_imgs = [scout_down] * len(scouts)
                conjs_imgs = [conjurer_down] * len(conjurers)

                #Stage 2 intro screen
                window.fill((0, 0, 0))
                draw_bg(stage_2_bg, tile_size * 3, window)
                stage_text = text_block("Stage 2", 50, (window_width//2, window_height//2))
                window.blit(stage_text[0], stage_text[1])

                pygame.display.update()
                time.sleep(2)

            #From stage 2 to stage 3
            elif stage == 2:
                stage = 3

                #Reduce max lives
                if lives < 3:
                    lives = 3

                #Reduce max bombs
                if bombs_amount > 40:
                    bombs_amount = 40

                #Play stage 3 music
                play_song(stage_3_music, volume)

                #Load stage 3 assets
                block_img = img_load("wall3.png", "icons", (tile_size, tile_size))
                barrier_img = img_load("barrier3.png", "icons", (tile_size, tile_size))
                grass = img_load("grass3.png", "bgs", (tile_size, tile_size))

                #Add new points
                points_list = add_points(tilemap, 8)

                #Add new barriers
                barriers = add_barriers(tilemap, window, 2)
                
                #Add new door
                door_rect = barriers[-1]
                barriers.pop(-1)

                #Add new key
                player_has_key = False
                game_key, game_key_rect, game_key_found = add_key(barriers)

                #Reset player position
                player.x = tile_size
                player.y = tile_size + top_bar_height

                #Add new enemies
                scouts = add_scouts(tilemap, obstacles, 16)
                conjurers = add_conjurers(tilemap, obstacles, 20)
                scouts_imgs = [scout_down] * len(scouts)
                conjs_imgs = [conjurer_down] * len(conjurers)

                #Stage 3 intro screen
                window.fill((0, 0, 0))
                draw_bg(stage_3_bg, tile_size * 3, window)
                stage_text = text_block("Stage 3", 50, (window_width//2, window_height//2))
                window.blit(stage_text[0], stage_text[1])

                pygame.display.update()
                time.sleep(2)
            
            #From stage 3 to win screen
            elif stage == 3:
                screen = "win screen"
                
                #Restart game data and assets to stage 1
                block_img = img_load("wall.png", "icons", (tile_size, tile_size))
                barrier_img = img_load("barrier.png", "icons", (tile_size, tile_size))
                grass = img_load("grass.jpg", "bgs", (tile_size, tile_size))
                barriers = add_barriers(tilemap, window, 3)
                game_key, game_key_rect, game_key_found = add_key(barriers)
                player_has_key = False
                door_rect = barriers[-1]
                barriers.pop(-1)

                player.x = tile_size
                player.y = tile_size + top_bar_height


        #Bomb placements
        if key[pygame.K_x]:
            if len(bombs) < 2:
                pass
            #Bomb cooldown
            if current_time - bomb_time < bomb_cooldown:
                pass
            else:
                add_bombs(player, bombs)
                bomb_time = current_time
                bombs_amount -= 1
    
    #Game over screen
    elif screen == "game over":

        #Play game over music
        if song != "game over":
            play_song(game_over_music, volume)
            song = "game over"

        #Draw game over bg
        window.fill((0, 0, 0))
        if stage == 1:
            draw_bg(stage_1_bg, tile_size * 3, window)
        elif stage == 2:
            draw_bg(stage_2_bg, tile_size * 3, window)
        elif stage == 3:
            draw_bg(stage_3_bg, tile_size * 3, window)

        #Draw game over text
        game_over_text = text_block("Game Over", 50, (window_width//2, window_height//2 - 100))
        time_text = text_block("Time:" + str(round(game_time/1000, 2)), 30, (window_width//2, window_height//2))
        points_text = text_block("Points:" + str(points), 30, (window_width//2, window_height//2 + 50))
        notice_text = text_block("Press Enter to restart", 30, (window_width//2, window_height//2 + 100))

        window.blit(game_over_text[0], game_over_text[1])
        window.blit(time_text[0], time_text[1])
        window.blit(points_text[0], points_text[1])
        window.blit(notice_text[0], notice_text[1])


        pygame.display.update()

        #Restart game
        key = pygame.key.get_pressed()
        if key[pygame.K_RETURN]:
            block_img = img_load("wall.png", "icons", (tile_size, tile_size))
            barrier_img = img_load("barrier.png", "icons", (tile_size, tile_size))
            grass = img_load("grass.jpg", "bgs", (tile_size, tile_size))

            points_list = add_points(tilemap, 8)

            barriers = add_barriers(tilemap, window, 3)
            game_key, game_key_rect, game_key_found = add_key(barriers)
            player_has_key = False
            door_rect = barriers[-1]
            barriers.pop(-1)

            scouts = add_scouts(tilemap, obstacles, 10)
            scouts_imgs = [scout_down] * len(scouts)
            scout_speed = 32

            bombs = []
            explosion_state = 0

            conjurer_speed = 32
            conjurers = []
            conjs_imgs = []

            lives = 3
            points = 0
            game_time = 0
            bombs_amount = 100

            player.x = tile_size
            player.y = tile_size + top_bar_height

            stage = 1
            screen = "title"
    
    #Win screen
    elif screen == "win screen":

        #Play win music
        if song != "win":
            play_song(win_music, volume)
            song = "win"

        #Draw win bg
        window.fill((0, 0, 0))
        if stage == 1:
            draw_bg(stage_1_bg, tile_size * 3, window)
        elif stage == 2:
            draw_bg(stage_2_bg, tile_size * 3, window)
        elif stage == 3:
            draw_bg(stage_3_bg, tile_size * 3, window)

        #Draw win text
        win_text = text_block("YOU WIN", 50, (window_width//2, window_height//2 - 100))
        time_text = text_block("Time:" + str(round(game_time/1000, 2)), 30, (window_width//2, window_height//2))
        points_text = text_block("Points:" + str(points), 30, (window_width//2, window_height//2 + 50))
        notice_text = text_block("Press Enter to restart", 30, (window_width//2, window_height//2 + 100))

        window.blit(win_text[0], win_text[1])
        window.blit(time_text[0], time_text[1])
        window.blit(points_text[0], points_text[1])
        window.blit(notice_text[0], notice_text[1])

        pygame.display.update()

        #Restart game and add rank position
        key = pygame.key.get_pressed()
        if key[pygame.K_RETURN]:
            block_img = img_load("wall.png", "icons", (tile_size, tile_size))
            barrier_img = img_load("barrier.png", "icons", (tile_size, tile_size))
            grass = img_load("grass.jpg", "bgs", (tile_size, tile_size))

            points_list = add_points(tilemap, 8)

            barriers = add_barriers(tilemap, window, 3)
            game_key, game_key_rect, game_key_found = add_key(barriers)
            player_has_key = False
            door_rect = barriers[-1]
            barriers.pop(-1)

            scouts = add_scouts(tilemap, obstacles, 10)
            scouts_imgs = [scout_down] * len(scouts)
            scout_speed = 32

            bombs = []
            explosion_state = 0

            conjurer_speed = 32
            conjurers = []
            conjs_imgs = []

            top_points = rank_points(top_points, points, nametag)

            lives = 3
            points = 0
            game_time = 0
            bombs_amount = 100

            player.x = tile_size
            player.y = tile_size + top_bar_height

            stage = 1
            screen = "title"
            

    #Ranks screen
    elif screen == "ranks":

        #Draw ranks bg
        window.fill((0, 0, 0))
        draw_bg(settings_screen_tile, tile_size * 3, window)

        #Add rank text
        rank_text = text_block("TOP 5 RANKS", 50, (window_width//2, window_height//2 - 200))

        #Add names and points
        nametag_1_text = text_block(top_points[0][1], 30, (window_width//2, window_height//2 - 100))
        nametag_2_text = text_block(top_points[1][1], 30, (window_width//7, window_height//2 + 50))
        nametag_3_text = text_block(top_points[2][1], 30, (window_width//2.5, window_height//2 + 50))
        nametag_4_text = text_block(top_points[3][1], 30, (window_width*1.5/2.5, window_height//2 + 50))
        nametag_5_text = text_block(top_points[4][1], 30, (window_width*6/7, window_height//2 + 50))

        point_1_text = text_block(str(top_points[0][0]), 30, (window_width//2, window_height//2 - 50))
        point_2_text = text_block(str(top_points[1][0]), 30, (window_width//7, window_height//2 + 100))
        point_3_text = text_block(str(top_points[2][0]), 30, (window_width//2.5, window_height//2 + 100))
        point_4_text = text_block(str(top_points[3][0]), 30, (window_width*1.5/2.5, window_height//2 + 100))
        point_5_text = text_block(str(top_points[4][0]), 30, (window_width*6/7, window_height//2 + 100))

        #Draw all text
        window.blit(rank_text[0], rank_text[1])

        window.blit(nametag_1_text[0], nametag_1_text[1])
        window.blit(nametag_2_text[0], nametag_2_text[1])
        window.blit(nametag_3_text[0], nametag_3_text[1])
        window.blit(nametag_4_text[0], nametag_4_text[1])
        window.blit(nametag_5_text[0], nametag_5_text[1])

        window.blit(point_1_text[0], point_1_text[1])
        window.blit(point_2_text[0], point_2_text[1])
        window.blit(point_3_text[0], point_3_text[1])
        window.blit(point_4_text[0], point_4_text[1])
        window.blit(point_5_text[0], point_5_text[1])
        
        #Add back button
        back_button = button("Back", 30, (window_width//2, window_height - 50))
        window.blit(back_button[0], back_button[1])

        pygame.display.update()

        #Back to title screen
        if event.type == pygame.MOUSEBUTTONDOWN:
            if back_button[1].collidepoint(cursor_cords):
                click_sound2.play()
                screen = "title"

        pygame.display.update()

    #About screen
    elif screen == "about":
        
        #Draw about bg
        window.fill((0, 0, 0))
        draw_bg(settings_screen_tile, tile_size * 3, window)

        #Add about text
        about_text = text_block("ABOUT", 50, (window_width//2, window_height//2 - 200))
        back_button = button("Back", 30, (window_width//2 - 250, window_height - 50))
        
        window.blit(about_text[0], about_text[1])
        window.blit(back_button[0], back_button[1])

        #Add author img
        coder_img_block = img_block(coder_img, (100, 100), (100, 100))
        if coder_img_block[1].collidepoint(cursor_cords):
            coder_img = img_load("real coder.jpg", "about", (500, 500))
        else:
            coder_img = img_load("coder.jpg", "about", (500, 500))

        window.blit(coder_img_block[0], coder_img_block[1])

        #Add info
        name_text = text_block("Author:David Obando Blanco", 20, (window_width//2, 140))
        id_text = text_block("Student ID: 2024157494", 20, (window_width//2, 170))
        college_text = text_block("College: Instituto Tecnologico de Costa Rica", 20, (window_width//2, 200))
        class_text = text_block("Class: Introdccion a la programacion", 20, (window_width//2, 230))
        major_text = text_block("Major: Ingenieria en Computadores", 20, (window_width//2, 260))
        year_text = text_block("Year: 2024", 20, (window_width//2, 290))
        teacher_text = text_block("Teacher: Leonardo Araya Martinez", 20, (window_width//2, 320))
        country_text = text_block("Country: Costa Rica", 20, (window_width//2, 350))
        version_text = text_block("Version: 1.0", 20, (window_width//2, 380))

        #Draw info
        window.blit(name_text[0], name_text[1])
        window.blit(id_text[0], id_text[1])
        window.blit(college_text[0], college_text[1])
        window.blit(class_text[0], class_text[1])
        window.blit(major_text[0], major_text[1])
        window.blit(year_text[0], year_text[1])
        window.blit(teacher_text[0], teacher_text[1])
        window.blit(country_text[0], country_text[1])
        window.blit(version_text[0], version_text[1])

        #Back to title screen
        if event.type == pygame.MOUSEBUTTONDOWN:
            if back_button[1].collidepoint(cursor_cords):
                click_sound2.play()
                screen = "title"

        pygame.display.update()

    #General event handler
    if event.type == pygame.QUIT:
        run = False

    clock.tick(60)
    pygame.display.flip()

pygame.quit()
