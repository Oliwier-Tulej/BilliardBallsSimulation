import math

class Ball:
    
    def __init__(self, canvas, x, y, r, xVelocity, yVelocity, friction, color):
        self.canvas = canvas
        self.r = r
        self.image = self.create_circle(x, y, r, canvas, color)
        self.vx = xVelocity
        self.vy = yVelocity
        self.friction = friction
        self.color = color
        self.vector_line = None
        self.speed_label = None
        self.show_vector = True
        self.show_speed = True
    
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

        if(self.speed() > 0):
            self.vx *= (1 - self.friction * dt)
            self.vy *= (1 - self.friction * dt)

        if abs(self.vx) < 5: 
            self.vx = 0
        if abs(self.vy) < 5: 
            self.vy = 0

        dx = self.vx * dt
        dy = self.vy * dt

        self.canvas.move(self.image, dx, dy)

        self.drawVelocityVector()
        self.updateSpeedLabel()
    
    def checkCollision(self, other):
        x0, y0 = self.center()
        x1, y1 = other.center()

        dx = x1 - x0
        dy = y1 - y0

        distance = math.sqrt(dx*dx + dy*dy)

        #if no collision end function
        if ((distance > (self.r + other.r)) or (distance == 0)):
            return
        
        #normal vector
        nx = dx / distance
        ny = dy / distance

        #tangential vecctor
        tx = -ny
        ty = nx

        v1n = (self.vx * nx)+(self.vy * ny) #normal vector speed
        v1t = (self.vx * tx)+(self.vy * ty) #tangential vector speed
        v2n = (other.vx * nx)+(other.vy * ny) #normal vector speed
        v2t = (other.vx * tx)+(other.vy * ty) #tangential vector speed

        #elastic collision
        m = 0.16
        v1n_prime = (v1n * (m - m) + 2 * m * v2n) / (m + m)
        v2n_prime = (v2n * (m - m) + 2 * m * v1n) / (m + m)
        
        #coverting to vector
        self.vx = v1n_prime * nx + v1t * tx
        self.vy = v1n_prime * ny + v1t * ty
        other.vx = v2n_prime * nx + v2t * tx
        other.vy = v2n_prime * ny + v2t * ty

        #separating
        overlap = self.r + other.r - distance
        if overlap > 0:
            self.canvas.move(self.image, -nx * overlap * 0.6, -ny * overlap * 0.6)
            self.canvas.move(other.image, nx * overlap * 0.6, ny * overlap * 0.6)

    def center(self):
        coordinates = self.canvas.coords(self.image)
        return (coordinates[2]+coordinates[0])/2, (coordinates[3]+coordinates[1])/2
    
    def speed(self):
        return math.sqrt(self.vx*self.vx + self.vy*self.vy)
    
    def drawVelocityVector(self, scale=0.2, color="black"):
        #remove previous if exists
        if(self.vector_line):
            self.canvas.delete(self.vector_line)
        
        #only draw if moving
        if(abs(self.vx) > 0 or abs(self.vy) > 0):
            cx, cy = self.center()
            end_x = cx + self.vx * scale
            end_y = cy + self.vy * scale
            
            min_length = 5
            vector_length = math.sqrt((end_x - cx)*(end_x - cx) + (end_y - cy)*(end_y - cy))
            if((vector_length < min_length) and (vector_length > 0)):
                    scale_factor = min_length / vector_length
                    end_x = cx + self.vx * scale * scale_factor
                    end_y = cy + self.vy * scale * scale_factor
            
            self.vector_line = self.canvas.create_line(
                cx, cy, end_x, end_y, 
                arrow="last", fill=color, width=2, arrowshape=(8, 10, 5)
            )

    def updateSpeedLabel(self):
        #remove previous if exists
        if self.speed_label:
            self.canvas.delete(self.speed_label)
        
        cx, cy = self.center()
        speed_value = self.speed()
        if speed_value > 0:
            self.speed_label = self.canvas.create_text(
                cx, cy - self.r - 10,
                text=f"{speed_value:.0f}",
                fill="yellow" if self.color == "black" else "black",
                font=("Arial", 10, "bold")
            )
    
    def setVelocity(self, vx, vy):
        self.vx = vx
        self.vy = vy
