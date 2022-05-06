class Drop():
    x = width/2
    y = 0
    yspeed = 1
    
    def __init__(self, x, y, yspeed):
        self.x = x
        self.y = y
        self.yspeed = yspeed
        
        def fall(self):
            y = y + yspeed
            
        def show(self):
            stroke(225)
            strokeWeight(1)
            line(x, y, x, y + 10)
