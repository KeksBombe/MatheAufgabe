from logging import getLogger

import yaml
from itertools import combinations
from vpython import vector, mag, proj, box, color
import Ball as Ball
import os
import logging


class Space():
    def __init__(self, file = "philipp/Kugeln.yaml", fileSpace = "philipp/Space.yaml"):
        logger = getLogger(__name__)
        logging.basicConfig(filename='simulation.log', encoding='utf-8', level=logging.WARNING)
        with open(fileSpace, 'r') as space:
            spaceData = yaml.safe_load(space)

        for name, dimension in spaceData['space']['dimensions'].items():
            dimValue = dimension['value']
            if not (dimension['range'][0] < dimValue < dimension['range'][1]):
                dimValue = min(dimValue,dimension['range'][1])
                dimValue = max(dimension['range'][0], dimValue)
                logger.warning(name + ' config out of range')
            if name == 'depth':
                self.depth = dimValue
            if name == 'width':
                self.width = dimValue
            if name == 'height':
                self.height = dimValue

        borderSection = spaceData['space']['border']['thickness']
        thickness = borderSection['value']
        if not (borderSection['range'][0] < thickness < borderSection['range'][1]):
            thickness = max(thickness,borderSection['range'][0])
            thickness = min(thickness,borderSection['range'][1])
            logger.warning('thickness config out of range')
        self.thickness = thickness

        if spaceData['space']['border']['visable']:
            wallR = box(pos=vector(self.width / 2, 0, 0),
                        size=vector(thickness, self.height - self.thickness, self.depth + self.thickness),
                        color=color.red)
            wallL = box(pos=vector(-self.width / 2, 0, 0),
                        size=vector(thickness, self.height - self.thickness, self.depth + self.thickness),
                        color=color.red)
            wallB = box(pos=vector(0, -self.height / 2, 0),
                        size=vector(self.width + self.thickness, thickness, self.depth + self.thickness),
                        color=color.blue)
            wallT = box(pos=vector(0, self.height / 2, 0),
                        size=vector(self.width - self.thickness, thickness, self.depth - self.thickness),
                        color=color.blue)
            wallBK = box(pos=vector(0, 0, -self.depth / 2),
                         size=vector(self.width - self.thickness, self.height - self.thickness, thickness),
                         color=color.gray(0.7))
        self.spheres= set()

        with open(file, 'r') as f:
            data = yaml.safe_load(f)

        # Erstelle die Bälle
        for ball_name, ball_data in data['spheres'].items():
            radius = ball_data['radius']
            radius = max(min(radius['value'], radius['range'][1]), radius['range'][0])
            vectorVel = ball_data['velocity']
            velocity =vector(vectorVel[0], vectorVel[1], vectorVel[2])
            vectorPos = ball_data['position']
            position = vector(vectorPos[0], vectorPos[1], vectorPos[2])
            farbe = ball_data['color']
            mass = ball_data['mass']
            self.spheres.add(Ball.Ball(radius=radius, position=position, velocity=velocity,
                                       color = vector(farbe[0], farbe[1], farbe[2]),
                                       mass=mass))


    def simulateStep(self, dt, elasticity):
        self.collisionDetection(dt, elasticity)
        self.collisionWithBorder(dt, elasticity)
        self.zeitschritt(dt)



    def collisionDetection(self, dt, elasticity):
        teilmengen = list(combinations(self.spheres, 2))
        ball1 = None
        ball2 = None
        #Alle Teilmengen der Mächtigkeit 2
        for pair in teilmengen:
            ball1 = pair[0]
            ball2 = pair[1]
            pos1 = ball1.sphere.pos + ball1.velocity * dt
            radius1 = ball1.sphere.radius
            pos2 = ball2.sphere.pos + ball2.velocity * dt
            radius2 = ball2.sphere.radius
            dif = pos1 - pos2
            if mag(dif) < (radius2 + radius1):
                n = dif
                v1Collision = proj(ball1.velocity, n)
                v2Collision = proj(ball2.velocity, n)

                m1 = ball1.mass
                m2 = ball2.mass

                v1StrichCollision = (m1 * v1Collision + m2 * (2 * v2Collision - v1Collision)) / (m1 + m2)
                v2StrichCollision = (m2 * v2Collision + m1 * (2 * v1Collision - v2Collision)) / (m1 + m2)

                v1StrichCollision = v1StrichCollision * elasticity
                v2StrichCollision = v2StrichCollision * elasticity

                ball1.velocity = ball1.velocity - v1Collision + v1StrichCollision
                ball2.velocity = ball2.velocity - v2Collision + v2StrichCollision

    def collisionWithBorder(self,dt, elasticity):
        for ball in self.spheres:
            futureposition = ball.sphere.pos + ball.velocity * dt
            if not (-self.width / 2  + ball.sphere.radius) < futureposition.x < (self.width / 2 - ball.sphere.radius):
                ball.velocity.x = -ball.velocity.x * elasticity
            if not (-self.height / 2 + ball.sphere.radius) < futureposition.y < (self.height / 2 - ball.sphere.radius):
                ball.velocity.y = -ball.velocity.y * elasticity
            if not (-self.depth / 2 + ball.sphere.radius) < futureposition.z < (self.depth / 2 - ball.sphere.radius):
                ball.velocity.z = -ball.velocity.z * elasticity

    def zeitschritt(self, dt):
        for ball in self.spheres:
            ball.sphere.pos = ball.sphere.pos + ball.velocity * dt