import pygame,random,copy
import json

#optional thing choose where the pictures are taken from when using fname
art_folder = ""

#colisions and bounce curently not working
#rotation is not used in colisions




#particles have class with all the info 
def add_arrs(arr1,arr2):
    for i in range(len(arr1)):
        arr1[i]+=arr2[i]
    return arr1
def arr_min_max(arr,mini,maxi):
    for i in range(len(arr)):
        if arr[i]<mini:
            arr[i] = mini
        elif arr[i]>maxi:
            arr[i] = maxi
    return arr
class Inheritance():
    def __init__(self,Colour=0,Size=0,Pos=0,Timer=0):
        self.Colour = Colour
        self.Size = Size
        self.Pos  = Pos
        self.Timer = Timer
def circle_surf(radius, color):
    surf = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0, 0, 0))
    return surf
def two_circle_colision(pos1,size1,pos2,size2):#position is top left
    distance_squared = (pos1[0]+size1 - (pos2[0]+size2))**2 + (pos1[1]+size1 - (pos2[1]+size2))**2
    # check for collision
    if distance_squared <= (size1 + size2)**2:
        return 1
    else:
        return 0
def circle_rect_colision(pos1,radius,pos2,size): #pos1 is circle,pos2 is rectangle
    closest_x = max(pos2[0], min(pos1[0]-radius, pos2[0] + size[0]))
    closest_y = max(pos2[1], min(pos1[1]-radius, pos2[1] + size[1]))
    # calculate squared distance between closest point and center of circle
    distance_squared = (closest_x - pos1[0]-radius)**2 + (closest_y - pos2[1])**2
    # check for collision
    if distance_squared <= radius**2:
        return 1
    else:
        return 0
# def reg_bounce():
def bounce_off(rect1,rect2,Cpos,bounce):
    if rect1.top < rect2.bottom and rect1.bottom > rect2.bottom:#top touch bottom
        if Cpos[1]<0:#if heading up
            rect1.top = rect2.bottom
            Cpos = [-bounce*Cpos[0],-bounce*Cpos[1]]
    if rect1.bottom > rect2.top and rect1.top < rect2.top:#its bottom touches top
        if Cpos[1]>0:#if heading down
            Cpos = [-bounce*Cpos[0],-bounce*Cpos[1]]
            rect1.bottom = rect2.top
    if rect1.left < rect2.right and rect1.right > rect2.right:#left touch right
        if Cpos[0]<0:#if heading up
            rect1.left = rect2.right
            Cpos = [-bounce*Cpos[0],-bounce*Cpos[1]]
    if rect1.right > rect2.left and rect1.left < rect2.left:#its bottom touches top
        if Cpos[0]>0:#if heading down
            Cpos = [-bounce*Cpos[0],-bounce*Cpos[1]]
            rect1.right = rect2.left
    # if rect.left < tile.right:
    #     colisions['left'].append(tile)
    # if rect.right > tile.left:
    #     colisions['right'].append(tile)
    return Cpos,[rect1.left,rect1.top]
def mini_rectater(pos,size):#used by rectater
    if len(size)<2:#circle
        rect = pygame.Rect(pos[0]-size[0],pos[1]-size[0],size[0],size[0])
    else: #square
        rect = pygame.Rect(pos[0]-size[0]/2,pos[1]-size[1]/2,size[0],size[1])
    return rect
        
def rectater(pos1,size1,pos2,size2):#assumes offcenter particle#figures out if rect or circle and turns them into two rects
    rect1 = mini_rectater(pos1,size1)
    rect2 = mini_rectater(pos2,size2)
    return rect1,rect2

