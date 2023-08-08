# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:          Joshua Perry
#                Ryan Nguyen
#                Yujiro Ochiai
#                Weston Bauer
# Section:      520
# Assignment:   fun_game
# Date:         12 / 7 / 2022

#We were given permission to use pygame instead of turtle graphics

#Caution dear reader, what you are about to witness is NSFW
#You have been warned

import sys, pygame
import math
import time
import random
import numpy as np
import threading  #biggest pain to implement, but performance really needed it
#probably implemented it poorly,

pygame.init()

fps = 30
bullets = 15
numberOfWaves = 15
size = width, height = 1500, 1000

screen = pygame.display.set_mode(size)


class objects(object):

  def __init__(self,
               x=10,
               y=10,
               accel=.5,
               maxSpeed=5,
               width=50,
               height=50,
               friction=.2,
               img="intro_ball.gif",
               collide=True,
               power="n",
               orientation=False,
               currImage=False):
    self.width = width
    self.height = height
    self.collide = collide
    self.maxSpeed = maxSpeed
    self.accel = accel
    self.friction = friction
    self.power = power
    self.accx = 0
    self.accy = 0
    self.volx = 0
    self.voly = 0
    self.orientation = orientation
    if bool(currImage):
      self.currImage = pygame.transform.scale(pygame.image.load(currImage),
                                              (width, height))
    self.img = pygame.transform.scale(pygame.image.load(img), (width, height))
    self.position = self.img.get_rect().move([x, y])

  def Move(self, x=0, y=0):
    """updates acceleration of object with given input"""
    self.accx = x
    self.accy = y

  def update(self):
    """updates position of object based on its velocity and acceleration"""
    if abs(self.volx + self.accx) < self.maxSpeed:
      self.volx += self.accx
    else:
      self.volx = self.maxSpeed if self.volx > 0 else -self.maxSpeed
    if abs(self.voly + self.accy) < self.maxSpeed:
      self.voly += self.accy
    else:
      self.voly = self.maxSpeed if self.voly > 0 else -self.maxSpeed
    self.position = self.position.move(self.volx, self.voly)


class button(objects):

  def __init__(self,
               x=100,
               y=100,
               width=500,
               height=100,
               img="intro_ball.gif",
               c=0):
    objects.__init__(self,
                     x=x,
                     y=y,
                     width=width,
                     height=height,
                     img=img,
                     collide=False,
                     maxSpeed=bullets)
    self.c = c

  def isClicked(self):
    """returns true if the button's coordinate is being pressed"""
    try:
      if pygame.mouse.get_pressed()[0] and event.button == 1:
        if self.position.collidepoint(pygame.mouse.get_pos()):
          return True
        return False
    except:
      return False


class zombieSpawn(objects):

  def __init__(self, x=50, y=50, img="intro_ball.gif"):
    objects.__init__(self, x=x, y=y, img=img, collide=False)


class bullet(objects):

  def __init__(self,
               x,
               y,
               vx=1,
               vy=-1,
               damage=50,
               time=10,
               img="intro_ball.gif",
               width=5,
               height=5,
               ctime=0):
    objects.__init__(self,
                     x=x,
                     y=y,
                     width=width,
                     img=img,
                     height=height,
                     maxSpeed=bullets,
                     collide=False)
    self.ctime = ctime
    self.time = time
    self.damage = damage
    self.volx = vx
    self.voly = vy

  def unload(self):
    """destroys the bullet if it has been longer than self.time"""
    if (c - self.ctime) / fps >= self.time:
      destroy(self)

  def dmgEnim(self):
    obsticle = collision(self, [])
    if bool(obsticle):
      if type(obsticle) != type(player()):
        try:
          obsticle.health -= self.damage
        except:
          pass
        destroy(self)

  def update(self):
    self.unload()
    self.dmgEnim()
    self.position = self.position.move(self.volx, self.voly)


