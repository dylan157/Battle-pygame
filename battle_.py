#!/usr/bin/env python
#This game was made as a throw together project. Excuse the vile coding.
from random import randint
from sys import platform
import players
import os, pygame
import time
global health_icon
global bandit_icon
global fight_timer

size = width, height = 640, 640
pygame.init()
screen = pygame.display.set_mode((size))
ISintro = False


if platform == "linux" or platform == "linux2":
    clear = lambda: os.system('clear')
elif platform == "darwin":
    clear = lambda: os.system('clear')
elif platform == "win32":
    clear = lambda: os.system('cls')
#------------------------------------------------------------------------------------------------------- Varibles
def intro():
    print "Welcome to Battle-with-map!"
    time.sleep(2)
    print "The current objective is to kill enemies and make it through the levels!"
    time.sleep(2)
    print "Buy your way to the next level through the shop"
    time.sleep(2)
    print "Monsters will spawn in the top half of the screen after you step on spawn (~~)"
    time.sleep(2)
    print "Kill the monsters to earn gold!. To stop this intro appearing, set ISintro to False."
    time.sleep(2)
if ISintro: intro()

player = players.Player(raw_input("Name your character: "))

#boring varibles
player_score = 0
error_message = ""
ran = randint 
Still_alive = True
screen_in_use = 0


#other varibles
win = 300
gold_count = 2
enemy_count = 4
Map_Size_X_Y = 8



#bot varibles
d3bug = False
bot_speed = 0.05
bot_memory = 2
max_step = 2

#Icons
land_icon = '@'
bandit_icon = 'X'
health_icon = '+'
player_icon = "h" # make player icon longer (# => ##) to increase screen block size. eg: '##' = 2x2 board icons.
splayer_icon = "H"
wall_icon = "-"
body_icon = "*"
shop_icon = "$"
spawn_icon = "~"
boss_icon1 = "("
door_icon = "|"
fire = "F"



#------------------------------------------------------------------------------------------------------- Map gen/icon length/Object placer/player start location
object_board = []
memory_board = []
playerboard = []
staticsm = [[],[],[],[],[],[]]
staticso = [[],[],[],[],[],[]]
staticsp = [[],[],[],[],[],[]]



for click in range(Map_Size_X_Y):
    object_board.append([land_icon] * Map_Size_X_Y)
    playerboard.append([land_icon] * Map_Size_X_Y)
    memory_board.append([0] * Map_Size_X_Y)
    for stats in staticsm:
        stats.append([0] * Map_Size_X_Y)
    for stats in staticso:
        stats.append([land_icon] * Map_Size_X_Y)
    for stats in staticsp:
        stats.append([land_icon] * Map_Size_X_Y)

Used_coordinates = [[],[],[],[],[],[],[],[]]# this varible prevents object placement conflict in the Object_placement function by recording xy's already in use(e.g bandit_icon in 4,7 so a gold_icon cant also be placed there )
player_xy = [(len(object_board)-2), 0, 0]
Used_coordinates[0].append(str(player_xy[0]) + str(player_xy[1]))


tick = 0
#for block in range(len(playerboard)):
#    playerboard[len(playerboard)/2][tick] = wall_icon
#    Used_coordinates[0].append(str(len(playerboard)/2) + str(tick))#Wall
#    playerboard[(len(static_o2)-1)][len(playerboard)/2] = spawn_icon
#    object_board[(len(static_o2)-1)][len(playerboard)/2] = spawn_icon
#    Used_coordinates[0].append(str((len(object_board)-1)) + str(0))#spawn

#    if tick == (len(playerboard)/2):
#        Used_coordinates[0].append(str(len(playerboard)/2) + str(tick))
#        4 = str(len(playerboard)/2)
#        playerboard[(len(playerboard)/2)+1][tick] = shop_icon
#        object_board[(len(playerboard)/2)+1][tick] = shop_icon
#        Used_coordinates[0].append(str((len(playerboard)/2)+1) + str(tick))
#    tick += 1#wall placer

def level_maker(player_bd, object_bd, used_co, door):
    tick = 0
    for block in range(len(player_bd)):
        player_bd[len(player_bd)/2][tick] = wall_icon
        used_co.append(str(len(player_bd)/2) + str(tick))#Wall
        if tick == 0:
            player_bd[(len(object_bd)-1)][len(playerboard)/2] = spawn_icon
            object_bd[(len(object_bd)-1)][len(playerboard)/2] = spawn_icon
            used_co.append(str((len(object_bd)-1)) + str(len(playerboard)/2))#spawn

        if tick == (len(player_bd)/2):
            used_co.append(str(len(player_bd)/2) + str(tick))
            player_bd[(len(player_bd)/2)+1][tick] = shop_icon
            object_bd[(len(player_bd)/2)+1][tick] = shop_icon
            used_co.append(str((len(player_bd)/2)+1) + str(tick))
        if tick == (len(player_bd)-1) and door:
            player_bd[len(player_bd)-1][0] = door_icon
            object_bd[len(player_bd)-1][0] = door_icon

            used_co.append(str(len(player_bd)-1) + str(int((len(playerboard)-1))))
        tick += 1#wall placer

