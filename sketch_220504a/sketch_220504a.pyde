#add/import essential libraries
add_library('minim')
import random

#initialize variables
day_ost = None
night_ost = None
ultimate_ost = None
ost_playlist = []

background_static = None
background_active = None

cloud_gallery = None

Lx1 = 200
Lx2 = 700
Mx1 = 800
Mx2 = 550
Mx3 = 100
Sx1 = 400
Sx2 = 450

face = None
sun = None
moon = None

S_angleRotate = 270
M_angleRotate = 90

total = 0
msg_x = 675

rain = []

#===============================================================================================================================
#===============================================================================================================================
#===============================================================================================================================

def initialize_image(bH, bW, cS, cI, cX, cY, cpX, cpY, canX, canY):
    backHeight = bH #background image height
    backWidth = bW  #background image width
    
    chunkSize = cS   #source image width; how much of the image we want to see
    chunkIncr = cI   #increment; used to increase the speed of background image movement
    chunkX = cX      #x coordinate of the source image upper left corner
    chunkY = cY      #y coordinate of the source image upper left corner
    
    cornerPointX = cpX #x coordinate of the destination image upper left corner
    cornerPointY = cpY #y coordinate of the destination image upper left corner
    
    canvasX = canX #destination image width
    canvasY = canY #destination image height
    
    return chunkX, chunkY, chunkIncr, chunkSize, backHeight, backWidth, cornerPointX, cornerPointY, canvasX, canvasY

#===============================================================================================================================
#===============================================================================================================================
#===============================================================================================================================

def active_image(chunkX, chunkIncr, chunkSize, backWidth):
    chunkX += chunkIncr #increments the X coordinate of the source image upper left corner
    if ( chunkX + chunkSize ) >= backWidth: #if the X coordinate and size is greater than the background image width
        chunkX = 0 #reset it to 0
        
    return chunkX, chunkIncr, chunkSize, backWidth
        
#===============================================================================================================================
#===============================================================================================================================
#===============================================================================================================================

def draw_cloud(c, x, y, Incr, gap):
    image(c, x, y)
    x -= Incr
    if x + 150 < 0:
        x = width
    return x
    
#===============================================================================================================================
#===============================================================================================================================
#===============================================================================================================================
class Drop():
    
    def __init__(self, x, y, z, ):
        self.x = x
        self.y = y
        self.z = z
        self.yspeed = map(z, 0, 20, 4, 10)
        self._length_ = map(z, 0, 20, 10, 15)
        self.thick = map(z, 0, 20, 0.02, 0.1)
        
    def fall(self):
        self.y += self.yspeed
        self.yspeed += 0.05
        
        if self.y > height:
            self.y = random.randint(-200, -100)
            self.yspeed = map(self.z, 0, 20, 4, 10)
        
    def show(self):
        stroke(random.randint(200, 225),random.randint(200, 225),random.randint(200, 225))
        strokeWeight(self.thick)
        line(self.x, self.y, self.x, self.y + self._length_)   

#===============================================================================================================================
#===============================================================================================================================
#===============================================================================================================================    
            
def sun_moon(x, S_AR, M_AR, check, f):
    noStroke()
    fill(252, 229, 112)
    f.resize(65, 65)
    
    pushMatrix()
    translate(333, 300)
    rotate(radians(S_AR))
    ellipse(x, 0, 70, 70)
    tint(255, 40)
    image(f, x - 32.5, -32.5)
    popMatrix()
    
    S_AR += 0.12075
    
    fill(254, 252, 215)

    pushMatrix()
    translate(333, 300)
    rotate(radians(M_AR))
    ellipse(x, 0, 70, 70)
    tint(255, 40)
    image(f, x - 32.5, -32.5)
    popMatrix()
    
    tint(255)
    
    M_AR += 0.12075
    
    if check == 0:
        S_AR = 270
        M_AR = 90
        
    return S_AR, M_AR 
    
#===============================================================================================================================
#===============================================================================================================================
#===============================================================================================================================
    
def display_text(days, x, check):
    
    if check == 0:
        days += 1
    
    if days == 2:
        text('"You will never be able to love anybody else until you love yourself." - Lelouch Lamperouge (Code Geass)', x, 50)
        x -= 0.5
    elif days > 2:
        x = 675
        days = 0
        
    return days, x

#===============================================================================================================================
#===============================================================================================================================
#===============================================================================================================================

def play_music(btn, song):
    active = song
    #set infinite loop; song will rewind and begin playing when song ends
    if active.isPlaying() == False:
        active.rewind()
        active.play()
        

#===============================================================================================================================
#===============================================================================================================================
#===============================================================================================================================

class button():
    
    def __init__(self, img):
        self.img = img
    
#===============================================================================================================================
#===============================================================================================================================
#===============================================================================================================================

