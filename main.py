import pygame, pickle, pytmx, random
from pygame.math import Vector2
from game import ui, entities, maploader, objects

"""
PyWeek 29 Game
Copyright (c) 2020 Orion Williams
See LICENSE file

Current File: MAIN.PY
"""

#INITIATION STUFF
pygame.init()
pygame.display.init()
pygame.mixer.init()

#PYGAME SETUP STUFF
window = pygame.display.set_mode([800, 600])
pygame.display.set_caption("PyWeek 29")

pygame.time.set_timer(pygame.USEREVENT + 1, 40)
pygame.time.set_timer(pygame.USEREVENT + 2, 500)

#GAME SETUP STUFF
ui.Color("w")
menubuttons = pygame.sprite.Group()
playbutton = ui.TextButton("play", [10, 100])
howbutton = ui.TextButton("how to play", [10, 150])
quitbutton = ui.TextButton("quit", [10, 200])
menubuttons.add(playbutton)
menubuttons.add(howbutton)
menubuttons.add(quitbutton)
completebuttons = pygame.sprite.Group()
nextbutton = ui.TextButton("Next Level", [305, 275])
replaybutton = ui.TextButton("Replay Level", [305, 300])
returnbutton = ui.TextButton("Return to Menu", [305, 325])
completebuttons.add(nextbutton)
completebuttons.add(replaybutton)
completebuttons.add(returnbutton)

ui.Color([255, 0, 0])
backbutton = ui.TextButton("Back", [10, 10])

#DEFINITION STUFF
running = True
screen = "menu"
prevscreen = "menu"
mouse = [0, 0]
addedripples = 0
npebble = None
level = 1
coins = 0
collected: int = 0
pid = 0
startclicked = False
startpos = [Vector2(140, 160), Vector2(100, 100), Vector2(100, 520), Vector2(400, 300), Vector2(140, 100), Vector2(140, 100), Vector2(500, 80), Vector2(100, 80), Vector2(120, 300), Vector2(180, 80), Vector2(100, 100), Vector2(700, 100), Vector2(100, 80), Vector2(100, 80), Vector2(400, 100)]
grassmusic = ["./resources/music/sunsetsong.mp3", "./resources/music/rainywindow.mp3", "./resources/music/theend.mp3", "./resources/music/midsummerambient.mp3"]
desertmusic = ["./resources/music/sunsetsong.mp3", "./resources/music/desertsong.mp3", "./resources/music/miragesong.mp3", "./resources/music/midsummerambient.mp3", "./resources/music/theend.mp3", "./resources/music/tropicice.mp3"]
icemusic = ["./resources/music/arcticambient.mp3", "./resources/music/tropicice.mp3", "./resources/music/snowynight.mp3", "./resources/music/rainywindow.mp3", ]

alltiles = pygame.sprite.Group()
walls = pygame.sprite.Group()
floatys = pygame.sprite.Group()
coingrp = pygame.sprite.Group()
drains = pygame.sprite.Group()
sharks = pygame.sprite.Group()
waterfalls = pygame.sprite.Group()
grass = pygame.sprite.Group()
alltiles, walls, floatys, coingrp, drains, sharks, waterfalls, grass = maploader.loadmap(random.randint(0, 15))

boat = entities.Boat([360, 280])
pebbles = pygame.sprite.Group()
ripples = pygame.sprite.Group()
trails = pygame.sprite.Group()

def loadLevel(level):
    global boat, alltiles, walls, floatys, drains, startpos, collected, coingrp, sharks, grass, screen, grassmusic, desertmusic, icemusic
    if level > 15:
        screen = "menu"
        pygame.mixer.music.stop()
    else:
        alltiles = pygame.sprite.Group()
        walls = pygame.sprite.Group()
        floatys = pygame.sprite.Group()
        coingrp = pygame.sprite.Group()
        drains = pygame.sprite.Group()
        sharks = pygame.sprite.Group()
        waterfalls = pygame.sprite.Group()
        grass = pygame.sprite.Group()
        alltiles, walls, floatys, coingrp, drains, sharks, waterfalls, grass = maploader.loadmap(level)
        boat.rect.center = startpos[level-1]
        boat.coords = boat.rect.left, boat.rect.top
        boat.reachedgate = False
        collected = 0
        boat.collected = 0
        boat.health = 100
        if level < 7:
            pygame.mixer.music.load(random.choice(grassmusic))
        if level < 12 and level > 6:
            pygame.mixer.music.load(random.choice(desertmusic))
        if level > 11:
            pygame.mixer.music.load(random.choice(icemusic))

def loadmusic():
    global level
    if pygame.mixer.music.get_busy() == 0:
        if level < 7:
            pygame.mixer.music.load(random.choice(grassmusic))
        if level < 12 and level > 6:
            pygame.mixer.music.load(random.choice(desertmusic))
        if level > 11:
            pygame.mixer.music.load(random.choice(icemusic))
        pygame.mixer.music.play()

def newpebble():
    global mouse, npebble, pebbles, ripples, addedripples, pid
    pid += 1
    npebble = entities.Pebble([400, 596], mouse, pid)
    #ntrail = entities.Trail(pid, npebble)
    pebbles.add(npebble)
    #trails.add(ntrail)
    addedripples = 0
    pygame.time.set_timer(pygame.USEREVENT + 2, 500)

