class Ball:
    
    def __init__(self, canvas, x, y, r, xVelocity, yVelocity, friction, color):
        self.canvas = canvas
        self.image = self.create_circle(x, y, r, canvas, color)
        self.vx = xVelocity
        self.vy = yVelocity
        self.friction = friction
    
    def create_circle(self, x, y, r, canvas, color): #center coordinates, radius
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        return canvas.create_oval(x0, y0, x1, y1, fill=color)
    
    def move(self, dt):
        coordinates = self.canvas.coords(self.image)

        if(coordinates[2] >= (self.canvas.winfo_width()) or coordinates[0] < 0):
            self.vx = -self.vx
        if(coordinates[3] >= (self.canvas.winfo_height()) or coordinates[1] < 0):
            self.vy = -self.vy

        self.vx *= (1 - self.friction * dt)
        self.vy *= (1 - self.friction * dt)

        if abs(self.vx) < 1: 
            self.vx = 0
        if abs(self.vy) < 1: 
            self.vy = 0

        dx = self.vx * dt
        dy = self.vy * dt

        self.canvas.move(self.image, dx, dy)