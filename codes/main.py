import pygame
import os
import math
import sys
import random
import neat
import time
import pickle
import gzip
from neat.population import Population
from neat.reporting import BaseReporter

screen_width = 1920
screen_height = 1080

car_size_x = 60
car_size_y = 60

current_generation = 0

BORDER_COLOR = (255, 255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
game_map = pygame.image.load('./medium_map.png').convert() 
screen.blit(game_map, (0,0))
pygame.display.set_caption('Self Driving Car')

class Car:
    def __init__(self):
        self.sprite = pygame.image.load('./car.png').convert()
        self.sprite = pygame.transform.scale(self.sprite, (car_size_x, car_size_y))
        self.rotated_sprite = self.sprite

        self.speed_set = False

        self.pos = [830, 920] # Starting position
        self.angle = 0
        self.speed = 0
        self.center = [int(self.pos[0]) + car_size_x / 2, int(self.pos[1]) + car_size_y / 2]

        self.radars = [] # Radars
        self.count_radars = 7
        self.radars_for_draw = []

        self.is_alive = True
        self.corners = []
        self.goal = False
        self.distance_data = []

        self.distance = 0
        self.time = 0

    def draw_car(self,screen):
        screen.blit(self.rotated_sprite, self.pos)
        self.draw_radar(screen) # To display radars

    def draw_radar(self,screen):
        for radar in self.radars:
            end_point = radar[0]
            pygame.draw.line(screen,(0,255,0),self.center,end_point,1)
    
    def detect_collion(self,game_map):
        self.is_alive = True
        
        for corner in self.corners:
            if game_map.get_at((int(corner[0]), int(corner[1]))) == BORDER_COLOR:
                self.is_alive = False
                break

    def make_radar(self,game_map,degree): # Here we are going to create those radar that reaches outwards till it either reaches the border (I won't be implementing the condition where it stops when it reaches out too far)
        radius = 0 # Try to make it as small as possible without too much time taken to ensure more accurate measurement of our radar distances
        x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * radius) # x=rcos(theeta)
        y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * radius) # y=rsin(theeta)

        while not game_map.get_at((x,y)) == BORDER_COLOR and radius < 500: # Hyperparameter here (the radius)
            radius += 0.5
            x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * radius)
            y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * radius)

        dist = int(math.dist([x,y], self.center))
        self.radars.append([[x,y],dist])


    def update_car(self, game_map):

        if not self.speed_set:
            self.speed = 20 # Try to build a interactive element to being able to change the speed of the car during the simulation 
            self.speed_set = True

        self.rotated_sprite = self.rotate_image(self.sprite, self.angle)
        self.pos[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        self.pos[1] += math.sin(math.radians(360 - self.angle)) * self.speed

        self.distance += self.speed 
        self.time += 1

        self.center = [int(self.pos[0]) + car_size_x / 2, int(self.pos[1]) + car_size_y / 2]

        length = math.hypot(car_size_x/2,car_size_y/2)
        left_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 30))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 30))) * length]
        right_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 150))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 150))) * length]
        left_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 210))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 210))) * length]
        right_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 330))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 330))) * length]
        self.corners = [left_top, right_top, left_bottom, right_bottom]

        self.detect_collion(game_map)
        self.radars.clear()

        for d in range(-90, 91, 30): # 91 to include 90 degrees in it 
            self.make_radar(game_map,d)

    def get_input_data(self):
        radar = self.radars
        res = [0]*self.count_radars
        for i, r in enumerate(radar):
            res[i] = r[1]

        self.distance_data = res

        return res

    def alive(self):
        return self.is_alive

    def get_reward(self):
        # Rewards would be optimal if the car goes further and also if the distance between respective angles were as similar as possible 
        # This would be an interesting function to keep tweaking 

        # return self.distance # This seems to be very efficient by itself

        return self.distance - 0.2*(abs(self.distance_data[0] - self.distance_data[-1]) + abs(self.distance_data[1] - self.distance_data[-2]) + abs(self.distance_data[2] - self.distance_data[-3]))

    def rotate_image(self,image,angle):
        rectangle = image.get_rect()
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rectangle = rectangle.copy()
        rotated_rectangle.center = rotated_image.get_rect().center
        rotated_image = rotated_image.subsurface(rotated_rectangle).copy()
        return rotated_image