level_maker(staticsp[0], staticso[0], Used_coordinates[0], False)
level_maker(staticsp[1], staticso[1], Used_coordinates[1], True)
level_maker(staticsp[2], staticso[2], Used_coordinates[2], True)
level_maker(staticsp[3], staticso[3], Used_coordinates[3], True)
level_maker(staticsp[4], staticso[4], Used_coordinates[4], True)
level_maker(staticsp[5], staticso[5], Used_coordinates[5], True)
playerboard = staticsp[screen_in_use]
object_board = staticso[screen_in_use]
memory_board = staticsm[screen_in_use]


shop = [['-', 's1', 's2', 's3', 's4', 's5', '-', '-'],
        ['-', 's$', 'sf', 'sf', 'sf', 'sf', 'sf', '-'],
        ['-', 'sf', 'sf', 'sf', 'sf', 'sf', 'sf', '-'],
        ['-', 'sf', 'sf', 'sf', 'sf', 'sf', 'sf', '-'],
        ['-', 'sf', 'sf', 'sf', 'sf', 'sf', 'sf', '-'],
        ['-', 'sf', 'sf', 'sf', 'sf', 'sf', 'sf', '-'],
        ['-', 'sf', 'sf', 'sf', 'sf', 'sf', 'sf', '-'],
        ['-', '-', '-', 'sd', 'sd', '-', '-', '-']]
shopm = [['-', 's1', 's2', 's3', 's4', 's5', '-', '-'],
        ['-', 's$', 'sf', 'sf', 'sf', 'sf', 'sf', '-'],
        ['-', 'sf', 'sf', 'sf', 'sf', 'sf', 'sf', '-'],
        ['-', 'sf', 'sf', 'sf', 'sf', 'sf', 'sf', '-'],
        ['-', 'sf', 'sf', 'sf', 'sf', 'sf', 'sf', '-'],
        ['-', 'sf', 'sf', 'sf', 'sf', 'sf', 'sf', '-'],
        ['-', 'sf', 'sf', 'sf', 'sf', 'sf', 'sf', '-'],
        ['-', '-', '-', 'sd', 'sd', '-', '-', '-']]

def Object_Placement(object_count, object_to_be_placed, Used_coordinates, specific_x1, specific_y1, specific_x2, specific_y2): # random input
    spot = []
    calculated_board_x, calculated_board_y = specific_x1, specific_y1
    calculated_board_x0, calculated_board_y0 = specific_x2, specific_y2
    if specific_x1 == "n":
        calculated_board_x = (len(object_board)-1)
    if specific_y1 == "n":
        calculated_board_y = (len(object_board)-1)
    if specific_x2 == "n":
        calculated_board_x0 = (0)
    if specific_y2 == "n":
        calculated_board_y0 = (0)
    for x in range(object_count): # How many random numbers?
        x, z = 0, 0        
        def baker():
            global x
            global z
            x, z = randint(calculated_board_y0, calculated_board_y), randint(calculated_board_x0, calculated_board_x)            
            if (str(x) + str(z)) in Used_coordinates: # or (str(x) + str(z)) in Used_coordinates:
                #print "XZ FOUND IN SPOT", (str(x) + str(z))
                baker()
            elif (str(x) + str(z)) in spot:
                #print "XZ FOUND IN USED COORDINATES", (str(x) + str(z))
                baker()
            else:
                object_board[x][z] = object_to_be_placed
                if object_to_be_placed == bandit_icon:
                    playerboard[x][z] = object_to_be_placed
                Used_coordinates.append(str(x) + str(z))
                spot.append(str(x) + str(z))
                           
        baker()

    if len(spot) > object_count:
        print "OVERFLOW!"
    return spot
    Used_coordinates.append(spot)
Object_Placement(gold_count, health_icon, Used_coordinates[0], "n", "n", "n", "n")
#Object_Placement(weapon_count, weapon_icon, "n", "n") ########## add me in!!!
#Object_Placement(gold_count, health_icon, Used_coordinates[0], "n", "n", "n", "n")

#staticsp = playerboard[:]
#staticso = object_board[:]
#staticsm = memory_board[:]

