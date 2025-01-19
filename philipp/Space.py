from logging import getLogger
from time import sleep

import yaml
from itertools import combinations

#from PyQt5.QtWidgets.QWidget import width
from vpython import vector, mag, proj, box, color, dot, norm
import philipp.Ball as Ball
import os
import logging
import math

from philipp.CollisionDetection import collidingSpheresWithSpheres, collisionHandlingSpheresWithSpheres
from philipp.view import makeBordersVisual


def createSpace(file):
    logger = getLogger(__name__)
    logging.basicConfig(filename='simulation.log', encoding='utf-8', level=logging.WARNING)
    with open(file, 'r') as space:
        spaceData = yaml.safe_load(space)
    width, height, depth = 0, 0, 0
    for name, dimension in spaceData['space']['dimensions'].items():
        dimValue = dimension['value']
        if not (dimension['range'][0] < dimValue < dimension['range'][1]):
            dimValue = min(dimValue, dimension['range'][1])
            dimValue = max(dimension['range'][0], dimValue)
            logger.warning(name + ' config out of range')
        if name == 'depth':
            depth = dimValue
        if name == 'width':
            width = dimValue
        if name == 'height':
            height = dimValue
    return width, height, depth

def createSpheres(file):
    with open(file, 'r') as f:
        data = yaml.safe_load(f)
    spheres = set()
    # Erstelle die Bälle
    for ball_name, ball_data in data['spheres'].items():
        radius = ball_data['radius']
        radius = max(min(radius['value'], radius['range'][1]), radius['range'][0])
        vectorVel = ball_data['velocity']
        velocity = vector(vectorVel[0], vectorVel[1], vectorVel[2])
        vectorPos = ball_data['position']
        position = vector(vectorPos[0], vectorPos[1], vectorPos[2])
        farbe = ball_data['color']
        mass = ball_data['mass']
        spheres.add(Ball.Ball(radius=radius, position=position, velocity=velocity,
                                   color=vector(farbe[0], farbe[1], farbe[2]),
                                   mass=mass))
    return spheres

class Space():
    def __init__(self, file = "philipp/Kugeln.yaml", fileSpace = "philipp/Space.yaml"):

        self.width, self.height, self.depth = createSpace(fileSpace)
        makeBordersVisual(fileSpace, self.height, self.width, self.depth)
        self.spheres= createSpheres(file)

    def simulateStep(self, dt, elasticity):
        spherecollisions = collidingSpheresWithSpheres(self.spheres, dt)
        collisionHandlingSpheresWithSpheres(dt, elasticity, spherecollisions)
        self.collisionWithBorder(dt, elasticity)
        self.zeitschritt(dt)

    def collisionWithBorder(self,dt, elasticity):
        #TODO
        for ball in self.spheres:
            if not (-self.width / 2 + ball.sphere.radius) < ball.sphere.pos.x:
                normalVektor = vector (1,0,0)
                depth = vector((-self.width / 2 + ball.sphere.radius), 0,0) - vector(ball.sphere.pos.x, 0,0)
                rueckStellVektor = helper(ball.velocity, normalVektor,depth)
                ball.sphere.pos = ball.sphere.pos + rueckStellVektor
                if not ball.velocity.x > 0:
                    ball.velocity.x = -ball.velocity.x * elasticity

            if not (self.width / 2 - ball.sphere.radius) > ball.sphere.pos.x:
                normalVektor = vector (-1,0,0)
                depth = vector(ball.sphere.pos.x, 0,0) - vector((self.width / 2 - ball.sphere.radius), 0,0)
                rueckStellVektor = helper(ball.velocity, normalVektor,depth)
                ball.sphere.pos = ball.sphere.pos + rueckStellVektor

                if not ball.velocity.x < 0:
                    ball.velocity.x = -ball.velocity.x * elasticity

            if not (-self.height / 2 + ball.sphere.radius) < ball.sphere.pos.y:
                if not ball.velocity.y > 0:
                    ball.velocity.y = -ball.velocity.y * elasticity
            if not (self.height / 2 - ball.sphere.radius) > ball.sphere.pos.y:
                if not ball.velocity.y < 0:
                    ball.velocity.y = -ball.velocity.y * elasticity

            if not (-self.depth / 2 + ball.sphere.radius) < ball.sphere.pos.z:
                if not ball.velocity.z > 0:
                    ball.velocity.z = -ball.velocity.z * elasticity
            if not (self.depth / 2 - ball.sphere.radius) > ball.sphere.pos.z:
                if not ball.velocity.z < 0:
                    ball.velocity.z = -ball.velocity.z * elasticity



    def zeitschritt(self, dt):
        for ball in self.spheres:
            ball.sphere.pos = ball.sphere.pos + ball.velocity * dt

vec1 = vector(1,0,0)
vec2 = vector(-1,0,0)
angle = vec1.diff_angle(vec2)
print((angle/(2* math.pi))*360)

def helper(vec1, normalVec, depth):
    angle = vec1.diff_angle(normalVec)
    angle = angle - (math.pi/2)
    betragRueckStellVektor = depth.mag
    try:
        betragRueckStellVektor = depth.mag / math.sin(angle)
    except ZeroDivisionError:
        print("false")
    rueckstellvektor = betragRueckStellVektor * -norm(vec1)
    print(rueckstellvektor)
    return rueckstellvektor