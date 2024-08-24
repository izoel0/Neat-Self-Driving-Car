import pygame
from pygame import Vector2
import math

def GetWindow(image, fill=False, bg_color = (40,40,40)):
    window = pygame.display.set_mode((image.get_width(), image.get_height()))
    if fill: window.fill(bg_color)
    window.blit(image, (0,0))
    pygame.display.update()
    return window

def getDestination(origin, angle, length) ->tuple:
    rad = math.radians(angle)
    horizontal = length * math.sin(rad)
    vertical = length * math.cos(rad)
    return (origin[0]-horizontal, origin[1]-vertical)

def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)

class SpriteTrack(pygame.sprite.Sprite):
    def __init__(self,image, *groups) -> None:
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect(topleft = (0,0))
        self.mask = pygame.mask.from_surface(self.image)

class RaceCar(pygame.sprite.Sprite):
    def __init__(self, spawnPosition, image, maxSteeringAngle=5,collisionGroup = [] ,*groups) -> None:
        super().__init__(*groups)
        self.spawnPosition = spawnPosition
        self.x, self.y = self.spawnPosition
        self.angle = 0

        self.Original = image
        self.image = self.Original.copy()
        self.rect = self.image.get_rect(center=self.spawnPosition)
        self.mask = pygame.mask.from_surface(self.image)

        self.steeringAngle = 0
        self.maxSteeringAngle = maxSteeringAngle
        self.alive = True

        self.rays = None
        if collisionGroup: self.CreateRays(collisionGroup)
    def CreateRays(self, collisionGroup):
        self.rays = [Ray(self, 45, 100, collisionGroup),
                     Ray(self, 90, 100, collisionGroup),
                     Ray(self, 270, 100, collisionGroup),
                     Ray(self, 315, 100, collisionGroup),]

    def rotate(self, rotate):
        self.angle += rotate
        if self.angle > 360:
            self.angle -= 360
        elif self.angle < 0:
            self.angle += 360
        self.image = pygame.transform.rotate(self.Original, self.angle)

    def steer(self, angle):
        self.steeringAngle = max(-self.maxSteeringAngle, min(self.maxSteeringAngle, angle))

    def move(self, speed):
        if self.steeringAngle != 0:
            self.rotate((speed/self.steeringAngle)*speed*3)
        self.x, self.y = getDestination((self.x, self.y), self.angle, speed)
    
    def collision(self, collisionGroup=[], checkAlive=True):
        if checkAlive and self.alive or not checkAlive:
            if pygame.sprite.spritecollideany(self, collisionGroup, pygame.sprite.collide_mask):
                return True
            else:
                return False
    
    def Vision(self, checkAlive=True):
        if checkAlive and self.alive or not checkAlive:
            vision = []
            for ray in self.rays:
                vision.append(ray.update())
            return vision

    def refresh(self):
        if self.alive:
            self.rect = self.image.get_rect(center=(self.x, self.y))
            self.mask = pygame.mask.from_surface(self.image)

    def reset(self, spriteGroup=None):
        self.steeringAngle = 0
        self.rotate(-self.angle)
        self.x, self.y = self.spawnPosition
        if spriteGroup: self.add(spriteGroup)
        self.alive = True


class Ray:
    def __init__(self, car:RaceCar, angle, length, collision) -> None:
        self.car = car
        self.angle = angle
        self.length = length
        self.collision = collision
    def update(self):
        origin = Vector2(self.car.x, self.car.y)

        dest = getDestination(origin, self.car.angle+self.angle, self.length)

        currentpos = origin
        heading = dest - currentpos
        direction = heading.normalize()
        for _ in range(int(heading.length())):
            currentpos += direction
            for sprite in self.collision:
                try:
                    if sprite.mask.get_at(currentpos):
                        leng = (currentpos-(self.car.x,self.car.y))
                        return math.hypot(leng[0],leng[1])
                except IndexError:
                    return self.length
        return self.length