class Particle():
    def __init__(self,Shape = "circle",Colour = [0,0,0,255],Size = [10,10],Pos=[0,0],Light = 0,Timer = -1,Cpos=0,Csize =0,Ccolour = 0,A=0,Create_particle= 0,Bounce=0,Tag=0,RealPos=0,Fname=0,Border =0, Cborder = 0, Rotation = 0, Crotation = 0):
        # follow shapes:spiral, circle, square, sin
        # modifications of these shapes are put into it
        # all things will need to be random
        if len(Colour)<4:#Visible but alpha missing
            Colour.append(255)
        if Ccolour:
            if len(Ccolour)<4:#Visible
                Ccolour.append(255)
        if Shape != "circle" and Shape != "rect":
            Size = [Shape.get_width(), Shape.get_height()]
        if type(Size) != list:
            Size = [Size,Size]
        if Csize and type(Csize) != list:
            Csize = [Csize,Csize]
        if Shape == 0 and Fname != 0:
            Shape = pygame.image.load(art_folder+Fname)
        
        self.Colour = Colour
        self.Size = Size
        self.Shape = Shape
        self.Light = Light
        self.Pos  = Pos
        #C = change per frame
        self.Timer = Timer #-1 means has no timer |decreases, when 0 the particle can terminate
        self.Csize = Csize
        self.Cpos = Cpos #aka velocity
        self.Ccolour = Ccolour
        self.Create_particle = Create_particle #0 unles [particle class,[0]]<--inherits nothing if an Inherite class inherits those traits if true
        self.A = A
        self.Bounce = Bounce #true or false to bounce on colision, also is bonce efficeny 0,100
        self.Tag = Tag#place for extra information
        self.RealPos = RealPos
        self.Fname = Fname#image that needs to be pulled up to make image
        self.Border = Border
        self.Cborder = Cborder
        self.Rotation = Rotation
        self.Crotation = Crotation
        #got to add real pos#only for real stuff
    def save(self,name='name',folder=''):
        if self.Fname:
            self.Shape = 0
        to_s = {"Shape":self.Shape,
                "Colour":self.Colour,
                "Size":self.Size,
                "Pos":self.Pos,
                "Light":self.Light,
                "Timer":self.Timer,
                "Cpos":self.Cpos,
                "Csize":self.Csize,
                "Ccolour":self.Ccolour,
                "A":self.A,
                "Create_particle":self.Create_particle,
                "Bounce":self.Bounce,
                "Tag":self.Tag,
                "RealPos":self.RealPos,
                "Fname":self.Fname,
                "Border":self.Border,
                "Cborder":self.Cborder,
                "Rotation":self.Rotation,
                "Crotation":self.Crotation
                }
        #we also want it so that their can be like smaller versions that use a full version to get the rest of their information/start all the blanks at wierd values so those specificaly get replaced
        with open(folder+name+'.json', 'w') as f:
            json.dump(to_s, f,indent = 2)

    def run(self):
        if self.Border:
            self.Border += self.Cborder
            if self.Border <1:# this way 
                self.Border = 1
                self.Timer = 1# this will mean it will be terminated after disapearing 
        if self.Ccolour:
            self.Colour = add_arrs(self.Colour,self.Ccolour) #increase colours
            self.Colour = arr_min_max(self.Colour,0,255)
        if self.RealPos:
            self.RealPos = add_arrs(self.RealPos,self.Cpos)
        elif self.Cpos:
            self.Pos = add_arrs(self.Pos,self.Cpos)
        if self.A:
            self.Cpos = add_arrs(self.Cpos,self.A)
        
        if self.Csize:
            self.Size = add_arrs(self.Size,self.Csize)
            self.Size = arr_min_max(self.Size,0,9999)
        
        if self.Crotation:
            self.Rotation += self.Crotation
        
        self.Timer -=1
        
        #if self.create_particle !=0:
        #return(self.Create_particle) #allows particles to create particles
        
    def adjust_pos(self,RelPos):#shows compared to a relative position, showPos = RealPos - RelPos
        self.Pos[0] = self.RealPos[0] - RelPos[0]
        self.Pos[1] = self.RealPos[1] - RelPos[1]
    def show(self,surf,RelPos= 0):
        if RelPos:
            if self.RealPos:#if I have a position that is relative
                self.adjust_pos(RelPos)
        if self.Shape == "circle":#particle is circle
            surf2 = pygame.Surface((self.Size[0] * 2, self.Size[0] * 2),pygame.SRCALPHA)
            pygame.draw.circle(surf2, self.Colour, (self.Size[0], self.Size[0]), self.Size[0],round(self.Border))
            if self.Light == 0:
                surf.blit(surf2,(self.Pos[0]-self.Size[0],self.Pos[1]-self.Size[0]))
            else:
                surf.set_colorkey((0, 0, 0))
                surf.blit(surf2,(self.Pos[0]-self.Size[0],self.Pos[1]-self.Size[0]),special_flags = pygame.BLEND_RGB_ADD)
        elif self.Shape == "rect":#rectangle
            surf2 = pygame.Surface((self.Size[0], self.Size[1]),pygame.SRCALPHA)
            pygame.draw.rect(surf2, self.Colour,[0,0,self.Size[0],self.Size[1]])
            if self.Rotation:
                surf2 = pygame.transform.rotate(surf2, self.Rotation)
            
            if self.Light == 0:
                if not self.Rotation:
                    surf.blit(surf2,(self.Pos[0]-self.Size[0]/2,self.Pos[1]-self.Size[1]/2))
                else:
                    surf.blit(surf2,(self.Pos[0]-surf2.get_width()/2,self.Pos[1]-surf2.get_height()/2))
            else:
                surf.set_colorkey((0, 0, 0))
                if not self.Rotation:
                    surf.blit(surf2,(self.Pos[0]-self.Size[0]/2,self.Pos[1]-self.Size[1]/2),special_flags = pygame.BLEND_RGB_ADD)
                else:
                    surf.blit(surf2,(self.Pos[0]-surf2.get_width()/2,self.Pos[1]-surf2.get_height()/2),special_flags = pygame.BLEND_RGB_ADD)
        else:#if image pygame image that is already loaded
            surf2 = pygame.Surface((self.Size[0], self.Size[1]),pygame.SRCALPHA)
            stretched_img = pygame.transform.scale(self.Shape,(int(self.Size[0]),int(self.Size[1])))
            surf2.blit(stretched_img,(0,0))
            if self.Rotation:
                surf2 = pygame.transform.rotate(surf2, self.Rotation)
            if self.Colour[3] !=255:
                surf2.set_alpha(self.Colour[3])
            if self.Light == 0:
                if not self.Rotation:
                    surf.blit(surf2,(self.Pos[0]-self.Size[0]/2,self.Pos[1]-self.Size[1]/2))
                else:
                    surf.blit(surf2,(self.Pos[0]-surf2.get_width()/2,self.Pos[1]-surf2.get_height()/2))
            else:
                surf.set_colorkey((0, 0, 0))
                if not self.Rotation:
                    surf.blit(surf2,(self.Pos[0]-self.Size[0]/2,self.Pos[1]-self.Size[1]/2),special_flags = pygame.BLEND_RGB_ADD)
                else:
                    surf.blit(surf2,(self.Pos[0]-surf2.get_width()/2,self.Pos[1]-surf2.get_height()/2),pygame.BLEND_RGB_ADD)
                
        return surf

    def inherite(self,old_particle,inheritance):
        if inheritance.Colour == 1:
            self.Colour = old_particle.Colour
        if inheritance.Pos == 1:
            self.Pos = copy.deepcopy(old_particle.Pos)#add_arrs(self.Pos, old_particle.Pos)
        if inheritance.Size == 1:
            self.Size = old_particle.Size
        if inheritance.Timer == 1:
            self.Timer = old_particle.Timer
    
        
    def check_colide(self,pos,size,shape):#assuming the positions have been turned to middle
        ret = 0
        if self.Shape == 'circle':#particle is sicle
            if shape == "circle":#shape is circle
                if two_circle_colision([self.Pos[0]-self.Size[0],self.Pos[1]-self.Size[0]], self.Size[0], [pos[0]-size[0],pos[1]-size[0]], size[0]):
                    ret = 1
            elif circle_rect_colision([self.Pos[0]-self.Size[0],self.Pos[1]-self.Size[0]], self.Pos[1], [pos[0]-size[0]/2,pos[1]-size[1]/2], size):
                    ret = 1#if square
        else:#square
            if shape == "circle":
                if circle_rect_colision((pos[0]-size[0],pos[1]-size[0]), size[0], [self.Pos[0]-self.Size[0]/2,self.Pos[1]-self.Size[1]/2], self.Size):
                    ret = 1
            else:#rect rect
                rect = pygame.Rect(self.Pos[0]-self.Size[0]/2,self.Pos[1]-self.Size[1]/2,self.Size[0],self.Size[1])
                rect2 = pygame.Rect(pos[0]-size[0]/2,pos[1]-size[1]/2,size[0],size[1])
                if rect.colliderect(rect2):
                    ret = 1
        if ret:
            if self.Bounce >0:
                rect1,rect2 = rectater(self.Pos,self.Size,pos,size)
                self.Cpos,self.Pos = bounce_off(rect1, rect2, self.Cpos, self.Bounce)
                self.Pos = [self.Pos[0] + self.Size[0]/2,self.Pos[1] + self.Size[1]/2]
        return ret
    def check_colide2(self,rect2):#checks colisions with
        rect1 = mini_rectater(self.Pos, self.Size)
        if rect1.colliderect(rect2):
            self.Cpos,self.Pos = bounce_off(rect1, rect2, self.Cpos, self.Bounce)
            self.Pos = [self.Pos[0] + self.Size[0]/2,self.Pos[1] + self.Size[1]/2]
       
            
