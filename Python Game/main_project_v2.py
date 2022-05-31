import pygame
import random
import button
import texts
import math

pygame.init()
clock = pygame.time.Clock()
fps = 60

#window game
stat_panel = 150
screen_width = 800
screen_height = 400 + stat_panel

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Warrior RPG")
#define game variables
current_fighter = 1
total_fighters = 3
action_cooldown = 0 
action_wait_time = 90
lv_points = 0
attack = False
potion = False
target = None
potion_effect = 15
clicked = False
game_over = 0
no_added = True
no_added2 = True
no_added3 = True
no_added4 = True
click_kepper = False
game_lvl = 1
add_lv = False
start_stats = [[10, 6, 40, 6], [6+game_lvl, 4+game_lvl, 1+3*game_lvl, 4]]

#background image
background_image = pygame.image.load('images/usable/background.jpg').convert_alpha()
#Main Map loading
mapa = pygame.image.load('images/World/mapa800x600.png').convert_alpha()
mapaeq = pygame.image.load('images/World/mapaeq800x600.png').convert_alpha()
mapacharacter = pygame.image.load('images/World/mapapostać800x600.png').convert_alpha()
mapalore = pygame.image.load('images/World/mapadziennik800x600.png').convert_alpha()
mapaoptions = pygame.image.load('images/World/mapaopcje800x600.png').convert_alpha()

#panel image
panel_img = pygame.image.load('images/usable/panel.png').convert_alpha()
#stat_add_button
plusik_img = pygame.image.load('images/usable/plusik.png').convert_alpha()
#button images
potion_img = pygame.image.load('images/usable/potion.png').convert_alpha()
restart_img = pygame.image.load('images/usable/restart.png').convert_alpha()
#sword image
sword_img = pygame.image.load('images/usable/sword.png').convert_alpha()
#stat panel
panel_frame = pygame.image.load('images/usable/stat.png').convert_alpha()
panel2_frame = pygame.image.load('images/usable/menu.png').convert_alpha()
panel2start_frame = pygame.image.load('images/usable/menu_1.png').convert_alpha()
panel2exit_frame = pygame.image.load('images/usable/menu_2.png').convert_alpha()
#Arrow load 
arrow_img = pygame.image.load('images/usable/strzałka.png').convert_alpha()
#load victory and defeat images
victory_img = pygame.image.load('images/Endgame/victory/victory.png').convert_alpha()
defeat_img = pygame.image.load('images/Endgame/defeat/defeat.png').convert_alpha()
#Victory update image
knight_stat_image = pygame.image.load('images/Idle/knight/0.png')
knight_stat_image.get_rect()

