from vpython import rate, scene, wtext, slider
from Space import Space


class Simulation():
    def __init__(self, rate = 100, dt = 0.001, space = Space()):
        self.rate = rate
        self.dt = dt
        self.space = space

sim = Simulation()

scene.title = 'Simulation'
scene.caption = 'Simulation Speed:'

def manipulateSimulationSpeed(event):
    if event.id  == 'simSpeed':
        sim.rate = event.value
        wt.text = '{:d}'.format(event.value) + ' Simulation Steps per Second'

speedSlider = slider(bind=manipulateSimulationSpeed, max = 5000, min=1, value = 1000, id = 'simSpeed', step=1)
wt = wtext(text='{:d}'.format(speedSlider.value) + ' Simulation Steps per Second')

def Simulate():
    while True:
        rate(sim.rate)
        sim.space.simulateStep(sim.dt)

Simulate()