#i susspect has something to do with the for loop or specificaly Pos
#suspect inherite sin others dont use it but when inherits hapen issue hapens setting it to a part in the class
def save_particles(particles,name='name',folder=''):
    for particle in particles:
        particle.save(name,folder)
        
#could consider making an alternative that checks for the keys before
def load_particle(fname="name",folder ="",prename = 0):#loads item 
    if not prename:#if the extension has not already been named
        text =  json.load(open(folder+fname+'.json'))
    else:#.json is already in the item name
        text =  json.load(open(folder+fname))
    particle = Particle(text['Shape'],text['Colour'],text['Size'],text['Pos'],text['Light'],text['Timer'],text['Cpos'],text['Csize'],text['Ccolour'],text['A'],text['Create_particle'],text['Bounce'],text['Tag'],text['RealPos'],text['Fname'],text['Border'],text['Cborder'],text['Rotation'],text['Crotation'])
    return particle
def run_particles(particles):
    #new_particles = []
    for particle in particles:
        particle.run()
    # new_particles = []
    # for particle in particles:
    #     new_particle = particle.run()
    #     if new_particle !=0:
    #         new_particle[0].inherite(particle,new_particle[1])
    #         new_particles.append(copy.deepcopy(new_particle[0]))
    # for new_particle in new_particles:
    #     particles.insert(0,new_particle)
    return particles
