from vpython import vector, mag, proj, box, color, dot, norm
import math
from philipp.CollisionDetection import collidingSpheresWithSpheres, collisionHandlingSpheresWithSpheres, \
    collidingSpheresWithBoxes, handleSphereBoxCollision
from philipp.YAMLParser import createSpace, createSpheres
from philipp.view import makeBordersVisual


class Space():
    def __init__(self, file = "philipp/Kugeln.yaml", fileSpace = "philipp/Space.yaml"):

        self.width, self.height, self.depth, self.obstacles = createSpace(fileSpace)
        makeBordersVisual(fileSpace, self.height, self.width, self.depth)
        self.spheres= createSpheres(file)

    def simulateStep(self, dt, elasticity):
        spherecollisions = collidingSpheresWithSpheres(self.spheres, dt)
        collisionHandlingSpheresWithSpheres(dt, elasticity, spherecollisions)
        self.collisionWithBorder(elasticity)
        sphereBoxCollisions = collidingSpheresWithBoxes(self.spheres, self.obstacles)
        handleSphereBoxCollision(sphereBoxCollisions, dt)
        self.zeitschritt(dt)

    def collisionWithBorder(self, elasticity):
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
                normalVektor = vector (0,1,0)
                depth = vector(0, (-self.height / 2 + ball.sphere.radius),0) - vector(0, ball.sphere.pos.y,0)
                rueckStellVektor = helper(ball.velocity, normalVektor,depth)
                ball.sphere.pos = ball.sphere.pos + rueckStellVektor
                if not ball.velocity.y > 0:
                    ball.velocity.y = -ball.velocity.y * elasticity
            if not (self.height / 2 - ball.sphere.radius) > ball.sphere.pos.y:
                normalVektor = vector (0,-1,0)
                depth = vector(0, ball.sphere.pos.y,0) - vector(0, (self.height / 2 - ball.sphere.radius),0)
                rueckStellVektor = helper(ball.velocity, normalVektor,depth)
                ball.sphere.pos = ball.sphere.pos + rueckStellVektor
                if not ball.velocity.y < 0:
                    ball.velocity.y = -ball.velocity.y * elasticity

            if not (-self.depth / 2 + ball.sphere.radius) < ball.sphere.pos.z:
                normalVektor = vector (0,0,1)
                depth = vector(0,0 ,(-self.depth / 2 + ball.sphere.radius)) - vector(0,0 ,ball.sphere.pos.z)
                rueckStellVektor = helper(ball.velocity, normalVektor,depth)
                ball.sphere.pos = ball.sphere.pos + rueckStellVektor
                if not ball.velocity.z > 0:
                    ball.velocity.z = -ball.velocity.z * elasticity
            if not (self.depth / 2 - ball.sphere.radius) > ball.sphere.pos.z:
                normalVektor = vector (0,0,-1)
                depth = vector(0, 0, ball.sphere.pos.z) - vector(0, 0, (self.depth / 2 - ball.sphere.radius))
                rueckStellVektor = helper(ball.velocity, normalVektor,depth)
                ball.sphere.pos = ball.sphere.pos + rueckStellVektor
                if not ball.velocity.z < 0:
                    ball.velocity.z = -ball.velocity.z * elasticity

    def zeitschritt(self, dt):
        for ball in self.spheres:
            ball.sphere.pos = ball.sphere.pos + ball.velocity * dt


def helper(vec1, normalVec, depth):
    angle = vec1.diff_angle(normalVec)
    angle = angle - (math.pi/2)
    betragRueckStellVektor = depth.mag
    try:
        betragRueckStellVektor = depth.mag / math.sin(angle)
    except ZeroDivisionError:
        print("false")
    rueckstellvektor = betragRueckStellVektor * -norm(vec1)
    return rueckstellvektor