#def font
font = pygame.font.SysFont('Algerian', 18)
font_1 = pygame.font.SysFont('Algerian', 16)
font_2 = pygame.font.SysFont('Algerian', 8)
font_3 = pygame.font.SysFont('Algerian', 20)
#def col
red = (255, 0 , 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
black = (0, 0, 0)

#create function for drawing text
def text_draw( text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#function for drowing background
def draw_bg():
    screen.blit(background_image, (0,0))
   

def draw_panel():
    screen.blit(panel_img, (-80 ,screen_height - stat_panel))
    # show knight stat
    text_draw(f'{knight.name} HP: {knight.hp}', font, red, 50, screen_height - stat_panel + 30)
    text_draw(f' LV: {knight.lv}', font_3, yellow, 100, screen_height - stat_panel + 95)
    for count, i in enumerate(monster_list):
        text_draw(f'{i.name} HP: {i.hp}', font, red, 550, (screen_height - stat_panel + 30) + count * 40)

#character class
class character():
    def __init__(self, x, y, name, str, defence, max_hp, potion, luck, xp, lv ):
        self.x = x
        self.y = y
        self.name = name
        self.str = str
        self.defence = defence
        self.max_hp = max_hp
        self.hp = max_hp
        self.start_potion = potion
        self.potion = potion    
        self.luck = luck 
        self.xp = xp 
        self.lv = lv  
        self.xp_need = int(20 * (0.8 * lv))
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0     #0 idle, 1 player attack, 2 enemy attack, 3 hurt, 4 death, 5 crit
        self.update_time = pygame.time.get_ticks()
        #load idle images
        temp_list = []
        for i in range(3):
        
            self.img = pygame.image.load(f'images/Idle/{self.name}/{i}.png')
            self.img = pygame.transform.scale(self.img, (self.img.get_width(), self.img.get_height()))
            temp_list.append(self.img)
        self.animation_list.append(temp_list)
        #load attack images for human
        temp_list = []
        for i in range(8):
            self.img = pygame.image.load(f'images/Attack/knight/{i}.png')
            self.img = pygame.transform.scale(self.img, (self.img.get_width(), self.img.get_height()))
            temp_list.append(self.img)
        self.animation_list.append(temp_list)
        #load attack images for enemy
        temp_list = []
        for i in range(4):
            self.img = pygame.image.load(f'images/Attack/monster/{i}.png')
            self.img = pygame.transform.scale(self.img, (self.img.get_width(), self.img.get_height()))
            temp_list.append(self.img)
        self.animation_list.append(temp_list)
        #load hurt images 
        temp_list = []
        for i in range(4):
            self.img = pygame.image.load(f'images/Hurt/{self.name}/{i}.png')
            self.img = pygame.transform.scale(self.img, (self.img.get_width(), self.img.get_height()))
            temp_list.append(self.img)
        self.animation_list.append(temp_list)
        #load death images 
        temp_list = []
        for i in range(5):
            self.img = pygame.image.load(f'images/Death/{self.name}/{i}.png')
            self.img = pygame.transform.scale(self.img, (self.img.get_width() , self.img.get_height()))
            temp_list.append(self.img)
        self.animation_list.append(temp_list)
        #load crit images 
        temp_list = []
        for i in range(4):
            self.img = pygame.image.load(f'images/Crit/{self.name}/{i}.png')
            self.img = pygame.transform.scale(self.img, (self.img.get_width() , self.img.get_height()))
            temp_list.append(self.img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x , y)
    

    def update(self):
        self.animation_cooldown = 150
        #handle animation
        #update image
        self.image = self.animation_list[self.action][self.frame_index]
        #check time to update
        if pygame.time.get_ticks() - self.update_time > self.animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #check amount of animations to restart
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 4:
                self.frame_index = len(self.animation_list[self.action]) - 1
            elif self.action == 3 and crit > 1:
               self.action = 5
               self.frame_index = 0
                
            else:
                self.idle()
    
    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack_hum(self, target):
        #crit dmg
        lv_crit = (self.luck) / 8
        los = random.uniform(0, 1)
        global crit
        crit = lv_crit + (los * lv_crit)
        print(crit)
        #deal dmg
        rand = random.uniform(0.8,1.2)
        damage = (self.str * rand) - (0.4 * self.defence)
        damage = round(damage, 0)
        damage = int(damage)
        self.action = 1
        if crit > 1:
            target.hp -= int(damage * 1.5)
            d_damage = int(damage * 1.5)
            
        else:
            target.hp -= int(damage)
            d_damage = int(damage)
            
        target.hurt()
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(d_damage), red)
        damage_text_group.add(damage_text)
        #set variables to attack animation
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    
    def attack_mon(self, target):
        #crit dmg
        lv_crit = (self.luck) / 8
        los = random.uniform(0, 1)
        global crit
        crit = lv_crit + (los * lv_crit)
        #deal dmg
        
        rand = random.uniform(0.8,1.2)
        damage = (self.str * rand) - (0.4 * self.defence)
        damage = round(damage, 0)
        damage = int(damage)
        self.action = 2
        if crit > 1:
            target.hp -= int(damage * 1.5)
            d_damage = int(damage * 1.5)
        else:
            target.hp -= int(damage)
            d_damage = int(damage)
        #enemy hurt animation
        target.hurt()
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(d_damage), red)
        damage_text_group.add(damage_text)
        #set variables to attack animation
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    
    def hurt(self):
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        self.action = 4
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    
    def restart(self):
        self.alive = True
        self.potion = self.start_potion
        self.action = 0
        self.frame_index = 0
        self.hp = self.max_hp
        self.update_time = pygame.time.get_ticks()
    
    def next_stage(self):
        self.alive = True
        self.potion = self.start_potion
        self.action = 0
        self.hp = self.max_hp
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def draw_ch(self):
        screen.blit(self.image, self.rect)


