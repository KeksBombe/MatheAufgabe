import math
from itertools import combinations

from vpython import mag, proj, vector, norm


def collidingSpheresWithSpheres(spheres, dt):
    teilmengen = list(combinations(spheres, 2))
    collisions = list()
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
            collisions.append(pair)
    return collisions

def collisionHandlingSpheresWithSpheres(dt, elasticity, sphereCollisions):
    for pair in sphereCollisions:
        ball1 = pair[0]
        ball2 = pair[1]
        pos1 = ball1.sphere.pos + ball1.velocity * dt
        pos2 = ball2.sphere.pos + ball2.velocity * dt
        dif = pos1 - pos2
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


