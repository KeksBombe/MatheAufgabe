from vpython import rate

from philipp.Constants import INITIAL_SIM_RATE, INITIAL_ELASTICITY
from philipp.Space import Space
from philipp.view import View


class Simulation():
    def __init__(self, rate = INITIAL_SIM_RATE, dt = 0.005,elasticity = INITIAL_ELASTICITY, space = Space()):
        self.rate = rate
        self.dt = dt
        self.space = space
        self.elasticity = elasticity
    def Simulate(self):
        while True:
            rate(self.rate)
            self.space.simulateStep(self.dt, self.elasticity)

def start():
    sim = Simulation()
    View(sim)
    sim.Simulate()

if __name__ == '__main__':
    sim = Simulation()
    gui = View(sim)
    sim.Simulate()