#------------------------------------------------------------------------------------------------------- print board
def print_board(board):
    x = 0
    y = 0
    size = 80
    icons = {'@' : 'ground.jpg',
    'X':'bandit.jpg',
    '+':'health.jpg',
    "h":'player.jpg',
    "H":'splayer.jpg',
    "-":'wall.jpg',
    "*":'dead.jpg',
    "$":'shop.jpg',
    "~":'spawn.jpg',
    "(":'boss.jpg',
    "|":'door.jpg',
    "F":"fire.jpg",
    "f":"fire1.jpg",
    "g":"fire2.jpg",
    "G":"fire3.jpg",
    "s1":"shopwall1.jpg",
    "s2":"shopwall2.jpg",
    "s3":"shopwall3.jpg",
    "s4":"shopwall4.jpg",
    "s5":"shopwall5.jpg",
    "s6":"shopwall6.jpg",
    "sf":"shopfloor.jpg",
    "sd":"shopdoor.jpg",
    "s$":"shop$.jpg"}
    for row in object_board:
        for j in range(1):
            print " ".join(row)
    for row in board:
        cout = 0
        x = 0
        for square in row:
            cout +=1 
            #pygame.draw.rect(screen, icons[square], [x, y, int(size), int(size)]) 
            try:
                img = pygame.image.load("assets/"+icons[square])
            except: img = pygame.image.load("assets/ground.jpg")
            screen.blit(img,(x,y))
            if x < width: x += size
            else: x = 0
        y += size
    pygame.display.update()


print_board(playerboard)
#print_board(memory_board)

#------------------------------------------------------------------------------------------------------- Board Transport
def board_transport(move_choice, em, who):
    #Board transport determins if the move it has been ordered to process is legal or not (valid input and on-map) 
    #Once the move has been validated, the players current location is re-written and returned to be further processed by the game loop.
    global error_message
    global player_score
    global static_player
    global clear


    if move_choice == "d3bug":
        player.level, player.gold, player.attack, player.health = 15766, 15766, 15766, 15766
    em = move_choice
    if move_choice == "XP!":
        player.xp += 10
        player.gold
    if move_choice == "RESET":
        who[0] = 0
        who[1] = 0
    if move_choice == "STP":
        print static_player[0]
        print static_player[1]
        print static_player[2]
        time.sleep(3)

    if len(move_choice) == 1 and move_choice[0] in ('w', 'a', 's', 'd'):
        if move_choice[0] == "w":
            if who[0] - int(1) >= 0: #UP
                if playerboard[(who[0] - int(1))][who[1]] not in (wall_icon, 's1','s2','s3','s4','s5','s6'):
                    who[0] -= int(1) 
                else:
                    em = "You can't move there!"
            else:
                em = "You can't move there!"

        elif move_choice[0] == "s":
            if (who[0] + int(1)) <= (len(object_board)-1): #DOWN
                if playerboard[(who[0] + int(1))][who[1]] not in (wall_icon, 's1','s2','s3','s4','s5','s6'):
                    who[0] += int(1)
                else:
                    em = "You can't move there!"
            else:
                em = "You can't move there!"

        elif move_choice[0] == "d":
            if who[1] + int(1) <= (len(object_board)-1): #RIGHT
                if playerboard[who[0]][(who[1] + int(1))] not in (wall_icon, 's1','s2','s3','s4','s5','s6'):
                    who[1] += int(1)
                else:
                    em = "You can't move there!"
            else:
                em = "You can't move there!"

        elif move_choice[0] == "a":
            if who[1] - int(1) >= 0: #LEFT
                if playerboard[who[0]][(who[1] - int(1))] not in (wall_icon, 's1','s2','s3','s4','s5','s6'):
                    who[1] -= int(1)
                else:
                    em = "You can't move there!"
            else:
                em = "You can't move there!"
        else:
            em = "What?"
    else:
        em = "Controls: w,a,s,d + enter"
    error_message = em
    return who

