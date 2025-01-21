import logging
import yaml
from vpython import vector, box
from philipp.Ball import Ball

def createSpace(file):
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='simulation.log', encoding='utf-8', level=logging.WARNING)
    with open(file, 'r') as space:
        spaceData = yaml.safe_load(space)

    dimensionSpace = createVectorFromArray(spaceData['space']['dimensions']['value'])

    obstacles = set()

    for name, obstacle in spaceData['space']['obstacles']['cuboid'].items():
        position = createVectorFromArray(obstacle['position']['value'])
        dimension = createVectorFromArray(obstacle['dimensions']['value'])
        rotationAxis = createVectorFromArray(obstacle['rotationAxis']['value'])
        radRotation = obstacle['rotationInRad']['value']
        b = box(pos=position, size=dimension)
        b.rotate(axis=rotationAxis, angle=radRotation)
        obstacles.add(b)
        b.rotationAxis= rotationAxis
        b.radRotation = radRotation

    return dimensionSpace.x, dimensionSpace.z, dimensionSpace.y, obstacles

def createSpheres(file):
    with open(file, 'r') as f:
        data = yaml.safe_load(f)
    spheres = set()
    # Erstelle die Bälle
    for ball_name, ball_data in data['spheres'].items():
        radius = ball_data['radius']
        radius = max(min(radius['value'], radius['range'][1]), radius['range'][0])
        velocity = createVectorFromArray(ball_data['velocity'])
        position = createVectorFromArray(ball_data['position'])
        farbe = ball_data['color']
        mass = ball_data['mass']
        spheres.add(Ball(radius=radius, position=position, velocity=velocity,
                                   color=vector(farbe[0], farbe[1], farbe[2]),
                                   mass=mass))
    return spheres

# Array muss die Größe 3 haben
def createVectorFromArray(array):
    return vector(array[0], array[1], array[2])