class HealthBar():
    def __init__(self, x, y ,hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp, max_hp):
        #update with new hp
        self.hp = hp
        self.max_hp = max_hp
        #calculate with new ratio
        ratio = self.hp / self.max_hp   
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 10))
        pygame.draw.rect(screen, green, (self.x , self.y, 150 * ratio, 10))

class XpBar():
    def __init__(self, x, y ,xp, xp_need, lv):
        self.x = x
        self.y = y
        self.xp = xp
        self.xp_need = int(xp_need)
        self.lv = lv
        self.rect2 = pygame.Rect(x,y,150,10)

    
    def draw(self, xp, lv, xp_need):
        #update with new xp
        self.xp = int(xp)
        self.lv = lv
        self.xp_need = xp_need
        #calculate with new ratio
        if self.xp >= self.xp_need:
            self.lv += 1 
            self.xp -= self.xp_need
        self.xp_need = int(20 * (0.8 * self.lv))
        ratio_2 = self.xp / int(self.xp_need)
        pygame.draw.rect(screen, black, (self.x, self.y, 150, 10))
        pygame.draw.rect(screen, yellow, (self.x , self.y, 150 * ratio_2, 10))


class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0
    
    def update(self):
        #move damage text up
        self.rect.y -= 1
        #delete the text after sec
        self.counter += 1
        if self.counter > 30:
            self.kill()

class Sound(pygame.sprite.Sprite):
    def __init__(self, sound_path):
        super().__init__()
        self.sound_path = sound_path
        self.menu_music = pygame.mixer.Sound('sound/Menu/awesomeness.wav')
    def sound(self):
        self.menu_music.play(-1)
        self.menu_music.set_volume(0.2)
    def sound_stop(self):
        self.menu_music.stop()

damage_text_group = pygame.sprite.Group()
sound_group = pygame.sprite.Group()
sound = Sound('awesomeness.wav')
sound_group.add(sound)

knight = character(100 , 285, 'Knight', 10, 6, 40, 1, 6, 0, 1)
monster_1 = character(600, 300, "monster", 6+game_lvl, 4+game_lvl, 1+3*game_lvl, 1, 4, 0, 1)
monster_2 = character(720, 300, "monster", 6+game_lvl, 4+game_lvl, 1+3*game_lvl, 1, 4, 0, 1)
all_list = []
monster_list = []
monster_list.append(monster_1)
monster_list.append(monster_2)
all_list.append(knight)
all_list.append(monster_1)
all_list.append(monster_2)

knight_health_bar = HealthBar(50, screen_height - stat_panel  + 50, knight.hp, knight.max_hp)
monster_1_health_bar = HealthBar(550, screen_height - stat_panel  + 50, monster_1.hp, monster_1.max_hp)
monster_2_health_bar = HealthBar(550, screen_height - stat_panel  + 90, monster_2.hp, monster_2.max_hp)
knight_xp_bar = XpBar(50, screen_height - stat_panel + 70, knight.xp, knight.xp_need, knight.lv)
knight_update_xp_bar = XpBar(knight_stat_image.get_width() + 70, knight_stat_image.get_height() - 50, knight.xp, knight.xp_need, knight.lv)

#create buttons
potion_button = button.Button(screen, 250, screen_height - stat_panel + 40, potion_img, 35,35)
restart_button = button.Button(screen, 370, screen_height - stat_panel + 70, restart_img, 64,64)
add_stat_str = button.Button(screen, knight_stat_image.get_width() + 520, knight_stat_image.get_height() - 90, plusik_img, 40,25)
add_stat_defence = button.Button(screen, knight_stat_image.get_width() + 520, knight_stat_image.get_height() - 60, plusik_img, 40,25)


