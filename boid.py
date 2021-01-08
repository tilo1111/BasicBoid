import pygame
import random
import math

max_v = 2
fov = 100
min_dist = 20
pygame.init()
WIDTH, HEIGHT = pygame.display.Info().current_w - 100, pygame.display.Info().current_h - 100
pygame.quit()

class Boid(pygame.sprite.DirtySprite):
    def __init__(self, x, y, max_v, fov, image):

        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.Vx = random.randint(-10, 10) / max_v
        self.Vy = random.randint(-10, 10) / max_v

        self.fov = fov
        self.max_v = max_v

    def dist(self, neighbour):
        dist_x = self.rect.x - neighbour.rect.x
        dist_y = self.rect.y - neighbour.rect.y
        return math.sqrt(dist_x * dist_x + dist_y * dist_y)

    def alignment(self, boid_list):
        if len(boid_list) < 1:
            return

        avg_x = 0
        avg_y = 0

        for boid in boid_list:
            if boid.rect.x == self.rect.x and boid.rect.y == self.rect.y:
                continue

            avg_x += boid.Vx
            avg_y += boid.Vy

        avg_x /= len(boid_list)
        avg_y /= len(boid_list)

        self.Vx += 0.1*(avg_x - self.Vx)
        self.Vy += 0.1*(avg_x - self.Vy)

    def cohesion(self, boid_list):
        if len(boid_list) < 1:
            return

        avg_x = 0
        avg_y = 0
        
        for boid in boid_list:
            avg_x += boid.rect.x
            avg_y += boid.rect.y

        avg_x /= len(boid_list)
        avg_y /= len(boid_list)

        self.Vx += 0.01*(avg_x - self.rect.x)
        self.Vy += 0.01*(avg_y - self.rect.y)

    def separation(self, boid_list, min_dist):
        if len(boid_list) < 1:
            return

        dist_x = 0
        dist_y = 0
        colisions = 0

        for boid in boid_list:
            dist = self.dist(boid)

            if dist < min_dist:
                colisions += 1
                xdiff = (self.rect.x - boid.rect.x)
                ydiff = (self.rect.y - boid.rect.y)

                if xdiff >= 0:
                    xdiff = math.sqrt(min_dist) - xdiff
                elif xdiff < 0:
                    xdiff = -math.sqrt(min_dist) - xdiff

                if ydiff >= 0:
                    ydiff = math.sqrt(min_dist) - ydiff
                elif ydiff < 0:
                    ydiff = -math.sqrt(min_dist) - ydiff

                dist_x += xdiff
                dist_y += ydiff

        if colisions == 0:
            return

        self.Vx -= 0.7*(dist_x - self.Vx)
        self.Vy -= 0.7*(dist_y - self.Vy)

    def update(self):
        self.dirty = 1
            
        if self.rect.x < 0 and self.Vx < 0:
            self.rect.x = WIDTH
        if self.rect.x > WIDTH and self.Vx > 0:
            self.rect.x = 0
        if self.rect.y < 0 and self.Vy < 0:
            self.rect.y = HEIGHT
        if self.rect.y > HEIGHT and self.Vy > 0:
            self.rect.y = 0

        if abs(self.Vx) > self.max_v or abs(self.Vy) > self.max_v:
            tmp = self.max_v / max(abs(self.Vx), abs(self.Vy))
            self.Vx *= tmp
            self.Vy *= tmp
            
        if self.Vx==0 and self.Vy==0:
            self.Vx += random.randint(-10,10) / 10
            self.Vy += random.randint(-10,10) / 10

        self.rect.x += self.Vx
        self.rect.y += self.Vy