def show_particles(surf,particles,RelPos=0):
    for particle in particles:
        surf = particle.show(surf,RelPos)
    return surf
def purge_particles(particles):
    difrence = 0
    for i in range(len(particles)):
        real_spot = i-difrence
        if particles[real_spot].Timer == 0:
            difrence+=1
            particles.pop(real_spot)
    return particles

#if its not particles then must all be lines or rectangles
def colide_particles(particles,particles2,dup=0):#assuming arr2 also particles,dup means same list
    for i,particle in enumerate(particles):
        for j,particle2 in enumerate(particles2):
            colide = 0
            if not dup:
                colide = particle.check_colide(particle2.Pos,particle2.Size,particle2.Shape)
            else:
                if not i ==j: 
                    colide = particle.check_colide(particle2.Pos,particle2.Size,particle2.Shape)#if duplicate particle arrays dont read yourself
            if colide:#write colision code here
                #wierd bounce physics
                # if particle.Bounce >0:
                #     particle.Cpos = [-abs(particle.Bounce)*particle.Cpos[0],-abs(particle.Bounce)*particle.Cpos[1]] 
                if particle.Tag == 'colours':
                    particle.Colour = [random.randint(150,200),random.randint(150,200),random.randint(150,200),255]
    return particles
#below should be super useful for like bullets and enemys
def colide_particles_rects(particles,rects):#rects: a string of pygame rectstyle objects
    for particle in particles:
        for rect in rects:
            colide = particle.check_colide2(rect)
            if colide:#write colision code here
                particle.Colour = [0,0,0,255]
                pass
    return particles 