# RUNNING POSITON # RUNNING POSITON # RUNNING POSITON # RUNNING POSITON # RUNNING POSITON # RUNNING POSITON # RUNNING POSITON # RUNNING POSITON # RUNNING POSITON # RUNNING POSITON # RUNNING POSITON # RUNNING POSITON
run = True
inscription_changer = True
while run:
    #fps 
    clock.tick(fps)

    #Beginning Inscripion       FIRST PART
    while inscription_changer:
        #start play menu sound
        sound.sound()   
        pos = pygame.mouse.get_pos()
        screen.blit(panel2_frame,(0, -25))
        start = pygame.Rect(290,275,220,50)
        exit_fun = pygame.Rect(290,370,220,50)
        #pygame.draw.rect(screen, red, (290, 370, 220, 50))
        #texts.draw()
        if start.collidepoint(pos):
            screen.blit(panel2start_frame,(0, -25))
            if clicked == True:
                inscription_changer = False
        if exit_fun.collidepoint(pos):
            screen.blit(panel2exit_frame,(0, -25))
            if clicked == True:
                pygame.quit()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                        pygame.quit()
            else:
                clicked = False
        pygame.display.update()
            
    #drawing background         First BATTLE    First BATTLE    First BATTLE    First BATTLE    First BATTLE    First BATTLE    First BATTLE    First BATTLE    First BATTLE    First BATTLE    First BATTLE    First BATTLE
    # stop menu sound
    sound.sound_stop()
    #draw bg 
    draw_bg()
    #draw panel
    draw_panel()
    knight_health_bar.draw(knight.hp, knight.max_hp)
    monster_1_health_bar.draw(monster_1.hp, monster_1.max_hp)
    monster_2_health_bar.draw(monster_2.hp, monster_1.max_hp)
    knight_xp_bar.draw(knight.xp, knight.lv, knight.xp_need)
    #draw knight
    knight.update()
    knight.draw_ch()
    #draw monsters
    for monster in monster_list:
        monster.update()
        monster.draw_ch()
    #draw the damage text
    damage_text_group.update()
    damage_text_group.draw(screen)
    #cotrol player action
    #reset action variables
    attack = False
    potion = False
    target = None
    #make sure mouse is visable
    pygame.mouse.set_visible(True)
    pos = pygame.mouse.get_pos()
    for count, characters in enumerate(all_list):
        #characters positioning
        if count == 1:
                characters_pos =  [characters.x - 150, characters.y - 210]
        elif count == 2:
                characters_pos = [characters.x - 210, characters.y - 210]
        else: 
            characters_pos = [characters.x + 60, characters.y - 180]
            
        if game_over == 0:
                pygame.mouse.set_visible(False) 
        #show stat_frame in place of mouse cursos
        if characters.rect.collidepoint(pos):
            if characters.alive == True:
                screen.blit(panel_frame, characters_pos)
                text_draw(f'{characters.name} HP: {characters.hp} / {characters.max_hp}' , font_1, green, characters_pos[0] + 15, characters_pos[1] + 20)
                text_draw(f' Str: {characters.str}' , font_1, green, characters_pos[0] + 10, characters_pos[1] + 40)
                text_draw(f' Def: {characters.defence}' , font_1, green, characters_pos[0] + 10, characters_pos[1] + 60)
                text_draw(f' Luck: {characters.luck}' , font_1, green, characters_pos[0] + 10, characters_pos[1] + 80)
                text_draw(f' Potions: {characters.potion}' , font_1, green, characters_pos[0] + 10, characters_pos[1] + 100)
                text_draw(f' Lv: {characters.lv}' , font_1, red, characters_pos[0] + 80, characters_pos[1] + 120)
            else:
                screen.blit(panel_frame, characters_pos)
                text_draw(f'{characters.name} HP: {characters.hp} / {characters.max_hp}' , font_1, red, characters_pos[0] + 15, characters_pos[1] + 20)
                text_draw(f' Str: {characters.str}' , font_1, green, characters_pos[0] + 10, characters_pos[1] + 40)
                text_draw(f' Def: {characters.defence}' , font_1, green, characters_pos[0] + 10, characters_pos[1] + 60)
                text_draw(f' Luck: {characters.luck}' , font_1, green, characters_pos[0] + 10, characters_pos[1] + 80)
                text_draw(f' Potions: {characters.potion}' , font_1, green, characters_pos[0] + 10, characters_pos[1] + 100)
                text_draw(f' Lv: {characters.lv}' , font_1, red, characters_pos[0] + 80, characters_pos[1] + 120)

    pygame.mouse.set_visible(True)     
    for count, monster in enumerate(monster_list):
        if monster.rect.collidepoint(pos):
            #hide mouse
            if game_over == 0:
                pygame.mouse.set_visible(False)
            #show sword in place of mouse cursos
            screen.blit(sword_img, pos)
            if clicked == True and monster.alive == True:
                attack = True
                target = monster_list[count]
    #show xp
    if knight_xp_bar.rect2.collidepoint(pos):
        text_draw(f'{knight.xp} / {knight.xp_need}' , font_2, green, knight_xp_bar.rect2.centerx - 10, knight_xp_bar.y)

    if potion_button.draw():
        potion = True
        #show number of potions ramining
    text_draw(str(knight.potion), font, red, 290, screen_height - stat_panel + 35)

    if game_over == 0:
        #player action
        if knight.alive == True:
            if current_fighter  == 1:
                action_cooldown += 1
                if action_cooldown >= action_wait_time:
                    #attack
                    if attack == True and target != None:
                        knight.attack_hum(target)
                        current_fighter += 1
                        action_cooldown = 0
                    if potion == True:
                        if knight.potion > 0:
                            #check heal beyond full
                            if knight.max_hp - knight.hp > potion_effect:
                                heal_amount = potion_effect
                    
                            else: 
                                heal_amount = knight.max_hp - knight.hp
                            knight.hp += heal_amount
                            knight.potion -= 1
                            damage_text = DamageText(knight.rect.centerx, knight.rect.y, str(heal_amount), green)
                            damage_text_group.add(damage_text)
                            current_fighter += 1
                            action_cooldown = 0
        else:
            game_over = -1                                                
        #enemy action
        for count, monster in enumerate(monster_list):
            if current_fighter == 2 + count:
                if monster.alive == True:
                    action_cooldown += 1
                    if action_cooldown >= action_wait_time: 
                        if (monster.hp / monster.max_hp) < 0.5 and monster.potion > 0:
                            #check heal beyond full
                            if monster.max_hp - monster.hp > potion_effect / 2:
                                heal_amount = potion_effect / 2
                                heal_amount = round(heal_amount, 0)
                                heal_amount = int(heal_amount)
                            else: 
                                heal_amount = monster.max_hp - monster.hp
                                heal_amount = round(heal_amount, 0)
                                heal_amount = int(heal_amount)
                            monster.hp += heal_amount
                            monster.potion -= 1
                            damage_text = DamageText(monster.rect.centerx, monster.rect.y, str(heal_amount), green)
                            damage_text_group.add(damage_text)
                            current_fighter += 1
                            action_cooldown = 0
                        else:
                            #attack
                            monster.attack_mon(knight)
                            current_fighter += 1
                            action_cooldown = 0
                else: 
                    current_fighter += 1   
        
        #if all fighter have had a turn
        if current_fighter > total_fighters:
            current_fighter = 1
    # check if all bandits are dead
    alive_monsters = 0
    for monster in monster_list:
        if monster.alive == True:
            alive_monsters += 1
    if alive_monsters == 0:
        game_over = 1

    #check if game is over 
    if game_over !=0:
        if game_over == 1:
            #creating timer for events
            if no_added3:
                time_keeper = pygame.time.get_ticks()
                no_added3 = False
            screen.blit(victory_img,(0,0))
            if pygame.time.get_ticks() - time_keeper > 1000:
                screen.blit(knight_stat_image,(50, 0))
                text_draw(f'{knight.name}' , font_3, red, knight_stat_image.get_width() - 30, knight_stat_image.get_height())
                text_draw(f'LV: {knight.lv}' , font_3, yellow, knight_stat_image.get_width() + 120, knight_stat_image.get_height() - 30)

                #XP_BAR BLIT
                if no_added and pygame.time.get_ticks() - time_keeper > 2000:
                    for i in range(knight.xp_need):
                            knight.xp += 1
                            if knight.xp == knight.xp_need:
                                knight.lv += 1
                                lv_points += 3 
                                knight.xp -= knight.xp_need
                            knight_update_xp_bar.draw(knight.xp, knight.lv,  knight.xp_need) 
                            knight.xp_need = int(20 * (0.8 * knight.lv))
                            #print(knight.xp_need)
                            pygame.display.update()
                            if knight.lv > 5:
                                pygame.time.wait(50-int(round(knight.lv * 2.5, 0)))
                            else:
                                pygame.time.wait(50-int(round(knight.lv * 1.7, 0)))
                    no_added = False
                    add_lv = True
                knight_update_xp_bar.draw(knight.xp, knight.lv, knight.xp_need)

        else: 
            screen.blit(defeat_img,(0,0))
            if restart_button.draw():
                for champions in all_list:
                    champions.restart()
                current_fighter = 1
                action_cooldown = 0
                game_over = 0
        # adding stats to the enemies
        if no_added4:
            for monster in monster_list:
                monster.max_hp += 4 * math.ceil(game_lvl * 0.5)
                monster.str += 1 * math.ceil(game_lvl * 22.5)
                monster.defence += 1 * math.ceil(game_lvl * 0.5)
                monster.lv += 1
                if monster.lv % 2 == 0:
                    monster.luck += 1
                else:
                    monster.luck += 2
                no_added4 = False
        # ADDING STATS AFTER BATTLE    # ADDING STATS AFTER BATTLE    # ADDING STATS AFTER BATTLE    # ADDING STATS AFTER BATTLE    # ADDING STATS AFTER BATTLE    # ADDING STATS AFTER BATTLE    # ADDING STATS AFTER BATTLE
        if add_lv == True:
            if no_added2 == True:
                knight.max_hp += knight.max_hp * 0.2
                knight.max_hp = int(knight.max_hp)
                knight.hp = knight.max_hp
                knight.luck += 2
                no_added2 = False
            if add_stat_str.draw() and lv_points > 0:
                knight.str += 1
                lv_points -= 1
            if add_stat_defence.draw() and lv_points > 0:
                knight.defence +=1
                lv_points -= 1
            text_draw(f'You have {lv_points} talent points to spend' , font, green, knight_stat_image.get_width() + 370, knight_stat_image.get_height() - 120)
            text_draw(f' Str {knight.str}' , font_3, red, knight_stat_image.get_width() + 430, knight_stat_image.get_height() - 90)
            text_draw(f' Def {knight.defence}' , font_3, red, knight_stat_image.get_width() + 430, knight_stat_image.get_height() - 60)
            
        #health_rect = pygame.Rect(200,300, 50,30)
        #pygame.draw.rect(screen, black,(200,300, 50,30))
        #if health_rect.collidepoint(pos):
            #if clicked == True:
            
    #Main Map loading    #Main Map loading    #Main Map loading    #Main Map loading    #Main Map loading    #Main Map loading    #Main Map loading    #Main Map loading    #Main Map loading    #Main Map loading
            if lv_points == 0 and add_lv == True: 
                screen.blit(arrow_img, (300,screen_height - stat_panel))
                arrow = pygame.Rect(345,screen_height - stat_panel, 120,80)
                if arrow.collidepoint(pos):
                    if clicked == True and pygame.time.get_ticks() - time_keeper > 3000:
                        click_kepper = True
                
                if click_kepper == True:
                    for champions in all_list:
                        champions.next_stage()
                    click_kepper = False
                    current_fighter = 1
                    action_cooldown = 0
                    game_over = 0
                    add_lv = False
                    no_added = True
                    no_added2 = True
                    no_added3 = True
                    no_added4 = True
    # Event Buttons    # Event Buttons    # Event Buttons    # Event Buttons    # Event Buttons    # Event Buttons    # Event Buttons    # Event Buttons    # Event Buttons    # Event Buttons    # Event Buttons
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
        else:
            clicked = False
    
    pygame.display.update()
pygame.quit()
