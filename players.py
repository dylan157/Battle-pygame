from random import randint

class Player(object):
    def __init__(self, name):
        self.kills = 0
        self.level = 1
        self.xp = 0
        self.name = name
        self.health = 100
        self.max_health = 100
        self.attack = 100
        self.defence = 100
        self.weapon = 0
        self.weaponName = "Fists"
        self.side = 0
        self.sideName = "Arms"
        self.life = True
        self.gold = 0
    def health_check(self):
        if self.health >= self.max_health:
            self.health = self.max_health
            return False
        else:
            return True

    def level_check(self):
        if self.xp >= self.level*100:
            self.level += 1
            clear()
            print "Level up!"
            time.sleep(1)
            print "What would you like to add 50 skill points too?"
            print "1. Attack", "    ", "Attack lv currently: ", self.attack
            print "2. Defence", "    ", "Defence lv currently: ", self.defence
            print "3. Health", "    ", "Max Health currently: ", self.max_health
            skill = ""
            while skill not in ("1", "2", "3"):
                #skill = raw_input("enter: 1/2/3  -")
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            skill = "1"
                        if event.key == pygame.K_2:
                            skill = "2"
                        if event.key == pygame.K_3:
                            skill = "3"

                if skill == "1":
                    self.attack += 50
                elif skill == "2":
                    self.defence += 50
                elif skill == "3":
                    self.max_health += 50
                else:
                    print "Please re-enter  -"
            self.health = self.max_health
    def stat_check(self):
        self.level_check()
        self.health_check()

class Enemy(object):#needs work to handle higher levels
    def __init__(self, sc, static_player):
        names = ["Bandit", "Random angry guy", "Scavenger", "Death dunden", "Wild Bone Biter", "Skeleton", "Kill Caller", "KILLTOLN"  ]
        weapons = ["Fists", "Stick", "Brick", "Pole", "Hammer", "knife", "Sharp knife", "Razor Teeth" "Bone Bat", "Katana", "KIll SCREAM", "ION LAZOR", "KILL BAT 2.0"]
        sides = ["Arms", "Leathers", "Arms", "Wooden board", "Thick Leathers", "Kevlar Amour", "Thick Skin", "Leather Robe", "Hard Bones", "Bone Shield", "Hard Bones", "Bone Shield", "Skin Silk Battle Robe", "Kill shield", "METAL AMOUR", "BALLISTIC AMOUR 2.0"]
        self.battle_level = sc * 2
        self.level = randint(self.battle_level, self.battle_level)
        if self.level > 8: self.level = 8
        self.name = names[self.level]
        if self.level == 0:
            self.level += 1 
        self.health = randint(int(static_player[1] * self.level*.4), int(static_player[1] * self.level*.9))
        self.attack = randint(int(static_player[1] * self.level*.4), int(static_player[1] * self.level*.9))
        self.defence = randint(int(static_player[1] * self.level*.4), int(static_player[1] * self.level*.9))
        self.life = True
        self.weapon = randint(0, 1)
        self.side = randint(0, 1)
        if self.weapon == 1:
            self.weaponName = weapons[self.level+1]
        else:
            self.weaponName = weapons[self.level]
        if self.side == 1:
            self.sideName = sides[self.level+1]
        else:
            self.sideName = sides[self.level]
    def calls(self):
        calls = ["Your going to die!", "Say hello to my little friend!", "Take this!", "Prepare to turn to paste!", "blub blub", "Squarch!", "Its peanut butter jelly time!", "Bleed, BLEED!", "Bossani will end you mortal!", "Your time is limited!", "Are we inside a game?", "The grass was greener!", "Say hello to skeaks for me!", "You will never leave alive!", "Argh!!!!", "*Tries to fly*.. Damn, i cant fly", "Why cant we just be friends?", "Say goodbye to your spine", "Always remember to bring a towel!", "I will kill you, then the demons will kill you :D", "Please just die", "Die", "Can you stop breathing?", "Banana blast!", "LUBBA BUB BUB", "DDIIEE!", "all your castles are belong to us!"]
        calls2 = ["ARHGGGGGG!", "SCREEEECH!", "DIIIIIEEEE!", "RAWWWW!!", "EHHHHHHHCHHH!", "KSSSSKSSK!!", "ICCHCHH!!", "KILL ALL HUMANS", "BEEP BOP", "01001011 01001001 01001100 01001100", "DIE DIE DIE", "'WARNING, FRIENDBOT SET TO KILL MODE. TO CHANGE YOUR FRIENDBOTS PLAYMODE, PLEASE REFER TO THE USERS MANUAL'", "Hello friend!", "HUMAN.LIFE MUST = 0"]
        if self.level <= 2:
            print "" 
            print self.name + " says: " + "'" + calls[randint(0, len(calls)-1)] + "'"
         
        else:
            if self.level < 7:
                print "" 
                print self.name + " says: " + calls2[randint(0, 6)]
                
            else:   
                print "" 
                print self.name + " says: " + calls2[randint(6, len(calls2)-1)]

class Boss(object):
    def __init__(self, static_player):
        self.name = "Bossani!"
        self.level = randint(10, 30)
        self.health = randint(int(static_player[1] * (self.level* 0.1)), int(static_player[1] * (self.level* 0.1)))
        self.attack = randint(int(static_player[0] * (self.level* 0.1)), int(static_player[0] * (self.level* 0.1)))
        self.defence = randint(int(static_player[2] * (self.level* 0.1)), int(static_player[2] * (self.level* 0.1)))
        self.life = True
        self.weapon = 5
        self.side = 5
        if self.weapon == 5:
            self.weaponName = "Temple Bat"

        if self.side == 5:
            self.sideName = "Bossanis "
        else:
            self.sideName = "Tail"
    def calls(self):
        calls2 = ["ARHGGGGGG!", "SCREEEECH!", "DIIIIIEEEE!", "RAWWWW!!", "EHHHHHHHCHHH!"]
        print "" 
        print self.name + " says: " + "'" + calls2[randint(0, len(calls2)-1)] + "'"
