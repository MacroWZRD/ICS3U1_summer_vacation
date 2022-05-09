#add/import essential libraries
add_library('minim')
import random

#initialize variables
day_ost = None
night_ost = None
ultimate_ost = None
ost_playlist = []
song_num = 0
st = False

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

#draw a cloud taking in a unique image, xy coord, increment, and gap between each loop
def draw_cloud(c, x, y, Incr, gap):
    image(c, x, y)
    x -= Incr
    #reset the cloud to be off the screen
    if x + 150 < 0:
        x = width
    return x
    
#===============================================================================================================================
#===============================================================================================================================
#===============================================================================================================================

#initiate a class for rain drops
class Drop():
    
    #the object attributes
    def __init__(self, x, y, z, ):
        self.x = x
        self.y = y
        self.z = z
        self.yspeed = map(z, 0, 20, 4, 10)
        self._length_ = map(z, 0, 20, 10, 15)
        self.thick = map(z, 0, 20, 0.02, 0.1)
     
    #fall function for rain drop
    def fall(self):
        #add to the y speed to mimic gravity
        self.y += self.yspeed
        self.yspeed += 0.05
        
        #reset the raindrop to the top of the screen once it passed the bottom of the screen
        if self.y > height:
            self.y = random.randint(-200, -100)
            self.yspeed = map(self.z, 0, 20, 4, 10)

    #draw the rain drop on the screen
    def show(self):
        #randomize rain color and thickness
        stroke(random.randint(200, 225),random.randint(200, 225),random.randint(200, 225))
        strokeWeight(self.thick)
        line(self.x, self.y, self.x, self.y + self._length_)   

#===============================================================================================================================
#===============================================================================================================================
#===============================================================================================================================    
  
#function to draw and move sun and moon        
def sun_moon(x, S_AR, M_AR, check, f):
    #setup the sun/moon object size and colors
    noStroke()
    fill(252, 229, 112)
    f.resize(65, 65)
    
    #change to a higher layer (creates a new canvas separate from the original canvas)
    pushMatrix()
    #define rotation point and rotate objects according to the degrees specified)
    translate(333, 300)
    rotate(radians(S_AR))
    ellipse(x, 0, 70, 70)
    tint(255, 40)
    image(f, x - 32.5, -32.5)
    #change back to the original canvas
    popMatrix()
    
    # increase the sun rotation angle 
    S_AR += 0.12075
    
    #set color for the moon
    fill(254, 252, 215)
    
    #change to a higher layer (creates a new canvas separate from the original canvas)
    pushMatrix()
    #define rotation point and rotate objects according to the degrees specified)
    translate(333, 300)
    rotate(radians(M_AR))
    ellipse(x, 0, 70, 70)
    tint(255, 40)
    image(f, x - 32.5, -32.5)
    #change back to the original canvas
    popMatrix()
    
    #reset transparency
    tint(255)
    
    # increase the sun rotation angle 
    M_AR += 0.12075
    
    # reset the sun and moon rotation angle after one day cycle
    if check == 0:
        S_AR = 270
        M_AR = 90
        
    return S_AR, M_AR 
    
#===============================================================================================================================
#===============================================================================================================================
#===============================================================================================================================

#draw text moving across the screen`
def display_text(days, x, check):
    
    #check for every new day cycle
    if check == 0:
        days += 1
    
    #check if 3 day cycles have passed
    if days == 2:
        #draw and move text
        text('"You will never be able to love anybody else until you love yourself." - Lelouch Lamperouge (Code Geass)', x, 50)
        x -= 0.5
        
    #check if 3 day cycle has passed
    elif days > 2:
        #reset all values
        x = 675
        days = 0
        
    return days, x

#===============================================================================================================================
#===============================================================================================================================
#===============================================================================================================================

#music player system
def play_music(action, song):
    #globalize and set required variables
    global song_num
    active = song
    #set infinite loop; song will rewind and begin playing when song ends
    if active.isPlaying() == False and active.length() - active.position() <= 34000:
        active.rewind()
        active.play()
    
    #switch to other songs in the 3 song playlist
    if action == "change":
        #reset the song selector to zero to prevent out of index error
        if song_num == 2:
            play_music("stop", ost_playlist[song_num]) 
            song_num = 0
        #increment the song selector to pisck the next song in the playlist array
        else:
            play_music("stop", ost_playlist[song_num]) 
            song_num += 1
        play_music("play", ost_playlist[song_num])
     
    #play the song
    if action == "play":
        active.play()

    #pause the song
    if action == "pause":
        active.pause()
        
    #rewind the song
    if action == "rewind":
        active.rewind()

    #stop the song
    if action == "stop":
        active.rewind()
        active.pause()
      
    #do nothing
    if action == None:
        pass

