# pygame fluid sim
import pygame
from random import randint

class Droplet():
    count = 0
    def __init__(self, screen, radius=15, GRAVITY=200, COR=0.8, colour="blue"):
        self.screen = screen
        self.HEIGHT = screen.get_height()
        self.WIDTH = screen.get_width()
        self.radius = radius
        self.drop_pos = pygame.Vector2(self.WIDTH / 2, self.radius)
        self.vy = 0
        self.vx = randint(-500, 500)
        self.dt = 0
        self.GRAVITY = GRAVITY
        self.COR = COR  # Coefficient of Restitution
        self.start = False
        self.colour = colour
        Droplet.count += 1
        
    def draw(self):
        # draws the circle to the screen
        self.circle = pygame.draw.circle(self.screen, self.colour, self.drop_pos, self.radius)

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

            if self.drop_pos.y <= self.radius:
                self.drop_pos.y = self.radius
                self.vy = -self.vy * self.COR
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
                self.vx = randint(-500, 500)

    def velocity_controlled_colour(self):
        x = abs(self.vy) if abs(self.vy) <= 255 else 255
        y = 255 - x 
        self.colour = (x, y, 0)

    def random_colour(self):
        self.colour = (randint(0, 255), randint(0, 255), randint(0, 255))
        
    def handle_collisions(self, drops):
        for drop in drops:
            if drop is self:
                continue  # Skip self-collision

            distance = self.drop_pos.distance_to(drop.drop_pos)
            if distance < self.radius + drop.radius:
                # Avoid division by zero if droplets exactly overlap
                # normalize the vector to make calculations based on direction instead of magnitude 
                # method was found on stack overflow, initially the smoothness of the collisions was 
                # much worse before normalizing 
                if distance == 0:
                    normal = pygame.Vector2(1, 0)
                else:
                    normal = (self.drop_pos - drop.drop_pos) / distance

                # Calculate how much the droplets overlap and separate them evenly
                overlap = (self.radius + drop.radius - distance) * 0.5
                self.drop_pos += normal * overlap
                drop.drop_pos -= normal * overlap

                # Get the normal components of both droplets' velocities
                v_self_normal = self.vx * normal.x + self.vy * normal.y
                v_drop_normal = drop.vx * normal.x + drop.vy * normal.y

                # Damping factor for energy loss during collision
                damping = 0.5
                self_delta = (v_drop_normal - v_self_normal) * damping
                drop_delta = (v_self_normal - v_drop_normal) * damping

                # Adjust velocities along the collision normal
                self.vx += self_delta * normal.x
                self.vy += self_delta * normal.y
                drop.vx += drop_delta * normal.x
                drop.vy += drop_delta * normal.y
                
class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.WIDTH, self.HEIGHT = (1280, 720)
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.running = True
        self.drops = []

    def add_droplets(self, mouse_pos):
        x, y = mouse_pos
        droplet = Droplet(self.screen, GRAVITY=250)
        droplet.drop_pos.x = x
        droplet.drop_pos.y = y
        droplet.random_colour()
        self.drops.append(droplet)
    
    def events(self): # keypress and event logic
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self.add_droplets(mouse_pos)
        if keys[pygame.K_BACKSPACE]:
            self.drops = []

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            self.screen.fill("purple")
            self.events() # bundled the event logic into a method for press and event types

            for drop in self.drops:
                drop.draw()
                drop.set_dt(dt)
                drop.update()
                drop.handle_collisions(self.drops)
            
            pygame.display.flip()
        pygame.quit()


if __name__ == "__main__":
    Game().run()