def setup():
    #global sound and background assets
    global day_ost, night_ost, ultimate_ost, ost_playlist
    global background_static, background_active
    global cloud_L1, cloud_L2, cloud_M1, cloud_M2, cloud_M3, cloud_S1, cloud_S2
    global face, sun, moon, angleRotate
    
    #define window size and framerate (frames per second)
    size(666, 475)
    ellipseMode(CENTER)
    frameRate(60)
    
    #initialize minim
    m = Minim(this)
    
    #load and play music file
    day_ost = m.loadFile("let_love_win.mp3")
    night_ost = m.loadFile("the_calling.mp3")
    ultimate_ost = m.loadFile("monody.mp3")
    ost_playlist = [day_ost, night_ost, ultimate_ost]
    
    #global active background variables
    global bg_cornerPointX, bg_cornerPointY, bg_canvasX, bg_canvasY
    global bg_backHeight, bg_backWidth, bg_chunkSize, bg_chunkIncr, bg_chunkX, bg_chunkY
    
    #load images into variables
    background_static = loadImage("firewatch.png")
    background_active = loadImage("day_night.png")
    
    cloud_L1 = loadImage("cloud_sprite_L1.png")
    cloud_L2 = loadImage("cloud_sprite_L2.png")
    cloud_M1 = loadImage("cloud_sprite_M1.png")
    cloud_M2 = loadImage("cloud_sprite_M2.png")
    cloud_M3 = loadImage("cloud_sprite_M3.png")
    cloud_S1 = loadImage("cloud_sprite_S1.png")
    cloud_S2 = loadImage("cloud_sprite_S2.png")
    
    face = loadImage("baby_face.png")
 
    #initialize active background variables  
    bg_chunkX, bg_chunkY, bg_chunkIncr, bg_chunkSize, bg_backHeight, bg_backWidth, bg_cornerPointX, bg_cornerPointY, bg_canvasX, bg_canvasY = initialize_image(475, 15000, 100, 5, 0, 0, 0, 0, 666, 475) 
    
    #display active background
    copy(background_active, bg_chunkX, bg_chunkY, bg_chunkSize, bg_backHeight, bg_cornerPointX, bg_cornerPointY, bg_canvasX, bg_canvasY)
    
    #rain
    global rain
    for i in range(500):
        #                x,                      y,                         z                      
        rain.append(Drop(random.randint(1, 666), random.randint(-500, -50), random.randint(0,20)))
    
    
    
#===============================================================================================================================
#===============================================================================================================================
#===============================================================================================================================
    
def draw():
    
    #global active background variables
    global bg_cornerPointX, bg_cornerPointY, bg_canvasX, bg_canvasY
    global bg_backHeight, bg_backWidth, bg_chunkSize, bg_chunkIncr, bg_chunkX, bg_chunkY
    
    #move background
    bg_chunkX, bg_chunkIncr, bg_chunkSize, bg_backWidth = active_image(bg_chunkX, bg_chunkIncr, bg_chunkSize, bg_backWidth) 
                
    #display active background   
    copy(background_active, bg_chunkX, bg_chunkY, bg_chunkSize, bg_backHeight, bg_cornerPointX, bg_cornerPointY, bg_canvasX, bg_canvasY) 
    
    #sun-moon-face
    global S_angleRotate, M_angleRotate
    S_angleRotate, M_angleRotate = sun_moon(200, S_angleRotate, M_angleRotate, bg_chunkX, face)
    
    #display static active
    image(background_static, 0, 100)
        
    #clouds
    global Lx1, Lx2, Mx1, Mx2, Mx3, Sx1 , Sx2
    
    Lx1 = draw_cloud(cloud_L1, Lx1, 95, 1, cloud_L1.width)
    Lx2 = draw_cloud(cloud_L2, Lx2, 110, 1, cloud_L2.width)
    
    Mx1 = draw_cloud(cloud_M1, Mx1, 75, 1, cloud_M1.width)
    Mx2 = draw_cloud(cloud_M2, Mx2, 140, 1, cloud_M2.width)
    Mx3 = draw_cloud(cloud_M3, Mx3, 135, 1, cloud_M3.width)
    
    Sx1 = draw_cloud(cloud_S1, Sx1, 145, 1, cloud_S1.width)
    Sx2 = draw_cloud(cloud_S2, Sx2, 80, 1, cloud_S2.width)
    
    #text
    global total, msg_x
    total, msg_x = display_text(total, msg_x, bg_chunkX)
    
    #music player
    play_music(True, ost_playlist[0])
    
    #rain
    for x in range(0, len(rain)):
        rain[x].fall()
        rain[x].show()

#===============================================================================================================================
#===============================================================================================================================
#===============================================================================================================================
    
def keyPressed():
    if key == "s":
        day_ost.pause()
    print(key)

    
