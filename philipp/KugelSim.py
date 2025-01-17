from vpython import rate, scene, wtext, slider
from Space import Space


class Simulation():
    def __init__(self, rate = 100, dt = 0.005,elasticity = 0.9, space = Space()):
        self.rate = rate
        self.dt = dt
        self.space = space
        self.elasticity = elasticity

sim = Simulation()

scene.title = 'Simulation'
scene.caption = 'Simulation Speed:'

def manipulateSimulationSpeed(event):
    if event.id  == 'simSpeed':
        sim.rate = event.value
        wt.text = '{:d}'.format(event.value) + ' Simulation Steps per Second'
    if event.id == 'elasticity':
        sim.elasticity = event.value
        vt.text = '{:1.2f}'.format(event.value)


speedSlider = slider(bind=manipulateSimulationSpeed, max = 100, min=1, value = 1000, id = 'simSpeed', step=1)
wt = wtext(text='{:d}'.format(speedSlider.value) + ' Simulation Steps per Second')

scene.append_to_caption('\nElasticity factor:   ')

elasticitySlider = slider(bind=manipulateSimulationSpeed, max = 1, min=0.1, value = 0.9, id = 'elasticity', step=0.05)
vt = wtext(text='{:1.2f}'.format(elasticitySlider.value))

def Simulate():
    while True:
        rate(sim.rate)
        sim.space.simulateStep(sim.dt, sim.elasticity)

if __name__ == '__main__':
    Simulate()