class zombie(threading.Thread, objects):

  def __init__(self,
               x=300,
               y=300,
               accel=.1,
               maxSpeed=3,
               width=50,
               height=50,
               friction=.1,
               img="intro_ball.gif",
               health=100,
               dmg=10,
               currc=0,
               cooldown=3):
    threading.Thread.__init__(self)
    objects.__init__(self,
                     x,
                     y,
                     accel,
                     maxSpeed,
                     width,
                     height,
                     friction,
                     img,
                     orientation=[0, -1],
                     currImage=img)
    self.health = health
    self.dmg = dmg
    self.target = p1s[0]
    self.currc = currc
    self.cooldown = cooldown

  def setarget(self):
    if (len(p1s) != 0):
      shortest = distance(self, p1s[0])
      self.target = p1s[0]
      for player in p1s:
        if shortest > distance(self, player):
          shortest = distance(self, player)
          self.target = player

  def run(self):  # D=
    while ingame and self in zombsq:
      time.sleep(1 / fps)
    while ingame and self in zombs:
      self.zomb()
      rotateImage(self)
      event_obj.wait()

  def zomb(self):
    self.setarget()
    dist = distance(self, self.target)
    x = 0
    y = 0
    if dist != 0:
      x, y = self.target.position.center
      tx, ty = self.position.center
      x = (x - tx) / dist
      y = (y - ty) / dist
    if abs(x) < 0.1:
      if x > 0:
        x -= x * self.friction
        if x > .01:
          x -= .01
        else:
          x = 0
      elif x < 0:
        x += x * self.friction
        if x < -.01:
          x += .01
        else:
          x = 0
    if abs(y) < 0.1:
      if y > 0:
        y -= y * self.friction
        if y > .01:
          y -= .01
        else:
          y = 0
      elif y < 0:
        y += y * self.friction
        if y < -.01:
          y += .01
        else:
          y = 0
    touching = collide(self, [], x, y)
    for things in touching:
      if type(things) == type(
          player()) and (c - self.currc) / fps >= self.cooldown:
        things.health -= self.dmg
        self.currc = c

  def update(self):
    if (self.health <= 0):
      destroy(self)
    else:
      super().update()


class player(objects):

  def __init__(self,
               x=10,
               y=10,
               width=50,
               height=50,
               accel=.5,
               maxSpeed=5,
               friction=.5,
               reload=1,
               damage=50,
               movement=[
                 pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT,
                 pygame.K_PERIOD
               ],
               img="Player1.gif",
               health=100,
               target=False,
               currc=0):
    objects.__init__(self,
                     x=x,
                     y=y,
                     img=img,
                     width=width,
                     height=height,
                     accel=accel,
                     maxSpeed=maxSpeed,
                     friction=friction,
                     orientation=[0, -1],
                     currImage=img)
    self.movement = movement
    self.health = health
    self.reload = reload
    self.damage = damage
    self.target = target
    self.currc = currc

  def displaycurrenthealth(self, number):

    healthbar = pygame.Rect(10, 10 + 60 * number, 200, 50)
    greenrect = pygame.Rect(70, 10 + 60 * number, int(1.5 * self.health), 50)

    screen.blit(
      pygame.transform.scale(pygame.image.load("HealthBar.gif"), (200, 50)),
      healthbar)
    screen.blit(
      pygame.transform.scale(pygame.image.load("GreenHealth.gif"),
                             (int(1.5 * self.health), 50)), greenrect)

  def upgrade(self, maxSpeed=-1, accel=-1, reload=-1, damage=-1):
    if maxSpeed != -1:
      self.maxSpeed = maxSpeed
    if accel != -1:
      self.accel = accel
    if reload != -1:
      self.reload = reload
    if damage != -1:
      self.damage = damage

  def consume(self, power):
    if power.power != 'n':
      if power.power[0] == "s":
        self.upgrade(accel=self.accel * 1.1, maxSpeed=self.maxSpeed * 1.1)
      elif power.power[0] == "r":
        self.upgrade(reload=self.reload / 1.1)
      elif power.power[0] == "d":
        self.upgrade(damage=self.damage * 1.2)

      for num, item in enumerate(objs):
        if item == power:
          objs.pop(num)
          break

  def shoot(self):
    if self.findZomb() and (c - self.currc) / fps >= self.reload:
      self.currc = c
      global objs
      dist = distance(self, self.target)
      if dist != 0:
        x, y = self.target.position.center
        tx, ty = self.position.center
        x = bullets * (x - tx) / dist
        y = bullets * (y - ty) / dist
        objs += [bullet(tx, ty, x, y, damage=self.damage, ctime=c)]

  def findZomb(self):
    if (len(zombs) == 0):
      return False
    shortest = distance(self, zombs[0])
    self.target = zombs[0]
    for zombie in zombs:
      if shortest > distance(self, zombie):
        shortest = distance(self, zombie)
        self.target = zombie
    return True

  def update(self):
    self.findZomb()
    if (self.health < 100 and c % fps == 0):
      self.health += 1
    if (self.health <= 0):
      destroy(self)
    else:
      super().update()


