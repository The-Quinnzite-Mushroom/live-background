import pygame
import ctypes
from pynput import mouse
import qparticles as qp
import random

#things you need to change:

dip_size = [1920,1080] #your computers resolution
#the complete path of the folder the live bg photo will be in
pic_folder = 'C:/Users/quinn/eclipse-workspace/1_games/random_stuff/pictures/'

walpaper_mode = 4#0 is none
#1 : lily pads and white circles
#2 : lily pads and white circles only when click
#3 : red stuff
#4 : bunch of blue stuff falls from the sky

blue_man = qp.Particle(Shape = "rect",Size = [20,20],Csize = [0.5,0.5] ,Colour = [100,150,200],Ccolour = [-1,-1,-1],Cpos = [random.randint(-3,3),random.randint(3,6)],Timer = 250,Pos = [random.randint(0,dip_size[0]),0],Rotation = 0,Crotation = 30)
blue_man = qp.Particle()
blue_man.save("blue")

pygame.init()
display = pygame.Surface(dip_size)

def set_wallpaper(image_path):
    SPI_SETDESKWALLPAPER = 20
    # Change the wallpaper
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)
    
clock = pygame.time.Clock()
clock_rate = 60
xy = (0,0)
pressed2 = 0
particles = [] #list to be filled with particles
particles.append(blue_man)

    
def on_move(x, y):
    global xy
    xy = ((x,y))

def on_click(x, y, button, pressed):
    global pressed2
    pressed2 = pressed
    pass
    if not pressed:
        return False

def on_scroll(x, y, dx, dy):
    pass
    

quiting = 0
while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                pygame.quit()
                quiting = 1
                break
    if quiting:
        break
    
    #pynput stuff
    listener = mouse.Listener(on_move=on_move,on_click=on_click,on_scroll=on_scroll)
    listener.start()
    

    if walpaper_mode:
        if walpaper_mode == 1 or walpaper_mode == 2: #water
            display.fill((40,204,223))
            if walpaper_mode == 1 or (walpaper_mode ==2 and pressed2):
                particles.append(qp.Particle(Shape = "circle",Size = [4,4],Csize = [4,4] ,Colour = [100,50,100],Timer = 100,Pos = [xy[0],xy[1]],Border = 15,Cborder = -1,Light =1))
        if walpaper_mode == 3:
            display.fill((200,200,200))
            #fire
            particles.append(qp.Particle(Shape = "rect",Size = [20,20],Csize = [0.5,0.5] ,Colour = [200,100,100],Ccolour = [-1,-1,-1],Cpos = [random.randint(-3,3),-random.randint(3,6)],Timer = 100,Pos = [xy[0],xy[1]],Rotation = 25,Crotation = 10))
        if walpaper_mode == 4:
            display.fill((150,150,150))
            #water stuff coming down
            particles.append(qp.Particle(Shape = "rect",Size = [20,20],Csize = [0.5,0.5] ,Colour = [100,150,200],Ccolour = [-1,-1,-1],Cpos = [random.randint(-3,3),random.randint(3,6)],Timer = 250,Pos = [random.randint(0,dip_size[0]),0],Rotation = 0,Crotation = 30))
            particles.append(qp.Particle(Shape = "rect",Size = [20,20],Csize = [0.5,0.5] ,Colour = [100,150,200],Ccolour = [-1,-1,-1],Cpos = [random.randint(-3,3),random.randint(3,6)],Timer = 250,Pos = [random.randint(0,dip_size[0]),0],Rotation = 0,Crotation = 30))
        if walpaper_mode == 5:
            pass
        #makes particles run, show and delete
        particles = qp.purge_particles(particles)
        particles = qp.run_particles(particles)
        display = qp.show_particles(display,particles)
        #saves pygame display as pic and sets it as bg
        pygame.image.save(display,pic_folder+'pic.png')
        set_wallpaper(pic_folder+'pic'+".png")
        
    
            
    
    clock.tick(clock_rate)
pygame.quit()