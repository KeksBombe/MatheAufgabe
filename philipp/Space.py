import yaml
from itertools import combinations
from vpython import vector, mag, proj, box, color
import Ball


class Space():
    def __init__(self, depth= 10.0, width= 30.0, height= 45.0, thickness=0.2, file = "philipp/Kugeln.yaml"):
        self.depth = depth
        self.width = width
        self.height = height
        self.thickness = thickness
        self.spheres= set()

        with open(file, 'r') as f:
            data = yaml.safe_load(f)

        # Erstelle die Bälle
        for ball_name, ball_data in data['balls'].items():
            radius = ball_data['radius']
            vectorVel = ball_data['velocity']
            velocity =vector(vectorVel[0], vectorVel[1], vectorVel[2])
            vectorPos = ball_data['position']
            position = vector(vectorPos[0], vectorPos[1], vectorPos[2])
            farbe = ball_data['color']
            mass = ball_data['mass']
            self.spheres.add(Ball.Ball(radius=radius, position=position, velocity=velocity,
                                       color = vector(farbe[0], farbe[1], farbe[2]),
                                       mass=mass))
        wallR = box(pos=vector(self.width/2, 0, 0), size=vector(thickness, self.height - self.thickness, self.depth + self.thickness), color=color.red)
        wallL = box(pos=vector(-self.width/2, 0, 0), size=vector(thickness, self.height - self.thickness, self.depth + self.thickness), color=color.red)
        wallB = box(pos=vector(0, -self.height/2, 0), size=vector(self.width + self.thickness, thickness, self.depth + self.thickness), color=color.blue)
        wallT = box(pos=vector(0, self.height/2, 0), size=vector(self.width - self.thickness, thickness, self.depth - self.thickness), color=color.blue)
        wallBK = box(pos=vector(0, 0, -self.depth/2), size=vector(self.width - self.thickness, self.height - self.thickness, thickness), color=color.gray(0.7))

    def simulateStep(self, dt):
        teilmengen = list(combinations(self.spheres, 2))
        #Alle Teilmengen der Mächtigkeit 2
        for pair in teilmengen:
            ball1 = pair[0]
            ball2 = pair[1]
            pos1 = ball1.sphere.pos = ball1.sphere.pos + ball1.velocity * dt
            radius1 = ball1.sphere.radius
            pos2 = ball2.sphere.pos = ball2.sphere.pos + ball2.velocity * dt
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

                ball1.velocity = ball1.velocity - v1Collision + v1StrichCollision
                ball2.velocity = ball2.velocity - v2Collision + v2StrichCollision

        for ball in self.spheres:
            if not (-self.width / 2  + ball.sphere.radius) < ball.sphere.pos.x < (self.width / 2 - ball.sphere.radius):
                ball.velocity.x = -ball.velocity.x
            if not (-self.height / 2 + ball.sphere.radius) < ball.sphere.pos.y < (self.height / 2 - ball.sphere.radius):
                ball.velocity.y = -ball.velocity.y
            if not (-self.depth / 2 + ball.sphere.radius) < ball.sphere.pos.z < (self.depth / 2 - ball.sphere.radius):
                ball.velocity.z = -ball.velocity.z