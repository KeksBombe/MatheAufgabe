from vpython import rate
from Space import Space


class Simulation():
    def __init__(self, rate = 100, dt = 0.001, space = Space()):
        self.rate = rate
        self.dt = dt
        self.space = space

sim = Simulation()

def Simulate():
    while True:
        rate(sim.rate)
        #sim.space.simulationStep(sim.dt)
        sim.space.simulateStep(sim.dt)

Simulate()