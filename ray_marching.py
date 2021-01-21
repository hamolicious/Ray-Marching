
import pygame
from vector_class import Vector3D as Vec
from math import tan
from objects import Cube
from settings import Settings
from time import time
from threading import enumerate
from random import randint

class Ray:
    def __init__(self, pos=(), heading=()):
        x, y, z = pos
        self.pos = Vec(x, y, z)

        x, y, z = heading
        self.heading = Vec(x, y, z)
        self.heading.normalise()
    
    def step(self, distance=1):
        self.pos.add(self.heading * distance)

class Pixel:
    def __init__(self, image_pos, image, envir):
        self.envir = envir

        self.image_pos = image_pos
        self.image = image

        x, y = image_pos
        view_point = Vec(Settings.get('render_image_size')[0]/2, Settings.get('render_image_size')[1]/2, -envir.focal_length)
        ray_pos = Vec(x, y, 0)
        heading = ray_pos - view_point
        self.colour_ray = Ray(pos=(x, y, 0), heading=(heading.x, heading.y, heading.z))
        self.light_rays = []

        self.colour = [0, 0, 0]
        self.iters = 0

    def add_to_colour(self, colour):
        r, g, b = colour

        self.colour[0] += r
        self.colour[1] += g
        self.colour[2] += b

        self.iters += 1

    def set_colour(self):
        for i in range(3):
            if self.iters > 0:
                self.colour[i] /= self.iters

            if self.colour[i] > 255:
                self.colour[i] = 255

        self.image.set_at(self.image_pos, self.colour)

    def distance_estimator(self, from_pos, samples=100):
        # return 1

        safe_distance = 2
        while True:
            collided = False
            for obj in self.envir.objects:
                if obj.pos.dist(from_pos) < safe_distance**2:
                    collided = True
                
            if not collided:
                safe_distance += 1
            else:
                return safe_distance-1
            
            samples -= 1

            if samples <= 0:
                return safe_distance

    def render(self):
        done = False

        while not done:
            if 'Main' not in str(list(enumerate())) : quit()

            safe_distance = self.distance_estimator(self.colour_ray.pos) # get the minimum safe distance
            self.colour_ray.step(safe_distance) # march that distance

            x, y = self.image_pos
            if self.colour_ray.pos.dist(x, y, 0) > Settings.get('render_distance') : done = True # if out of max render distance stop
            if not self.envir.bounding_box.collide_point(self.colour_ray.pos): # if outside bounding box use sky colour
                r, g, b = Settings.get('sky_colour')
                r *= Settings.get('light_strength') ; g *= Settings.get('light_strength') ; b *= Settings.get('light_strength')

                self.add_to_colour([r, g, b])

                done = True

            for obj in self.envir.objects: # check for collisions
                if obj.collide_point(self.colour_ray):
                    self.add_to_colour(obj.colour)

                    done = True
                    break

        self.set_colour()

class Environment:
    def __init__(self):
        self.rendering_surface = pygame.Surface(Settings.get('render_image_size'))
    
        self.bounding_box = Cube(pos=(Settings.get('render_image_size')[0]/2, Settings.get('render_image_size')[1]/2, Settings.get('render_distance')/2), size=(Settings.get('render_image_size')[0], Settings.get('render_image_size')[1], Settings.get('render_distance')))

        self.objects = []
    
        self.FOV = Settings.get('FOV')
        self.focal_length = (0.5 * Settings.get('render_image_size')[0]) * tan(self.FOV / 2)

        self.completion = 0
        self.end = 0

        self.rendering = False
        self.start_time = 0
        self.end_time = 0
        self.elapsed_time = 0

    def calculate_completion(self):
        if self.end == 0 : return 0
        return round((abs(self.end - self.completion) / self.end) * 100, 3)

    def render(self):
        self.start_time = time()
        self.rendering = True

        self.FOV = Settings.get('FOV')
        self.focal_length = (0.5 * Settings.get('render_image_size')[0]) * tan(self.FOV / 2)

        width, height = Settings.get('render_image_size')
        self.rendering_surface = pygame.Surface(Settings.get('render_image_size'))

        self.completion = 0
        self.end = width * height

        positions = []
        for i in range(height):
            for j in range(width):
                positions.append((j, i))

        positions.sort(key=lambda elem : randint(0, 1000))
        for j, i in positions:
                pixel = Pixel(image_pos=(j, i), image=self.rendering_surface, envir=self)
                pixel.render()

                self.completion += 1

        self.end_time = time()
        self.elapsed_time = round(self.end_time - self.start_time, 3)
        self.rendering = False
        quit()












