add_library('minim')
day_ost = None
night_ost = None
music_delay = 1

def setup():
    global day_ost
    global night_ost
    m = Minim(this)
    day_ost = m.loadFile("let_love_win.mp3")
    night_ost = m.loadFile("the_calling.mp3")
    size(400,400)
    day_ost.play()
    
def draw():
    background(0)
    
def setGain(music_delay):
    pass
    
def keyPressed():
    global music_delay
    if keyCode == "UP" and music_delay != 1:
        music_delay += 0.1
    elif keyCode == "DOWN" and music_delay != 0:
        music_delay -= 0.1
    print(music_delay)