#------------------------------------------------------------------------------------------------------- Battle loop
def fight(enemy):
    player_weapon = ""
    enemy_weapon  = ""
    global fight_timer
    global battle_timer
    clear()
    print "A", enemy.name ,"appears!"
    time.sleep(1)
    weapon_check = ""
    if enemy.weapon > 0:
        weapon_check = "and has a weapon! >" + enemy.weaponName
    if (enemy.health + enemy.attack + enemy.defence) > (player.health + player.attack + player.defence):
        print "He looks tough" + weapon_check + "!"
    else:
        print "He looks weak" + weapon_check + "!"
    enemy.calls()
    time.sleep(2)
    fight_timer = True

    while fight_timer:
        battle_timer += 1
        class attack_style(object):
            def __init__(self, ch_attack_style, who):
                self.ch_attack_style = ch_attack_style
                if self.ch_attack_style == "o":
                    self.style = "Attack"
                    self.defence = 1 + who.side
                    self.attack = 1 + who.weapon
                    self.speed = 1
                elif self.ch_attack_style in ("d", "b"):
                    self.style = "Block!"
                    self.defence = 2 + who.side
                    self.attack = 0.5 + who.weapon
                    self.speed = 0
                elif self.ch_attack_style == "p":
                    self.style = "Throws a power attack!"
                    self.defence = 0.5 + who.side
                    self.attack = 3 + who.weapon
                    self.speed = 2
                elif self.ch_attack_style == "r":
                    self.style = "Retreat!"
                    self.defence = 2 + who.side
                    self.attack = 0.5
                    self.speed = 1
                else:
                    self.style = "panic!"
                    self.defence = 0.5
                    self.attack = 0.5
                    self.speed = 0
        class temp_stats(object):
            def __init__(self, who, who_move):
                self.style = who_move.style
                self.attack = who.attack * (who_move.attack)
                self.defence = who.defence * (who_move.defence)



        def battle(fighter, opponent, fighter_stat, opponent_stat):
            def attack(attack, defence):
                damage = int(attack / ran(2, int(defence*0.1)))
                if damage < (defence*0.1):
                    damage = 0

                return damage
            global fight_timer
            
            time.sleep(1)
            hit = attack(fighter_stat.attack, (opponent_stat.defence))
            if hit > 0:
                opponent.health -= hit
                print ""
                print fighter.name, "hit", opponent.name, "using", fighter.weaponName
                time.sleep(1)
                print ""
                print opponent.name, "Takes",  str(hit), "Damage!"
                time.sleep(1)
                print ""
                if opponent.health <= 0:
                    opponent.health = 0
                print opponent.name, "has", str(opponent.health) + " HP Remaining"
                time.sleep(1)
            else:
                print ""
                print opponent.name, "Blocked", fighter.name, "using", opponent.sideName
                time.sleep(1)
            if opponent.health <= 0:
                opponent.health = 0
                opponent.life = False
                print ""
                print opponent.name, "is dead!"
                fight_timer = False

        print ""
        print "Enter battle tactic:"
        print "'d'-Defencive"
        print "'o'-Basic attack"
        print "'p'-Power attack"
        print "'r'-Run"
        print "'s'-Battle stats"
        chosen_move = ""
        while chosen_move not in ("d", "o", "p", "r"):
            #chosen_move = raw_input("Enter now: ")
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        chosen_move = "d"
                    if event.key == pygame.K_o:
                        chosen_move = "o"
                    if event.key == pygame.K_p:
                        chosen_move = "p"
                    if event.key == pygame.K_r:
                        chosen_move = "r"
                    if event.key == pygame.K_s:
                        chosen_move = "s"
            if chosen_move == "s":
                clear()
                print "Enemy health:", enemy.health
                print "Enemy weapon:", enemy.weaponName
                print "Enemy stats:", "A/", enemy.attack, " D/", enemy.defence, " L/", enemy.level
                print "Your stats:", "A/", player.attack, " D/", player.defence, " L/", player.level
                print "Your health:", player.health
                print "Your weapon:", player.weaponName
                print "Your side:", player.sideName
                chosen_move = ""

        player_move = attack_style(chosen_move, player)
        enemy_rand = randint(0, 2)
        if enemy_rand == 0:
            enemy_move = attack_style("o", enemy)
        elif enemy_rand == 1:
            enemy_move = attack_style("d", enemy)
        else:
            enemy_move = attack_style("p", enemy)

        temp_player = temp_stats(player, player_move)
        temp_enemy = temp_stats(enemy, enemy_move)

        def who(enemy_move, player_move):
            player_speed = player.attack * player_move.speed
            enemy_speed = enemy.attack * enemy_move.speed
            if player_move.style == "Block!":
                player_speed = 0
            if player_move.style == "Retreat!" :
                player_speed = 0
                return "run"
            elif player_speed > enemy_speed:
                return 1
            elif player_speed < enemy_speed:
                return 0
            else:
                return randint(0,1)

        clear()
        print player.name, "prepares to", player_move.style,
        time.sleep(1)
        print ""
        print enemy.name, "prepares to", enemy_move.style
        time.sleep(1)

        Who = who(enemy_move, player_move)
        if Who == 1:
            battle(player, enemy, temp_player, temp_enemy)
            if fight_timer:

                enemy.calls()
                time.sleep(2)
                battle(enemy, player, temp_enemy, temp_player)
        elif Who == 0:
            enemy.calls()
            time.sleep(2)
            battle(enemy, player, temp_enemy, temp_player)
            if fight_timer:
                battle(player, enemy, temp_player, temp_enemy)
        elif Who == "run" or player_move.style == "Retreat!":
            enemy.calls()
            time.sleep(2)
            battle(enemy, player, temp_enemy, temp_player)
            fight_timer = False
            if player.life:
                return 1
            else:
                return 0

        time.sleep(1)


