import math
from datetime import timedelta
from itertools import combinations

from numpy.ma.core import angle
from vpython import mag, proj, vector, norm, sphere, arrow, color, rotate


# Prüft jede Teilmenge der Größe 2 der Menge spheres, ob die beiden Sphären kollidieren.
# Ausgegeben wird die Menge der Kollisionen.
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

# Die Kollisionen der Menge sphereCollisions werden bahandelt.
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

# Überprüft ob die Sphären mit den Boxen kollidieren und gibt alle Sphäre-Box kombinationen zurück, die kollidieren
def collidingSpheresWithBoxes(spheres, boxes):
    collisions = list()
    for ball in spheres:
        for box in boxes:
            if detectSphereBoxCollision(ball.sphere.pos, ball.sphere.radius, box):
                collisions.append([ball, box])
    return collisions

def detectSphereBoxCollision(ballposition, ballradius, box):
    # Relative Position berechnen
    relativePosition = ballposition - box.pos
    # Die Relative Position wird auf die Normalenvektoren der Box projiziert
    yDimension = relativePosition.proj(box.up)
    xDimension = relativePosition.proj(box.axis)
    zDimension = relativePosition.proj(box.axis.cross(box.up))
    # Der Betrag dieser Vektoren bestimmt den (von den Flächen der Box orthogonalen) Abstand vom Kreis Mittelpunkt zum Box Mittelpunkt

    # Distanzen des Mittelpunktes zur Dimensionsgrenze. Wenn der Mittelpunkt innerhalb der Dimensionsgrenze also innerhalb der Breite der Box zum Beispiel liegt
    # dann bleibt die Distanz 0. Wenn nicht dann trägt die Differenz zur Distanz zum Quader bei.
    distanceVector = vector(0, 0, 0)
    if not yDimension.mag < (box.height / 2):
        distanceVector.y = yDimension.mag - box.height / 2
    if not xDimension.mag < (box.length / 2):
        distanceVector.x = xDimension.mag - box.length / 2
    if not zDimension.mag < (box.width / 2):
        distanceVector.z = zDimension.mag - box.width / 2

    # Wenn der Radius der Kugel größer ist als der Betrag des Distanzvektors, kollidiert die Kugel
    return ballradius > distanceVector.mag

def handleSphereBoxCollision(collisions, dt):
    for pair in collisions:
        ball = pair[0]
        box = pair[1]
        timedelta = positionSphereOnCollisionPointWithCuboid(dt, ball, box)
        normalVec = computeCollisionNormalVector(ball, box)
        changeVelocityVectorWithCollisionNormal(ball, normalVec)



# Positions the Sphere where the collision happened and returns the time that was 'reversed' so the Sphere can move on with this time when the velocity was corrected
def positionSphereOnCollisionPointWithCuboid(DT, ball, cuboid):
    lastPositionWithoutCollision = ball.sphere.pos - ball.velocity * DT

    reversedTimeStep = DT
    # halbierter Zeitschritt für "binäre" Suche
    zeitschritt = DT / 2

    for i in range(2, 7):
        partlyReversedPosition = ball.sphere.pos - zeitschritt * ball.velocity
        collisionDetectedAgain = detectSphereBoxCollision(partlyReversedPosition, ball.sphere.radius, cuboid)
        if collisionDetectedAgain:
            zeitschritt = zeitschritt + DT / pow(2, i)
        else:
            reversedTimeStep = zeitschritt
            zeitschritt = zeitschritt - DT / pow(2, i)
            lastPositionWithoutCollision = partlyReversedPosition

    rueckstellVektor = lastPositionWithoutCollision - ball.sphere.pos
    ball.sphere.pos = ball.sphere.pos + rueckstellVektor
    return reversedTimeStep

def computeCollisionNormalVector(ball, box):
    # relative Position
    relativePosition = box.pos - ball.sphere.pos
    yDimension = relativePosition.proj(box.up)
    xDimension = relativePosition.proj(box.axis)
    zDimension = relativePosition.proj(box.axis.cross(box.up))

    normal = vector(0, 0, 0)
    # die könnten alternativ auch auf up axis und das kreuzprodukt projiziert werden
    relLength = rotate(vector(box.length/2, 0,0), angle=box.radRotation, axis=box.rotationAxis)
    relheight = rotate(vector(0, box.height / 2, 0), angle=box.radRotation, axis=box.rotationAxis)
    relWidth = rotate(vector(0,0,box.width/2), angle=box.radRotation, axis=box.rotationAxis)

    if yDimension.mag > box.height/2:
        #ball kann entweder drüber oder drunter sein
        one = yDimension - relheight
        two = yDimension + relheight
        if one.mag < two.mag:
            normal += one
        else:
            normal += two
    if xDimension.mag > box.length/2:
        #ball kann entweder links oder rechts sein
        one = xDimension - relLength
        two = xDimension + relLength
        if one.mag < two.mag:
            normal += one
        else:
            normal += two
    if zDimension.mag > box.width/2:
        #ball kann entweder vorne oder hinten sein
        one = zDimension - relWidth
        two = zDimension + relWidth
        if one.mag < two.mag:
            normal += one
        else:
            normal += two

    return normal

def changeVelocityVectorWithCollisionNormal(ball, collisionNormal):
    velComponentToNormal = ball.velocity.proj(collisionNormal)
    if ball.velocity.diff_angle(collisionNormal) < math.pi / 2:
        ball.velocity = ball.velocity - 2*velComponentToNormal
    arrow(pos=ball.sphere.pos, axis=collisionNormal, color=color.green)