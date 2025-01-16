from vpython import scene, slider, wtext, button

from philipp.Constants import INITIAL_SIM_RATE, INITIAL_ELASTICITY, MAX_SIM_RATE, MIN_SIM_RATE, RATE_STEP_SLIDER, \
    MAX_ELASTICITY, MIN_ELASTICITY, ELASTICITY_STEP_SLIDER


class View():
    def __init__(self, Simulation):
        self.Simulation = Simulation

        # Sliders and Labels
        scene.title = 'Simulation'
        scene.caption = 'Simulation Speed:'
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