def boss_animation():
    global playerboard
    work_xy = [0,0]
    tick = 0
    trail_text = "F"
    boss_name = "BOSSANI WILL KILL YOU"
    for block in range(len(playerboard)):
        playerboard[len(playerboard)/2][tick] = wall_icon

    
    while True:
        playerboard[work_xy[0]][work_xy[1]] = trail_text[tick%len(trail_text)-1]
        object_board[work_xy[0]][work_xy[1]] = trail_text[tick%len(trail_text)-1]
        tick += 1
        if work_xy[1] + int(1) <= (len(object_board)-1): #Boss animation 
            work_xy[1] += int(1)
        else:
            if (playerboard[work_xy[0] + 1][work_xy[1]]) not in (wall_icon):
                work_xy[0] += int(1)
                work_xy[1] = 0
            else: break
        time.sleep(bot_speed/4)
        clear()
        print_board(playerboard)
    work_xy = [0,0]
    time.sleep(bot_speed)
    for plays in range(8):
        tick = 0
        while True:
            playerboard[work_xy[0]][work_xy[1]] = boss_name[tick%len(trail_text)-1]
            tick += 1
            if work_xy[1] + int(1) <= (len(object_board)-1): 
                work_xy[1] += int(1)
            else:
                if (playerboard[work_xy[0] + 1][work_xy[1]]) not in (wall_icon):
                    work_xy[0] += int(1)
                    work_xy[1] = 0
                else: break
        work_xy = [0,0]
        clear()
        print_board(playerboard)
        time.sleep(bot_speed/4)

        while True:
            playerboard[work_xy[0]][work_xy[1]] = 'F'
            if work_xy[1] + int(1) <= (len(object_board)-1): 
                work_xy[1] += int(1)
            else:
                if (playerboard[work_xy[0] + 1][work_xy[1]]) not in (wall_icon):
                    work_xy[0] += int(1)
                    work_xy[1] = 0
                else: break
        work_xy = [0,0]
        clear()
        print_board(playerboard)
        work_xy = [0,0]
        clear()
        print_board(playerboard)
    playerboard[(len(playerboard)/3)-1][(len(playerboard)/2)-1] = boss_icon1
    object_board[(len(object_board)/3)-1][(len(object_board)/2)-1] = boss_icon1
    print_board(playerboard)