def distance(obj1, obj2):
  """returns the distance between the two object's centers"""
  x1, y1 = obj1.position.center
  x2, y2 = obj2.position.center
  return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)


def collision(obj, objes, x=0, y=0):
  """returns the object obj is touching that isn't in objes and will consume any power up if obj is a player"""
  objes += [obj]
  for ob in objs:
    if obj.position.move(obj.volx + x, obj.voly + y).colliderect(
        ob.position) and ob not in objes:
      if ob.collide:
        return ob
      else:
        if type(obj) == type(player()):
          obj.consume(ob)
  return False


def collide(obj, objes, x=0, y=0):
  """will move the obj with the acceleration of x and y without intersecting another object"""
  problem = collision(obj, objes, 0, 0)
  if bool(problem) and problem.collide:
    px, py = problem.position.center
    cx, cy = obj.position.center
    tempx = obj.position.x
    tempy = obj.position.y
    if abs(cx - px) > abs(cy - py):
      if cx > px:
        tempx += 50 + px - cx
      else:
        tempx += 50 + cx - px
    else:
      if cy > py:
        tempy += 50 + py - cy
      else:
        tempy += 50 + cy - py
    problem = collision(objects(x=tempx, y=tempy), objes)
    if (not bool(problem)
        or not problem.collide) or (abs(obj.position.x - tempx) < 2
                                    and abs(obj.position.y - tempy) < 2):
      obj.position.x = tempx
      obj.position.y = tempy
  Clyde = collision(obj, objes, x, y)
  while bool(Clyde):
    if Clyde.collide:
      cx, cy = Clyde.position.center
      px, py = obj.position.center
      if abs(cx - px) < abs(cy - py):
        y = 0
        obj.voly = 0
      else:
        x = 0
        obj.volx = 0
    objes += [Clyde]
    Clyde = collision(obj, objes, x, y)
  obj.Move(x, y)
  return (objes)


def rotate(obj, x=1, y=-1):
  """returns a rotated image"""
  return pygame.transform.rotate(obj.img, np.arctan2(x, y) * 180 / np.pi)


def controol(plays):
  """performs player movement with its player.movement controls"""
  key = pygame.key.get_pressed()
  x = 0
  y = 0
  if key[plays.movement[0]]:
    y -= plays.accel
  if key[plays.movement[1]]:
    x -= plays.accel
  if key[plays.movement[2]]:
    y += plays.accel
  if key[plays.movement[3]]:
    x += plays.accel
  if key[plays.movement[4]]:
    plays.shoot()
  if x == 0:
    if plays.volx > 0:
      if plays.volx < plays.friction:
        plays.volx = 0
      else:
        plays.volx -= plays.friction
    else:
      if plays.volx > plays.friction:
        plays.volx = 0
      else:
        plays.volx += plays.friction
  if y == 0:
    if plays.voly > 0:
      if plays.voly < plays.friction:
        plays.voly = 0
      else:
        plays.voly -= plays.friction
    else:
      if plays.voly > plays.friction:
        plays.voly = 0
      else:
        plays.voly += plays.friction
  collide(plays, [], x, y)


def destroy(obj):
  """deletes the object from any list from which it came"""
  try:
    if (type(obj) == type(player())):
      for num, ob in enumerate(p1s):
        if ob == obj:
          p1s.pop(num)
  except:
    pass
  try:
    if (type(obj) == type(zombie())):
      for num, ob in enumerate(zombs):
        if ob == obj:
          zombs.pop(num)
  except:
    pass
  for num, ob in enumerate(objs):
    if ob == obj:
      objs.pop(num)


def destroys(manyobjects):
  """deletes the objects from any list from which any of them came"""
  for i in manyobjects:
    destroy(i)


def loadMap(fileName, player2=False):
  """loads the map and possibly player 2 from the file that is given"""
  global p1s
  global zombs
  global objs
  global zombieSpawns
  global zombsq
  global ingame
  global wave
  global possiblespots
  wave = 1
  p1s = []
  zombs = []
  zombieSpawns = []
  possiblespots = []
  objs = []
  zombsq = []
  with open(fileName, "r") as file:
    for y, line in enumerate(file.readlines()):
      for x, letter in enumerate(line.strip()):
        if letter == 'o':
          objs += [objects(x=x * 50, y=y * 50, collide=True, img="Block.gif")]
        elif letter == '1':
          p1s += [player(x=x * 50, y=y * 50)]
        elif letter == '2' and player2:
          p1s += [
            player(x=x * 50,
                   y=y * 50,
                   movement=[
                     pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d,
                     pygame.K_SPACE
                   ],
                   img="Player2.gif")
          ]
        elif letter == "s":
          zombieSpawns += [zombieSpawn(x=x * 50, y=y * 50, img="Grave.gif")]
        else:
          possiblespots += [[x * 50, y * 50]]
  ingame = True