def addripples():
    global npebble, addedripples, ripples
    if addedripples == 1:
        nripple = entities.Ripple(npebble.rect.center, 0.015, 0.5, centered=True)
        ripples.add(nripple)
        addedripples+=1
    if addedripples == 2:
        nripple = entities.Ripple(npebble.rect.center, 0.0175, 0.25, centered=True)
        ripples.add(nripple)
        addedripples += 1
    if addedripples == 3:
        nripple = entities.Ripple(npebble.rect.center, 0.02, 0.2, centered=True)
        ripples.add(nripple)
        addedripples = 0

def levelcomplete():
    surface = pygame.surface.Surface([200, 150])
    surface.set_alpha(128)
    window.blit(surface, [300, 225])
    ui.SetFont("w", 28)
    ui.Text("level " + str(level) + " complete!", window, [305, 225])
    completebuttons.draw(window)

def infobox():
    global boat, collected, window
    surface = pygame.surface.Surface([220, 75])
    surface.set_alpha(127)
    window.blit(surface, [10, 515])
    ui.SetFont("w", 30)
    ui.Text("health - " + str(boat.health) + "%", window, [15, 520])
    ui.Text("coins collected - " + str(collected), window, [15, 555])

def updateall():
    waterfalls.update(boat)
    coingrp.update(boat)
    floatys.update(boat)
    drains.update(boat)
    sharks.update(boat)
    boat.update(walls, startpos[level - 1])
    alltiles.update(boat)

#GAME LOOP STUFF
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            mouse = list(pygame.mouse.get_pos())
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pressed = pygame.mouse.get_pressed()
            mouse = list(pygame.mouse.get_pos())
            if screen == "menu":
                if pressed[0] == 1:
                    if playbutton.click(mouse):
                        screen = "game"
                        level = 1
                        pygame.mixer.music.stop()
                        loadLevel(level)
                        pygame.mixer.music.play()
                        startclicked = True
                    elif quitbutton.click(mouse):
                        running = False
            if screen == "level complete":
                if pressed[0] == 1:
                    if nextbutton.click(mouse):
                        screen = "game"
                        level += 1
                        pygame.mixer.music.stop()
                        loadLevel(level)
                        pygame.mixer.music.play()
                    if replaybutton.click(mouse):
                        screen = "game"
                        pygame.mixer.music.stop()
                        loadLevel(level)
                        pygame.mixer.music.play()
                    if returnbutton.click(mouse):
                        screen = "menu"
                        level = 1
                        pygame.mixer.music.stop()
            elif screen == "game" and not screen == "menu":
                if pressed[0] == 1:
                    if not startclicked:
                        newpebble()
                    else:
                        startclicked = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                boat.reachedgate = True
        elif event.type == pygame.USEREVENT + 1:
            ripples.update(boat, ripples)
            pebbles.update(boat)
            trails.update()
            if boat.startripples:
                boat.startripples = False
                nripple = entities.Ripple(boat.startripplesat, 0.01, 1, centered=True)
                ripples.add(nripple)
                addedripples = 1
                pygame.time.set_timer(pygame.USEREVENT + 2, 500)
        elif event.type == pygame.USEREVENT + 2:
            if not addedripples == 0:
                addripples()


    if screen == "menu":
        window.fill([255, 255, 255])
        window.fill([45, 124, 188])
        ripples.draw(window)
        alltiles.draw(window)
        grass.draw(window)
        pebbles.draw(window)
        surface = pygame.surface.Surface([270, 600])
        surface.set_alpha(127)
        window.blit(surface, [0, 0])
        ui.SetFont("w", 48)
        ui.Text("calm waters", window, [10, 10])
        menubuttons.draw(window)
        pygame.mixer.music.stop()
    if screen == "game":
        collected = boat.collected
        window.fill([45, 124, 188])
        ripples.draw(window)
        alltiles.draw(window)
        boat.draw(window)
        grass.draw(window)
        infobox()
        pebbles.draw(window)
        updateall()
        hits = pygame.sprite.spritecollide(boat, ripples, False, pygame.sprite.collide_mask)
        loadmusic()
        if boat.reachedgate:
            screen = "level complete"
            boat.reachedgate = False
            coins += collected
        if len(hits) > 0 and not boat.hitrock:
            for ripple in hits:
                ripple.kill()
                if not ripple.hit:
                    boat.accelerate(ripple, walls)
                ripples.add(ripple)
        if boat.health <= 0:
            loadLevel(level)
    if screen == "level complete":
        window.fill([45, 124, 188])
        ripples.draw(window)
        alltiles.draw(window)
        boat.draw(window)
        grass.draw(window)
        pebbles.draw(window)
        updateall()
        hits = pygame.sprite.spritecollide(boat, ripples, False, pygame.sprite.collide_mask)
        if len(hits) > 0:
            for ripple in hits:
                ripple.kill()
                if not ripple.hit:
                    boat.accelerate(ripple, walls)
                ripples.add(ripple)
        levelcomplete()

    print(level)
    pygame.display.flip()

#CLOSE GAME STUFF
pygame.quit()