class Shop(): # move me to top
    def __init__(self):
        self.items = ["Basic knife       30  Gold", "Basic shield      60  Gold", "Access to zone 0  10  Gold", "Access to level 2  100  Gold"] 
        self.items2 = ["Steel sword       100  Gold", "Steel shield      145  Gold", "Access to zone 0  10  Gold", "Access to level 3  250  Gold"]
        self.items3 = [ "Ritchie's sword   400 Gold", "Ritchie's shield  650 Gold", "Access to zone 0  10  Gold", "Access to next level 400  Gold"]
    def shop(self):
        clear()
        if playerboard[4][0] != land_icon:
            self.items[2] = "Access to zone 0  50  Gold"
        if player.gold >= 0:
            print "Welcome to Ritchie's shop!"
            print ""
            counter = 0
            for stock in self.items:
                print str(counter) + ".", self.items[counter]
                counter += 1
            print str(counter) + ".", "Health            10  Gold"
            print ""
            print "Enter 'e' to exit"
            print "You have", player.gold, "gold"
            print ""
            #buy = raw_input("Enter item number to buy item  -")
            buy = ""
            while buy not in ("0", "1", "2", "3", "4", "e"):
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_0:
                            buy = "0"
                        if event.key == pygame.K_1:
                            buy = "1"
                        if event.key == pygame.K_2:
                            buy = "2"
                        if event.key == pygame.K_3:
                            buy = "3"
                        if event.key == pygame.K_4:
                            buy = "4"
                        if event.key == pygame.K_e:
                            buy = "e"
            if buy == "0" and self.items[0] != "SOLD" and player.gold >= 30:
                player.gold -= 30
                player.weapon = 1
                player.weaponName = "Knife"
                print "You have purchased a Basic knife!"
                self.items[0] = "SOLD"
                time.sleep(1)
                self.shop()

            elif buy == "1" and self.items[1] != "SOLD" and player.gold >= 60:
                player.gold -= 60
                player.side = 1
                player.sideName = "Shield"
                print "You have purchased a Basic shield!"
                self.items[1] = "SOLD"
                time.sleep(1)
                self.shop()

            elif buy == "2" and player.gold >= 10 and staticsp[screen_in_use][int(4)][0] != land_icon:
                    player.gold -= 10
                    print "You have purchased access to zone 0!"
                    staticsp[screen_in_use][int(4)][0] = land_icon
                    self.items[2] = "ZONE 0 IS ACCESSABLE"
                    time.sleep(1)
                    self.shop()
            elif buy == "3" and self.items2[3] != "SOLD" and player.gold >= 100:
                    player.gold -= 100
                    print "You have purchased access to level 2!"
                    self.items[3] = "SOLD"
                    time.sleep(1)
                    playerboard[len(playerboard)-1][(len(playerboard)-1)] = door_icon
                    object_board[len(playerboard)-1][(len(playerboard)-1)] = door_icon
                    Used_coordinates[0].append(str(len(playerboard)-1) + str((len(playerboard)-1)))
                    self.shop1()
            elif buy == "4":
                if player.health_check():
                    player.health += player.level *25
                    player.gold -= 10
                    self.shop()
                else:
                    clear()
                    print "You already have full heath!"
                    time.sleep(1)
                    self.shop()
            elif buy in ("e", "w", "a", "s", "d"):
                print "bye!"
                time.sleep(0.5)
            else:
                clear()
                print "You can't buy that!"
                time.sleep(0.3)
                self.shop()

        else:
            print "sorry! Looks like you're too poor to shop here :P"
            time.sleep(1)
            print "SLAM!"
            time.sleep(1)

    def shop1(self):
        clear()
        if playerboard[int(4)][0] != land_icon:
            self.items2[2] = "Access to zone 0  50  Gold"
        if player.gold >= 0:
            print "Welcome to Ritchie's shop!"
            print ""
            counter = 0
            for stock in self.items2:
                print str(counter) + ".", self.items2[counter]
                counter += 1
            print str(counter) + ".", "Health            10  Gold"
            print ""
            print "Enter 'e' to exit"
            print "You have", player.gold, "gold"
            print ""
            #buy = raw_input("Enter item number to buy item  -")
            buy = ""
            while buy not in ("0", "1", "2", "3", "4", "e"):
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_0:
                            buy = "0"
                        if event.key == pygame.K_1:
                            buy = "1"
                        if event.key == pygame.K_2:
                            buy = "2"
                        if event.key == pygame.K_3:
                            buy = "3"
                        if event.key == pygame.K_4:
                            buy = "4"
                        if event.key == pygame.K_e:
                            buy = "e"
            if buy == "0" and self.items2[2] != "SOLD" and player.gold >= 100:
                player.gold -= 100
                player.weapon = 2
                player.weaponName = "Steel sword"
                print "You have purchased a Steel sword!"
                self.items2[0] = "SOLD"
                time.sleep(1)
                self.shop1()

            elif buy == "1" and self.items2[3] != "SOLD" and player.gold >= 145:
                    player.gold -= 145
                    player.side = 2
                    player.sideName = "Steel shield"
                    print "You have purchased a Steel shield!"
                    self.items2[1] = "SOLD"
                    time.sleep(1)
                    self.shop1()

            elif buy == "2" and player.gold >= 10 and staticsp[screen_in_use][int(4)][0] != land_icon:
                    player.gold -= 10
                    print "You have purchased access to zone 0!"
                    staticsp[screen_in_use][int(4)][0] = land_icon
                    self.items2[2] = "ZONE 0 IS ACCESSABLE"
                    time.sleep(1)
                    self.shop1()
            elif buy == "3" and self.items2[3] != "SOLD" and player.gold >= 250:
                    player.gold -= 250
                    print "You have purchased access to level 3!"
                    self.items2[3] = "SOLD"
                    time.sleep(1)
                    playerboard[len(playerboard)-1][(len(playerboard)-1)] = door_icon
                    object_board[len(playerboard)-1][(len(playerboard)-1)] = door_icon
                    Used_coordinates[0].append(str(len(playerboard)-1) + str((len(playerboard)-1)))
                    self.shop1()
            elif buy == "4":
                if player.health_check():
                    player.health += player.level *25
                    player.gold -= 10
                    self.shop1()
                else:
                    clear()
                    print "You already have full heath!"
                    time.sleep(1)
                    self.shop1()
            elif buy in ("e", "w", "a", "s", "d"):
                print "bye!"
                time.sleep(0.5)
            else:
                clear()
                print "You can't buy that!"
                time.sleep(0.3)
                self.shop1()

        else:
            print "sorry! Looks like you're too poor to shop here :P"
            time.sleep(1)
            print "SLAM!"
            time.sleep(1)
    
    def shop2(self):
        clear()
        if playerboard[int(4)][0] != land_icon:
            self.items3[2] = "Access to zone 0  50  Gold"
        if player.gold >= 0:
            print "Welcome to Ritchie's shop!"
            print ""
            counter = 0
            for stock in self.items3:
                print str(counter) + ".", self.items3[counter]
                counter += 1
            print str(counter) + ".", "Health            10  Gold"
            print ""
            print "Enter 'e' to exit"
            print "You have", player.gold, "gold"
            print ""
            buy = ""
            #buy = raw_input("Enter item number to buy item  -")
            while buy not in ("0", "1", "2", "3", "4", "e"):
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_0:
                            buy = "0"
                        if event.key == pygame.K_1:
                            buy = "1"
                        if event.key == pygame.K_2:
                            buy = "2"
                        if event.key == pygame.K_3:
                            buy = "3"
                        if event.key == pygame.K_4:
                            buy = "4"
                        if event.key == pygame.K_e:
                            buy = "e"
            if buy == "0" and self.items3[0] != "SOLD" and player.gold >= 400:
                    player.gold -= 400
                    player.weapon = 3
                    player.weaponName = "Ritchie's sword"
                    print "You have purchased Ritchie's sword!"
                    self.items3[0] = "SOLD"
                    time.sleep(1)
                    self.shop2()

            elif buy == "1" and self.items3[1] != "SOLD" and player.gold >= 650:
                    player.gold -= 650
                    player.side = 3
                    player.sideName = "Ritchie's shield!"
                    print "You have purchased a Ritchie's shield!"
                    self.items3[1] = "SOLD"
                    time.sleep(1)
                    self.shop2()

            elif buy == "2" and player.gold >= 10 and staticsp[screen_in_use][int(4)][0] != land_icon:
                    player.gold -= 10
                    print "You have purchased access to zone 0!"
                    staticsp[screen_in_use][int(4)][0] = land_icon
                    self.items3[2] = "ZONE 0 IS ACCESSABLE"
                    time.sleep(1)
                    self.shop2()
            elif buy == "3" and self.items3[3] != "SOLD" and player.gold >= 400:
                    player.gold -= 400
                    print "You have purchased access to the next level!"
                    #self.items3[3] = "SOLD"d
                    time.sleep(1)
                    playerboard[len(playerboard)-1][(len(playerboard)-1)] = door_icon
                    object_board[len(playerboard)-1][(len(playerboard)-1)] = door_icon
                    Used_coordinates[0].append(str(len(playerboard)-1) + str((len(playerboard)-1)))
                    self.shop2()
            elif buy == "4":
                if player.health_check():
                    player.health += player.level *25
                    player.gold -= 10
                    self.shop2()
                else:
                    clear()
                    print "You already have full heath!"
                    time.sleep(1)
                    self.shop2()
            elif buy in ("e", "w", "a", "s", "d"):
                print "bye!"
                time.sleep(0.5)
            else:
                clear()
                print "You can't buy that!"
                time.sleep(0.3)
                self.shop2()

        else:
            print "sorry! Looks like you're too poor to shop here :P"
            time.sleep(1)
            print "SLAM!"
            time.sleep(1)


