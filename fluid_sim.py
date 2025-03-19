# pygame fluid sim

# Example file showing a circle moving on screen
import pygame
from random import randint


class Droplet():
    count = 0
    def __init__(self, screen, radius=40, GRAVITY=200, COR=0.8):
        self.screen = screen
        self.HEIGHT = screen.get_height()
        self.WIDTH = screen.get_width()
        self.radius = radius
        self.drop_pos = pygame.Vector2(self.WIDTH / 2, self.radius)
        self.vy = 0
        self.vx = 200
        self.dt = 0
        self.GRAVITY = GRAVITY
        self.COR = COR  # Coefficient of Restitution
        self.init_placement()
        self.start = False
        Droplet.count += 1
        
        
    def draw(self):
        # draws the circle to the screen
        self.circle = pygame.draw.circle(self.screen, self.colour(), self.drop_pos, self.radius)

    def set_dt(self, dt):
        # sets the time delta everyframe
        self.dt = dt

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.start = True 
        if self.start:
            # Collision with ground
            if self.drop_pos.y >= self.HEIGHT - self.radius:
                self.drop_pos.y = self.HEIGHT - self.radius  # Prevent sinking
                self.vy = -self.vy * self.COR  # Apply COR to Y velocity
                self.vx *= 0.95  # Simulate friction on the ground

            # Collision with right wall
            if self.drop_pos.x >= self.WIDTH - self.radius:
                self.drop_pos.x = self.WIDTH - self.radius  # Prevent going off-screen
                self.vx = -self.vx * self.COR  # Apply COR to X velocity

            # Collision with left wall
            if self.drop_pos.x <= self.radius:
                self.drop_pos.x = self.radius  # Prevent going off-screen
                self.vx = -self.vx * self.COR  # Apply COR to X velocity

            # Apply gravity
            self.vy += self.GRAVITY * self.dt
            self.drop_pos.y += self.vy * self.dt

            # Apply horizontal motion
            self.drop_pos.x += self.vx * self.dt

            # stop motion when velocity becomes negligable
            if abs(self.vy) <= 0.5:
                self.vy = 0
            if abs(self.vx) <= 0.5:
                self.vx = 0

            # Player input

            if keys[pygame.K_SPACE]:
                self.vy = -200 

    def init_placement(self):
        self.drop_pos.x += ((3 * self.radius * self.count) - 1)

    def colour(self):
        x = abs(self.vy) if abs(self.vy) <= 255 else 255
        y = 255 - x 
        return (x, y, 0)
    
    def handle_collisions(self, drops):
        for drop in drops:
            dist = self.drop_pos.distance_to(drop.drop_pos)
            if dist < self.radius + drop.radius and drop != self:
                overlap = -(dist - self.radius - drop.radius) * 0.5
                self.drop_pos += overlap * (self.drop_pos - drop.drop_pos).normalize()
                drop.drop_pos -= overlap * (self.drop_pos - drop.drop_pos).normalize()
                self.vy = -self.vy * 0.5
                self.vx = -self.vx * 0.5
                
    

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.WIDTH, self.HEIGHT = (1280, 720)
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.running = True
        self.drops = []
        self.drop_count()

    def drop_count(self):
        for i in range(5):
            self.drops.append(Droplet(self.screen, GRAVITY=100*(i + 1)))


    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.screen.fill("purple")

            for i in range(len(self.drops)):
                self.drops[i].draw()
                self.drops[i].set_dt(dt)
                self.drops[i].update()
                self.drops[i].handle_collisions(self.drops)
            
                
            
            # flip() the display to put your work on screen
            pygame.display.flip()

            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            

        pygame.quit()


if __name__ == "__main__":
    Game().run()

