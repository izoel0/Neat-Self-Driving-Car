import pygame
from RaceUtils import *

def EventQuit():
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
    return False

def TrackBG(track,color):
    bg = pygame.surface.Surface((track.get_width(), track.get_height()))
    bg.fill(color)
    bg.blit(track, (0,0))
    return bg

class RaceGame:
    RED_CAR = scale_image(pygame.image.load("imgs/red-car.png"), 0.55)
    trackImg = scale_image(pygame.image.load("imgs/track-border.png"), 1.1)
    TRACK = SpriteTrack(trackImg)
    carGroup = pygame.sprite.Group()

    def __init__(self, window,CarAmmount,track=None, background=None, SpawnPosition=None) -> None:
        self.window = window
        if track: 
            if background:
                self.background = background
            else:
                self.background = window.copy()
            self.TRACK=SpriteTrack(track)
            self.SpawnPosition = SpawnPosition if SpawnPosition else (40, self.background.get_height()-40)
        else:
            self.SpawnPosition = (70,500)
            self.background = TrackBG(self.trackImg, (40,40,40))
        self.cars = self.CreateCar(CarAmmount)
        self.carsAlive = CarAmmount

    def CreateCar(self, Ammount):
        cars = []
        for _ in range(Ammount):
            cars.append(RaceCar(self.SpawnPosition, self.RED_CAR, 5, [self.TRACK], self.carGroup))
        return cars

    def vision(self):
        data = []
        for car in self.cars:
             data.append(car.Vision())
        return data

    def update(self):
        for car in self.cars:
            car.move(2)
            car.refresh()
            if car.collision([self.TRACK]):
                car.alive = False
                car.kill()
                self.carsAlive -= 1
        self.window.blit(self.background, (0,0))
        self.carGroup.draw(self.window)

class Canvas:
    def __init__(self, window) -> None:
        self.window = window
    def draw(self, color=(255,255,255), radius=40):
        if pygame.mouse.get_pressed()[0]:
            mousePos = pygame.mouse.get_pos()
            pygame.draw.circle(self.window, color, mousePos, radius)
            return mousePos
        if pygame.mouse.get_pressed()[2]:
            pygame.draw.circle(self.window, (0,0,0), pygame.mouse.get_pos(), radius)
    def GetCanvas(self) -> pygame.surface.Surface:
        image = self.window.copy()
        image.set_colorkey((255,255,255))
        return image
    
if __name__ == '__main__':
    win = pygame.display.set_mode((600,600))
    canvas = Canvas(win)
    while True:
        if EventQuit():break

        canvas.draw()
        pygame.display.update()
    track = canvas.GetCanvas()
    while True:
        if EventQuit():break
        spawn = canvas.draw((0,255,0))
        if spawn:
            break

    pygame.display.update()

    race = RaceGame(win, 2, track, spawn)
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        if EventQuit(): break
        if race.carsAlive == 0: break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            race.cars[1].steer(5)
        elif keys[pygame.K_d]:
            race.cars[1].steer(-5)
        else:
            race.cars[1].steer(0)
        if keys[pygame.K_t] and register:
            race.cars[1].reset(race.carGroup)
            register = False
            race.carsAlive += 1
        elif not keys[pygame.K_t]:
            register = True
            
        
        race.update()
        pygame.display.update()