shop_use = Shop()
def map_changer( where_is, move):
    global ststicp
    global ststico
    global ststicm
    global playerboard
    global object_board
    global memory_board
    global screen_in_use
    global player_icon

    def ori():
        global ststico
        global ststicm
        global playerboard
        global object_board
        global memory_board
        global screen_in_use 
        global ststicp
        staticsp[screen_in_use] = playerboard
        staticso[screen_in_use] = object_board
        staticsm[screen_in_use] = memory_board

    def out():
        global ststicp
        global ststico
        global ststicm
        global playerboard
        global object_board
        global memory_board
        global screen_in_use
        playerboard = staticsp[screen_in_use]
        object_board = staticso[screen_in_use]
        memory_board = staticsm[screen_in_use]

    if move == "r":
        ori()
        screen_in_use += 1
        where_is = [len(playerboard)-1, 0, 0]
        out()

    if move == "l":
        ori()
        screen_in_use -= 1
        where_is = [len(playerboard)-1, len(playerboard)-1, 0]
        out()

    if move == "]":
        ori()
        where_is = [7, 4, 0]
        playerboard = shop[:]
        object_board = shopm[:]
        player_icon="H"

    if move == "[":
        where_is = [5, 4, 0]
        player_icon = "h"
        out()
    return where_is