def run_simulation(genomes,config):
    time.sleep(0.5)
    nets = []
    cars = []

    for i, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0
        cars.append(Car())

    clock = pygame.time.Clock()
    generation_font = pygame.font.SysFont("Arial", 30)
    alive_font = pygame.font.SysFont("Arial", 20)
    

    global current_generation
    current_generation += 1

    # Simple Counter To Roughly Limit Time (Not Good Practice)
    counter = 0

    while True:                   
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
 
        for i, car in enumerate(cars):
            output = nets[i].activate(car.get_input_data()) # output would be a list of 4 outputs - left, right, accelerate, break 
            # I wish to make multiple adjustments to the car if possible but we shall see what happens to the car 

            """car.angle += 10 * output[0] 
            car.angle -= 10 * output[1]
            car.speed += output[2]
            if car.speed <= 0:
                car.speed = 2"""

            # What i found when attempting to use deceleration was that the network exploited it's reward function of distance
            # It learned that if it just went in circles and moved at a snail's pace or didn't move at all it would be rewarded 
            """car.speed = car.speed/output[3] if output[3] != 0 else car.speed
            if car.speed <= 0:
                car.speed = 1"""

            choice = output.index(max(output))
            if choice == 0:
                car.angle += 10*output[0] # Left
            elif choice == 1:
                car.angle -= 10*output[1] # Right
            elif choice == 2:
                if(car.speed - 2 >= 12):
                    car.speed -= 2*output[2] # Slow Down
            else:
                car.speed += 2*output[3] # Speed Up

        still_alive = 0
        for i, car in enumerate(cars):
            if car.alive():
                still_alive+=1
                car.update_car(game_map)
                genomes[i][1].fitness += car.get_reward()

        if still_alive == 0:
            break

        counter += 1
        if counter == 30*40: # Stop After About 20 Seconds
            break
    
        screen.blit(game_map, (0,0))
        for car in cars:
            if car.alive():
                car.draw_car(screen)
        
        # Display Info
        text = generation_font.render("Generation: " + str(current_generation), True, (0,0,0))
        text_rect = text.get_rect()
        text_rect.center = (900, 450)
        screen.blit(text, text_rect)

        text = alive_font.render("Still Alive: " + str(still_alive), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (900, 490)
        screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(100)

class Checkpointer(BaseReporter):
    """
    A reporter class that performs checkpointing using `pickle`
    to save and restore populations (and other aspects of the simulation state).
    """

    def __init__(self, generation_interval=100, time_interval_seconds=300,
                 filename_prefix='neat-checkpoint-'):
        """
        Saves the current state (at the end of a generation) every ``generation_interval`` generations or
        ``time_interval_seconds``, whichever happens first.

        :param generation_interval: If not None, maximum number of generations between save intervals
        :type generation_interval: int or None
        :param time_interval_seconds: If not None, maximum number of seconds between checkpoint attempts
        :type time_interval_seconds: float or None
        :param str filename_prefix: Prefix for the filename (the end will be the generation number)
        """
        self.generation_interval = generation_interval
        self.time_interval_seconds = time_interval_seconds
        self.filename_prefix = filename_prefix

        self.current_generation = None
        self.last_generation_checkpoint = -1
        self.last_time_checkpoint = time.time()

    def start_generation(self, generation):
        self.current_generation = generation

    def end_generation(self, config, population, species_set):
        checkpoint_due = False

        if self.time_interval_seconds is not None:
            dt = time.time() - self.last_time_checkpoint
            if dt >= self.time_interval_seconds:
                checkpoint_due = True

        if (checkpoint_due is False) and (self.generation_interval is not None):
            dg = self.current_generation - self.last_generation_checkpoint
            if dg >= self.generation_interval:
                checkpoint_due = True

        if checkpoint_due:
            self.save_checkpoint(config, population, species_set, self.current_generation)
            self.last_generation_checkpoint = self.current_generation
            self.last_time_checkpoint = time.time()

    def save_checkpoint(self, config, population, species_set, generation):
        """ Save the current simulation state. """
        filename = '{0}{1}'.format(self.filename_prefix, generation)
        print("Saving checkpoint to {0}".format(filename))

        with gzip.open(filename, 'w', compresslevel=5) as f:
            data = (generation, config, population, species_set, random.getstate())
            pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)


    @staticmethod
    def restore_checkpoint(filename):
        """Resumes the simulation from a previous saved point."""
        with gzip.open(filename) as f:
            generation, config, population, species_set, rndstate = pickle.load(f)
            random.setstate(rndstate)
            return Population(config, (population, species_set, generation))


if __name__ == "__main__":
    
    # Load Config
    config_path = "./config.txt"
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path)

    # Create Population And Add Reporters
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    
    # Run Simulation For A Maximum of 1000 Generations
    population.run(run_simulation, 1000)
    save = Checkpointer()
    save.save_checkpoint(config,population,population.species, population.generation)