def loadWave(fileName, wave):
  """loads the zombie wave from the file and line that is given into the zombie que"""
  global zombsq
  global numberOfWaves
  global initializeZomb
  with open(fileName, "r") as file:
    waves = file.readlines()
    numberOfWaves = len(waves)
    wave = waves[wave - 1].strip()
    for letter in wave:
      if letter == "e":
        zombsq += [zombie(maxSpeed=2, health=50, dmg=5, img="Zombie easy.gif")]
      elif letter == "m":
        zombsq += [
          zombie(maxSpeed=3, health=80, dmg=10, img="Zombie medium.gif")
        ]
      elif letter == "h":
        zombsq += [
          zombie(maxSpeed=4, health=100, dmg=15, img="Zombie hard.gif")
        ]
      elif letter == "x":
        zombsq += [
          zombie(maxSpeed=5, health=250, dmg=20, img="Zombie extreme.gif")
        ]
    for item in zombsq:
      item.start()


def randomSpawnUpgrade(chance=800):
  """may or may not spawn a power up"""
  if (random.randint(1, chance) == 1):
    power = random.randint(0, 2)
    if power == 0:
      spawnUpgrade("d", "Damage.gif")
    elif power == 1:
      spawnUpgrade("r", "Reload.gif")
    else:
      spawnUpgrade("s", "Speed.gif")


def spawnUpgrade(powerup, img):
  """spawns a power up somewhere on the map"""
  global objs
  global possiblespots
  x, y = possiblespots[random.randint(0, len(possiblespots) - 1)]
  objs += [objects(x=x, y=y, collide=False, power=powerup, img=img)]


def tryToSpawnQ(chance=60):
  """may or may not spawn the next zombie in the zombie que"""
  global zombs
  global zombsq
  if len(zombsq) > 0 and len(zombieSpawns) > 0:
    for spawn in zombieSpawns:
      if len(zombsq) > 0:
        zombsq[0].position.x = spawn.position.x
        zombsq[0].position.y = spawn.position.y
        try:
          if not collision(zombsq[0], []) and random.randint(1, chance) == 1:
            zombs += [zombsq[0]]
            zombsq.pop(0)
            return True
        except:
          pass


def updateobjs(curlist=-1):
  """updates objs with the necessary sublists"""
  if curlist != -1:
    global objs
    for unit in curlist:
      if unit not in objs:
        objs += [unit]
  else:
    updateobjs(p1s)
    updateobjs(zombs)
    updateobjs(zombieSpawns)


def istherezombies():
  """returns True if there is a zombie on the map"""
  for obj in objs:
    if type(obj) == type(zombie):
      return True
  if len(zombsq) > 0:
    return True
  if len(zombs) > 0:
    return True
  return False


def waitfor(duration):
  """waits for duration - how long it has been since this was last called"""
  global currentTime
  newtime = time.time()
  try:
    time.sleep(duration - (newtime - currentTime))
  except:
    pass
  currentTime = newtime


def rotateImage(unit):
  """updates an image to its rotated self based on the nearest enemy"""
  if bool(unit.orientation) and bool(unit.target):
    if abs(
        abs(
          np.arctan2(unit.target.position.x - unit.position.x,
                     unit.target.position.y - unit.position.y) -
          np.arctan2(unit.orientation[0], unit.orientation[1]))) > .3:
      unit.currImage = rotate(unit, unit.target.position.x - unit.position.x,
                              unit.target.position.y - unit.position.y)
      unit.orientation[0] = unit.target.position.x - unit.position.x
      unit.orientation[1] = unit.target.position.y - unit.position.y


def render(unit):
  """draws onto the screen unit"""
  if bool(unit.orientation) and bool(unit.target):
    screen.blit(
      unit.currImage,
      pygame.Rect(unit.position.center[0] - unit.currImage.get_width() / 2,
                  unit.position.center[1] - unit.currImage.get_height() / 2,
                  50, 50))
  else:
    screen.blit(unit.img, unit.position)