#------------------------------------------------------------------------------------------------------- game loop
while player.life == True:
    icon_length = len(player_icon)
    bandit_icon = bandit_icon
    health_icon = health_icon
    #print_board(object_board)
    #time.sleep(1)
    while True:
        
        clear()
        #os.system('clear') #FOR LINUX  




        print error_message
        error_message = ""
        oldposision = player_xy
        playerboard[player_xy[0]][player_xy[1]] = player_icon # The players location on the board is only temporary. 
        print_board(playerboard) # After print_board, the players location is replaced with the xy value from object board
        print ""

        playerboard[oldposision[0]][oldposision[1]] = object_board[oldposision[0]][oldposision[1]] # Make players current xy  == object (bandit icon etc)
        memory_board[oldposision[0]][oldposision[1]] += 1 #Block usage counter (You have stepped on this square x times)


        # Reactions to board icons
        if object_board[oldposision[0]][oldposision[1]] == bandit_icon:
            enemy = players.Enemy(screen_in_use, static_player)
            battle_timer = 0
            GAME = fight(enemy)
            if player.life == True and GAME != 0 and not enemy.life:
                player.kills += 1
                player.xp += int((enemy.attack+enemy.defence)*randint(1, 4)/10*(battle_timer*0.5))
                player.gold += int((enemy.attack+enemy.defence)*.6)/battle_timer
                playerboard[oldposision[0]][oldposision[1]], object_board[oldposision[0]][oldposision[1]] = body_icon, body_icon
                clear()
                print_board(playerboard)
                Still_alive = True
            elif GAME == 1:
                clear()
                print_board(playerboard)
                Still_alive = True
            else:
                Still_alive = False
                break


        if playerboard[oldposision[0]][oldposision[1]] in (boss_icon1):
            enemy = players.Boss(static_player)
            battle_timer = 0
            GAME = fight(enemy)
            if player.life == True and GAME != 0 and not enemy.life:
                player.kills += 1
                player.xp += int((enemy.attack+enemy.defence)*.3)
                player.gold += int((enemy.attack+enemy.defence)*.6)/battle_timer
                playerboard[oldposision[0]][oldposision[1]], object_board[oldposision[0]][oldposision[1]] = body_icon, body_icon
                clear()
                print_board(playerboard)
                Still_alive = True
            elif GAME == 1:
                clear()
                print_board(playerboard)
                Still_alive = True
            else:
                Still_alive = False
                break
        if object_board[oldposision[0]][oldposision[1]] == health_icon:
            if player.health_check():
                if memory_board[oldposision[0]][oldposision[1]] <= 3:
                    player.health += player.level *25
            else:
                memory_board[oldposision[0]][oldposision[1]] -= 1
            if memory_board[oldposision[0]][oldposision[1]] == 3:
                playerboard[oldposision[0]][oldposision[1]], object_board[oldposision[0]][oldposision[1]] = land_icon, land_icon # Make chest_icon into bandit_icon

        if object_board[oldposision[0]][oldposision[1]] == shop_icon:
            player_xy = map_changer(player_xy, "]")
        if object_board[oldposision[0]][oldposision[1]] == "sd":
            player_xy = map_changer(player_xy, "[")

        if object_board[oldposision[0]][oldposision[1]] == "s$":
            if screen_in_use == 0:
                shop_use.shop()
            elif screen_in_use == 1:
                shop_use.shop1()
            elif screen_in_use == 2:
                shop_use.shop2()
            else: shop_use.shop2()
            clear()
            print_board(playerboard)


        if object_board[oldposision[0]][oldposision[1]] == spawn_icon:
            ban_count = 0
            body_count = 0
            for test in playerboard:
                for test2 in test:
                    if test2 == bandit_icon:
                        ban_count += 1
                    if test2 == body_icon:
                        body_count += 1


            if ban_count == 0:
                player.gold += 100
                static_player = [player.attack, player.max_health, player.defence]
                Object_Placement(enemy_count, bandit_icon, Used_coordinates[screen_in_use], "n", ((len(playerboard)/2)-1), "n", "n")
            if body_count >= 8:
                boss_animation()

        if object_board[oldposision[0]][oldposision[1]] == door_icon:
            if (player_xy[1] > int(len(playerboard)/2)):
                player_xy = map_changer(oldposision, "r")
            elif (player_xy[1] < int(len(playerboard)/2)):
                player_xy = map_changer(oldposision, "l")



        print "HP:", player.health, "  Level: ", player.level, "  Xp: ", player.xp, "  Gold: ", player.gold
        #print_board(object_board)


        player.stat_check()
        if Still_alive == True:
            choice = False
            while choice == False:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                            W = 'a'
                            choice = True
                        if event.key == pygame.K_s:
                            W = 's'
                            choice = True
                        if event.key == pygame.K_d:
                            W = 'd'
                            choice = True
                        if event.key == pygame.K_w:
                            W = 'w'
                            choice = True
                        if event.key == pygame.K_p:
                            W = raw_input('manual -')
                            choice = True
            #W = raw_input('wasd')
            if W == "p":
                boss_animation()
            elif W == "glitch":
                screen_in_use += 1
            elif W == "unglitch":
                screen_in_use -= 1
        else:
            Still_alive = False
            break

        '''else:
            W = d3bug_bot(bot_speed)'''
        board_transport(W, error_message, player_xy)
    break
else:
    print "You have died!"
    time.sleep(22)
    #hello