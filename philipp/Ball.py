from vpython import sphere, vector, color

class Ball():
    def __init__(self, radius = 1.0, color = color.blue, position = vector(0.0, 0.0, 0.0), mass = 1.0, velocity = vector(0.0, 0.0, 0.0), acceleration = vector(0.0, 0.0, 0.0)):
        self.sphere = sphere(color = color, radius = radius, pos = position)
        self.mass = mass
        self.velocity = velocity