#===============================================================================================================================
#===============================================================================================================================
#===============================================================================================================================

#create button class
class button():
    
    #the object attributes
    def __init__(self, img, action, x, y, w, h, state):
        self.img = img
        self.action = action
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.state = state
    
    #display original buttons: no tint 
    def show(self):
        tint(255)
        image(self.img, self.x, self.y)
     
    #detect mouse hover/mouse click
    def clicked(self):
        if (mouseX > self.x and mouseY > self.y) and (mouseX < self.x + self.w and mouseY < self.y + self.h):
            #tint the color
            tint(200)
            image(self.img, self.x, self.y)
            #check for different previous button clicks/state and returns "action"
            if mousePressed == True and self.state == False:
                return self.action
            
        return None
    
#===============================================================================================================================
#===============================================================================================================================
#===============================================================================================================================

def setup():
    #global sound and background assets
    global day_ost, night_ost, ultimate_ost, ost_playlist, song_num
    global background_static, background_active
    global cloud_L1, cloud_L2, cloud_M1, cloud_M2, cloud_M3, cloud_S1, cloud_S2
    global face, sun, moon, angleRotate
    global mPlay, mPause, mBackward, mForward
    
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
    day_ost.play()
    
    #global active background variables
    global bg_cornerPointX, bg_cornerPointY, bg_canvasX, bg_canvasY
    global bg_backHeight, bg_backWidth, bg_chunkSize, bg_chunkIncr, bg_chunkX, bg_chunkY
    
    #load images into variables
    background_static = loadImage("firewatch.png")
    background_active = loadImage("day_night.png")
    
    #load cloud images
    cloud_L1 = loadImage("cloud_sprite_L1.png")
    cloud_L2 = loadImage("cloud_sprite_L2.png")
    cloud_M1 = loadImage("cloud_sprite_M1.png")
    cloud_M2 = loadImage("cloud_sprite_M2.png")
    cloud_M3 = loadImage("cloud_sprite_M3.png")
    cloud_S1 = loadImage("cloud_sprite_S1.png")
    cloud_S2 = loadImage("cloud_sprite_S2.png")
    
    #load face images
    face = loadImage("baby_face.png")
 
    #initialize active background variables  
    bg_chunkX, bg_chunkY, bg_chunkIncr, bg_chunkSize, bg_backHeight, bg_backWidth, bg_cornerPointX, bg_cornerPointY, bg_canvasX, bg_canvasY = initialize_image(475, 15000, 100, 5, 0, 0, 0, 0, 666, 475) 
    
    #display active background
    copy(background_active, bg_chunkX, bg_chunkY, bg_chunkSize, bg_backHeight, bg_cornerPointX, bg_cornerPointY, bg_canvasX, bg_canvasY)
    
    #audio player icons
    mPlay = loadImage("play.png")
    mPlay.resize(40,40)
    mPause = loadImage("pause.png")
    mPause.resize(40,40)
    mBackward = loadImage("backward.png")
    mBackward.resize(48,30)
    mForward = loadImage("forward.png")
    mForward.resize(48,30)
    
    #rain
    global rain
    #create 500 rain drops
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
    p1 = 0
    pa = 0
    bw = 0
    fw = 0
    global st
    #switch between "pause" and "play" depending on if song is playing
    if ost_playlist[song_num].isPlaying():
        pa = button(mPause, "pause", 313, 400, mPause.width, mPause.height, st)
        pa.show()
        play_music(pa.clicked(), ost_playlist[song_num])
    else:
        pl = button(mPlay, "play", 313, 400, mPlay.width, mPlay.height, st)
        pl.show()
        play_music(pl.clicked(), ost_playlist[song_num])    
    
    bw = button(mBackward, "rewind", 253, 405, mPause.width, mPause.height, st)
    bw.show()
    play_music(bw.clicked(), ost_playlist[song_num])

    fw = button(mForward, "change", 368, 405, mPlay.width, mPlay.height, st)
    fw.show()
    play_music(fw.clicked(), ost_playlist[song_num])   
    
    st = mousePressed
    
    #rain
    for x in range(0, len(rain)):
        rain[x].fall()
        rain[x].show()

#===============================================================================================================================
#===============================================================================================================================
#===============================================================================================================================
   
#detects key inputs
def keyPressed():
    global song_num
    if key == "c":
        play_music("change", ost_playlist[song_num])
            
    if key == "s":
        play_music("pause", ost_playlist[song_num])
        
    if key == "p":
        play_music("play", ost_playlist[song_num])
        
    if key == "r":
        play_music("rewind", ost_playlist[song_num])
        
    print(key)

    
