import yaml
from vpython import scene, slider, wtext, button, box, vector, color

from Constants import INITIAL_SIM_RATE, INITIAL_ELASTICITY, MAX_SIM_RATE, MIN_SIM_RATE, RATE_STEP_SLIDER, \
    MAX_ELASTICITY, MIN_ELASTICITY, ELASTICITY_STEP_SLIDER

OPACITY=0.1

class View():
    def __init__(self, Simulation):
        self.Simulation = Simulation

        # Sliders and Labels
        scene.title = 'Simulation'
        scene.caption = 'Simulation Speed:'
        scene.autoscale = False
        speedSlider = slider(bind=self.handleEvent, max=MAX_SIM_RATE, min=MIN_SIM_RATE, value=INITIAL_SIM_RATE, id='simSpeed', step=RATE_STEP_SLIDER)
        self.wt = wtext(text='{:d}'.format(speedSlider.value) + ' Simulation Steps per Second')
        scene.append_to_caption('\nElasticity factor:   ')
        elasticitySlider = slider(bind=self.handleEvent, max=MAX_ELASTICITY, min=MIN_ELASTICITY, value=INITIAL_ELASTICITY, id='elasticity', step=ELASTICITY_STEP_SLIDER)
        self.vt = wtext(text='{:1.2f}'.format(elasticitySlider.value))
        scene.append_to_caption('\n')
        self.pause = button(bind= self.handleEvent, text='pause/resume', id='pause')

    def handleEvent(self, event):
        if event.id  == 'simSpeed':
            self.Simulation.rate = event.value
            self.wt.text = '{:d}'.format(event.value) + ' Simulation Steps per Second'
        if event.id == 'elasticity':
            self.Simulation.elasticity = event.value
            self.vt.text = '{:1.2f}'.format(event.value)
        if event.id == 'pause':
            self.Simulation.paused = not self.Simulation.paused

def makeBordersVisual(file, height, width, depth):
    with open(file, 'r') as space:
        spaceData = yaml.safe_load(space)
    borderSection = spaceData['space']['border']['thickness']
    thickness = borderSection['value']
    if not (borderSection['range'][0] < thickness < borderSection['range'][1]):
        thickness = max(thickness, borderSection['range'][0])
        thickness = min(thickness, borderSection['range'][1])

    if spaceData['space']['border']['visable']:
        wallR = box(pos=vector(width / 2, 0, 0),
                    size=vector(thickness, height - thickness, depth + thickness),
                    color=color.red, opacity=OPACITY)
        wallL = box(pos=vector(-width / 2, 0, 0),
                    size=vector(thickness, height - thickness, depth + thickness),
                    color=color.red,opacity=OPACITY)
        wallB = box(pos=vector(0, -height / 2, 0),
                    size=vector(width + thickness, thickness, depth + thickness),
                    color=color.blue, opacity=OPACITY)
        wallT = box(pos=vector(0, height / 2, 0),
                    size=vector(width - thickness, thickness, depth - thickness),
                    color=color.blue, opacity=OPACITY)
        wallBK = box(pos=vector(0, 0, -depth / 2),
                     size=vector(width - thickness, height - thickness, thickness),
                     color=color.gray(0.7), opacity=OPACITY)



