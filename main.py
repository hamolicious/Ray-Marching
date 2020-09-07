from os import system ; system('cls')
import pygame
from time import time
from objects import Sphere, objects_to_add
from ray_marching import Environment
from time import time, gmtime
from random import randint
from threading import Thread
from settings import Settings
import pygame_widgets

#region pygame init
Settings.load()

pygame.init()
pygame.font.init()
size = (1000, 600)
screen = pygame.display.set_mode(size)
screen.fill([255, 255, 255])
pygame.display.set_icon(screen)
clock, fps = pygame.time.Clock(), 0

font = pygame.font.SysFont('ariel', 30)
envir = Environment()
envir.objects = objects_to_add

delta_time = 0 ; frame_start_time = 0
#endregion

#region other

def epoh_to_str(epoh):
    if epoh < 60:
        return f'{epoh} seconds'
    else:
        full_time = gmtime(epoh)
        seconds, minutes, hours = full_time.tm_sec, full_time.tm_min, full_time.tm_hour

        return f'{hours:02}:{minutes:02}:{seconds:02}'

#endregion

#region actions

def render():
    thread = Thread(target=envir.render)
    thread.start()

#endregion

#region ui

class UI:
    events = []
    elements = []

    def update_events(events):
        UI.events = events

    def draw():
        for elem in UI.elements:
            elem.listen(UI.events)
            elem.draw()

def make_button(x, y, w, h, text, onClick):
    UI.elements.append(
        pygame_widgets.Button(
            screen, x, y, w, h,
            onClick=onClick,
            text=text
        )
    )

make_button(650, 70, 300, 50, 'Render Image', render)

#endregion

#region auto drawing

def draw_loading_bar(x, y, w, h, completion):
    pygame.draw.rect(screen, [0, 255, 0], (x, y, w, h), 0)

    completion /= 100
    pygame.draw.rect(screen, [255, 0, 0], (x + w, y, -int(w * completion)+1, h), 0)

def draw_label(x, y, text):
    screen.blit(
        font.render(text, True, [255, 255, 255]),
        (x, y)
    )

#endregion

#region menu's

def display_render():
    completion = envir.calculate_completion()

    draw_loading_bar(650, 10, 300, 50, completion)
    draw_label(650, 150, f'Time Elapsed: {epoh_to_str(envir.elapsed_time)}')


    screen.blit(pygame.transform.scale(envir.rendering_surface, (600, 600)), (0, 0))

#endregion

while True:
    UI.update_events(pygame.event.get())
    for event in UI.events:
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    frame_start_time = time()
    screen.fill([20, 20, 20])

    display_render()
    UI.draw()

    pygame.display.update()
    clock.tick(fps)
    delta_time = time() - frame_start_time
    pygame.display.set_caption(f'Framerate: {int(clock.get_fps())}')




