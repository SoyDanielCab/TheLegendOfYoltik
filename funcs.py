import pygame, sys
from pygame.locals import *
import os.path


SCREENRECT = Rect(0, 0,640, 480)
level_font = "PressStart2P-Regular.ttf" #Game font
level_txt = "Level " #level indicator


def load_image(file):
    file = os.path.join('images', file)
    print("load_image( " + file + " )")

    
    
    if not pygame.display.get_init():
        init()
    try:
        surface = pygame.image.load(file)
        print("pygame image surface apparently loaded")
    except pygame.error:
        print("pygame ERR0R in load_image():: " + pygame.get_error())
        surface = pygame.image.load("images/" + file)
        raise SystemExit( '%s: Impossible de charger l\'image "%s"' % (pygame.get_error(), file))
    return surface.convert_alpha()




def load_images(*files):
    imgs = []
    print("load_images() --> imgs[]")
    
    for file in files:
        imgs.append(load_image(file))
        print("Appending image, "+file)
    return imgs

def load_font(font_name,size):
    font = pygame.font.Font(font_name,size)
    return font

def make_pause(duration):
    from time import sleep
    sleep(duration)

class SoundGroup:
    sounds = []
    
    def add(self, snd):
        if isinstance(snd, pygame.mixer.Sound):
            self.sounds.append(snd)
            snd.set_volume(soundvol)
            
    def set_volume(self, vol):
        for snd in self.sounds:
            snd.set_volume(vol)

class dummysound:
    def play(self):
        print("WARNING: Using dummysound()")
    

def load_sound(file):
    global sndgrp

    if not pygame.display.get_init():
        init()
    
        if not pygame.mixer: return dummysound()
    else:
        print("load_sound did not need to init()")
    
    file = os.path.join('sound', file)
    try:
        sound = pygame.mixer.Sound(file)
        sndgrp.add(sound)
        print("Loaded sound file, " + file)
        return sound
    except pygame.error:
        print ('Warning, unable to load,', file)
    return dummysound()

def load_music(file):
    file = os.path.join('sound',file)
    try:
        pygame.mixer.music.load(file)
        print("Sound mixer loaded, apparently...")
    except pygame.error:
        print ('Warning, unable to load', file)

def play_music():
    try:
        pygame.mixer.music.play(-1)
        print("Music loaded... apparently...")
    except pygame.error:
        print ('Warning, music not loaded')

def init():
    global screen, clock, sndgrp

    if pygame.display.get_init():
        return
    
    #Impresions for console
    print("init()")
    pygame.init()
    clock = pygame.time.Clock()
    load_config()
    print("load_config() ended, going on...")
    
    screen = pygame.display.set_mode(SCREENRECT.size, fscreen*FULLSCREEN)
    pygame.display.set_caption('Eco Adventure') 
    pygame.mouse.set_visible(0)
    
    print("Going to load music...")
    
    pygame.mixer.music.set_volume(musicvol)
    sndgrp = SoundGroup()
    print("Music/sound set up. Running play_music()")
    play_music()
    print("Okay, init() is done...")

def load_config():
    global musicvol, soundvol, fscreen

    conf = None

    try:
        #Game configuration
        conf = open('pydza.conf')
        config = conf.readlines()
        conf.close()
        print ("Loading configuration.")
        
        for str in config:
            
            x = str.find("=")
            if x != -1:
                if str[:x] == "fullscreen":
                    fscreen = int(str[x+1:])
                    print ("\tfullscreen=" + fscreen.__str__())
                elif str[:x] == "musicvol":
                    musicvol = float(str[x+1:])
                    print ("\tmusicvol=" + musicvol.__str__())
                elif str[:x] == "soundvol":
                    soundvol = float(str[x+1:])
                    print ("\tsoundvol=" + soundvol.__str__())
        print("Valid config file, apparently.")
    
    except IOError:
        print ("No configuration file. Using default.")
        write_config(["fullscreen",0],["musicvol",1.0],["soundvol", 1.0])
        musicvol = 1.0
        soundvol = 1.0
        fscreen = 0

def write_config(*opt):
    print ("Writing configuration.")
    try:
        
        conf = open('pydza.conf', 'a+')
        
        config = conf.readlines()
        
        for o in opt:
            bFound = 0
            
            for line in config:
                if line.find(o[0]) != -1:
                    bFound = 1
                    break
            
            if bFound:
                
                config.remove(line)
                y = line.find('\n')
                
                line = line.replace(line[len(o[0])+1:y], str(o[1]))
                print ('\t' + line.replace('\n', ''))
                
                config.append(line)
            
            else:
                
                config.append(o[0] + "=" + str(o[1]) + "\n")
                print ('\t' + config[-1].replace('\n', ''))
    
        
        conf.seek(0)
        
        conf.truncate()
        
        conf.writelines(config)
        
        conf.close()
    except IOError:
        print ("Warning: Can't write configuration file.")

print("bg.png")
bgdtile = load_image('bg.png')
print("Background loaded")
pygame.display.set_icon(pygame.image.load("images/stop1.png"))
print("icon loaded")

def draw_background():
    global screen, background

    background = pygame.Surface(SCREENRECT.size)
    background.blit(bgdtile, (0,0))
    screen.blit(background, (0,0))
    pygame.display.flip()

def draw_levelnum(num, author):
    draw_background()

    police = load_font(level_font,30)
    text = level_txt+str(num+1)
    surf_text = police.render(text, True,(246,180,53))
    
    dirty = [screen.blit(surf_text,(230,235))]


    if author != "":
        police = load_font(level_font,15)
        text = "by %s" % author
        

        surf_text = police.render(text, True,(246,180,53))
        dirty.append(screen.blit(surf_text,(480, 448)))
        


    pygame.display.update(dirty)
    make_pause(2)

    draw_background()


"""
    if frs != "":
        police = load_font(level_font,15)
        text = "by %s" % frs
        

        surf_text = police.render(text, True,(146,180,53))
        dirty.append(screen.blit(surf_text,(480, 448)))
"""
    