def showAll():
  """draws onto the screen everything in objs"""
  for obj in objs:
    obj.update()
    render(obj)
  for num, thisplayer in enumerate(p1s):
    thisplayer.displaycurrenthealth(num)
  pygame.display.flip()


possiblespots = []  # list of possible spots for power ups to spawn
p1s = []  # list of current / alive players
zombs = []  #list of current / alive zombies
zombieSpawns = []  #list of possible zombie spawning locations
zombsq = []  #list of zombies waiting to be spawned
objs = []  #list of objects on screen
menu = [
  button(x=400, y=100, width=700, height=300, img="Title-Rad..png"),
  button(x=500, y=500, img="1_player.gif"),
  button(x=500, y=650, img="2_player.gif"),
  button(x=500, y=800, img="How_to.gif")
]  #list of everything to be displayed on the menu screen
menuc = 0
info = button(x=400, y=300, width=700, height=400, img="HowTo.gif")
win = button(x=400, y=300, width=700, height=400, img="Winner.gif")
lose = button(x=400, y=300, width=700, height=400, img="Loser.gif")
MapSelect = [
  button(x=500, y=300, img="Map_1.gif"),
  button(x=500, y=450, img="Map_2.gif"),
  button(x=500, y=600, img="Back.gif")
]  #list of everything to be displayed on the map select scree
mapc = 0
objs += menu
p2s = False
ingame = False
wave = 1
c = 0
currentTime = time.time()
event_obj = threading.Event()

#Everything up until now has just been initialization and function / class creation

while True:
  if menu[1].isClicked() and menu[
      1] in objs and c - menuc > 2 * fps / 3:  # if player1 menu button is pressed
    destroys(menu)
    p2s = False
    mapc = c
    objs += MapSelect

  if menu[2].isClicked() and menu[
      2] in objs and c - menuc > 2 * fps / 3:  # if player2 menu button is pressed
    destroys(menu)
    p2s = True
    mapc = c
    objs += MapSelect

  if menu[3].isClicked() and menu[
      3] in objs and c - menuc > 2 * fps / 3:  # if How-to menu button is pressed
    objs += [info]
    destroys(menu)

  if info.isClicked() and info in objs:  # if info screen is pressed
    destroy(info)
    menuc = c
    objs += menu

  if MapSelect[0].isClicked() and MapSelect[
      0] in objs and c - mapc > 2 * fps / 3:  # if map1 button is pressed
    loadMap("map1.txt", p2s)
  if MapSelect[1].isClicked() and MapSelect[
      1] in objs and c - mapc > 2 * fps / 3:  # if map2 button is pressed
    loadMap("map2.txt", p2s)
  if MapSelect[2].isClicked() and MapSelect[
      2] in objs and c - mapc > 2 * fps / 3:  # if back button is pressed
    destroys(MapSelect)
    menuc = c
    objs += menu

  if win.isClicked() and win in objs:  # if win screen is pressed
    menuc = c
    objs = menu[:]

  if lose.isClicked() and lose in objs:  # if you're a looser screen is pressed
    menuc = c
    objs = menu[:]

  updateobjs()  #update objects in objects on screen list
  c += 1  #update current frame
  waitfor(1 / fps)
  for event in pygame.event.get():  #if red x button is pressed
    if event.type == pygame.QUIT:
      ingame = False
      sys.exit()
  screen.fill([0, 0, 0])
  if ingame:  #if a round is ovvuring
    randomSpawnUpgrade()
    calctime = time.time()
    for plays in p1s:
      controol(plays)
      rotateImage(plays)
      if not pygame.Rect(0, 0, width, height).colliderect(
          plays.position):  #if a player is out of bounds
        destroy(plays)
    for zombi in zombs:
      event_obj.set()
    if not istherezombies():
      if wave <= numberOfWaves:  # if there is another wave after the one that just ended
        loadWave("zombies.txt", wave)
        randomSpawnUpgrade(1)
        wave += 1
      else:
        objs = [win]
        ingame = False
        p1s = []
        zombs = []
        zombieSpawns = []
    if len(p1s) == 0 and ingame:  # if there are no players alive
      objs = [lose]
      ingame = False
      p1s = []
      zombs = []
      zombieSpawns = []
    tryToSpawnQ(120)
  rendertime = time.time()
  showAll()
  pygame.display.flip()
