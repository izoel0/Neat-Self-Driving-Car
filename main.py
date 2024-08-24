import neat.nn.feed_forward
import pygame
import neat
import pickle
import time
import os
from game import *

class RaceSim:
    def __init__(self, window, population, track=None, background=None, spawnposition = None, ) -> None:
        self.window = window
        self.population = population
        self.game = RaceGame(self.window, self.population, track,background, spawnposition)
        self.cars = self.game.cars
    
    # Testing the game with keyboard input instead of AI decsision
    def TestGame(self):
        clock = pygame.time.Clock()
        while True:
            # set fps, do exit check: all car crash, window coles
            clock.tick(60)
            if EventQuit(): break
            if self.game.carsAlive == 0: break

            # For car control
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.cars[1].steer(5)
            elif keys[pygame.K_d]:
                self.cars[1].steer(-5)
            else:
                self.cars[1].steer(0)
            # Check if reset button is pressed after a release using a register bool to make sure it only run once
            if keys[pygame.K_t] and register:
                self.cars[1].reset(self.game.carGroup)
                register = False
                self.game.carsAlive += 1
            elif not keys[pygame.K_t]:
                register = True
                
            # display update
            self.game.update()
            pygame.display.update()
        pygame.quit()
    
    # making moves for network in a list and give fitness if gnomes given(training)
    def MoveAI(self, nets, datas, gnomes=None):
        # loop trough all gnomes,networks,cars in population
        for i in range(self.population):
            if self.cars[i].alive:
                if gnomes: gnomes[i][1].fitness += 1 # reward the gnomes for still being alive

                # let the network control the car
                output = nets[i].activate(datas[i])
                decsision = output.index(max(output))
                if decsision == 1:
                    self.cars[i].steer(-5)
                elif decsision == 2:
                    self.cars[i].steer(5)
                else:
                    self.cars[i].steer(0)
    # Simulation where AI get train
    def TrainAI(self, gnomes, config):
        # Creating network for each gnome and putting it in variable nets
        nets = []#list of network
        for _,gnome in gnomes:
            nets.append(neat.nn.FeedForwardNetwork.create(gnome, config))
            gnome.fitness = 0
        frames = 0 #frame for duration control/exit for generation
        while True:
            # add frame, check for exit: window close, no car alive, reach 4000 frame
            # returning if training is force to close ---> stop program or natural(False) === Check in line 130
            frames += 1
            if EventQuit(): return True
            if self.game.carsAlive == 0 or frames == 4000: return False

            # Handle AI movement
            datas = self.game.vision()
            self.MoveAI(nets, datas, gnomes)

            # Game/screen update
            self.game.update()
            pygame.display.update()
    
    # Sim where AI is test
    def TestAI(self, net, Loop=False):
        # frames for time to exit
        frames = 0
        while True:
            # check if window is close
            if EventQuit(): break

            # Ai Movement
            datas = self.game.vision()
            self.MoveAI([net], datas)

            # Stop test when reach 4000 frames
            frames += 1
            if frames == 4000 and not Loop: break
            if self.game.carsAlive == 0: return True

            # game/display update
            self.game.update()
            pygame.display.update()
    
    # Kill the sim if not old car is still being render despite creating new sim
    def KillSim(self):
        for car in self.cars:
            car.alive = False
            car.kill()

# Use canvas to create a track, return track, background, spawn position
def DrawTrack(win):
    # Drawing the Track
    canvas = Canvas(win)
    while True:
        if EventQuit(): break
        canvas.draw()
        pygame.display.update()
    
    background = win.copy()# getting the current track for bg
    track = canvas.GetCanvas()# getting the track without any spawn point since it mess with the colorkey/create alpha/transpparent road that the car do not hit/register as crash

    # picking spawn point
    while True:
        if EventQuit():break
        spawnPosition = canvas.draw((0,255,0))
        if spawnPosition:
            break
    pygame.display.update()
    return track, background ,spawnPosition

# Get a track, background, spawn position from the track pool, background pool, spawn posistion pool based on index pool
def getTrack(index=None):
    # getting index pool
    global indexPool
    # cycling index pool to rotate the track, background, spawn position
    indexPool += 1
    if indexPool > len(trackPool)-1:
        indexPool = 0
    if index: 
        indexPool = index

    return trackPool[indexPool], backgroundPool[indexPool],spawnPool[indexPool]

# Function that get called each generation by line 161
def SimTrainAI(gnomes, config):
    # get track, background, spawn position based on the rotation
    useTrack,background, spawnPosition = getTrack()
    # create new sim with the ammount of population, track background, spawn position
    sim = RaceSim(win, len(gnomes), useTrack,background, spawnPosition)
    force_quit = sim.TrainAI(gnomes, config) # if the window is closed by user will return true
    if force_quit:
        quit()
    sim.Killsim()

# Function to set up the necesary information for training AI
def GoTrainAI(config):
    # getting population
    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-18')# get population from chekpoint 18
    #p = neat.Population(config) #if not comanded then create new generation, make sure you only have line 158 on or 157 on

    # setting up report
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    # write the best gnome after 50 generation or when the requirement in config.txt is met as best.pickle in current directory
    winner = p.run(SimTrainAI, 50)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)

# set up and run test for ai
def GoTestAI(config, Loop=None):
    # get the winner from best.pickle
    with open('best.pickle', "rb") as f:
        winner = pickle.load(f)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    # running the test from each track in track pool
    if Loop == '':
        for i in range(len(trackPool)):
            track, background, spawnPosition = getTrack()
            sim = RaceSim(win, 1, track, background, spawnPosition)
            crash = sim.TestAI(winner_net)
            if crash: print('crash at', i)
            sim.KillSim()
    else:
        track, background, spawnPosition = getTrack(len(trackPool)-1)
        sim = RaceSim(win, 1, track, background, spawnPosition)
        crash = sim.TestAI(winner_net,True)
        if crash: print('crash')
        sim.KillSim()

if __name__ == '__main__':
    # setting up neat
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        config_path)
    
    # getting information on what you wnat to do
    drawing = input('draw?')
    test = input('test?')
    Loop = 'true'

    # initialize variable
    trackPool = [None]
    backgroundPool = [None]
    spawnPool = [None]
    indexPool = 0

    # set display
    width = 1000
    height = 1000
    win = pygame.display.set_mode((width, height))

    # drawing to map pool if you put something in draw prompt
    if drawing:
        poolammount = 1
        if Loop == '':
            poolammount = int(input('how many track you want to draw?'))
        for _ in range(poolammount):
            win.fill((0,0,0))# reset the window =
            # drawing track and putting the right information to the pool
            track,background, spawnPosition = DrawTrack(win)
            backgroundPool.append(background)
            trackPool.append(track)
            spawnPool.append(spawnPosition)
            time.sleep(1) # delay is needed for user to see the final track

    # test the AI if you put something in test prompt
    GoTestAI(config,Loop) if test else GoTrainAI(config)

    # use for you to test the game with keyboard control(A,D)
'''
    sim = RaceSim(win, 2, None, None)
    sim.TestGame()
'''

    