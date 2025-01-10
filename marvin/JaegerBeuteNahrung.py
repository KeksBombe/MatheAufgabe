import numpy as np
import yaml
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def run_simulation():
    params = read_params('marvin/params.yaml')

    # Extract parameters
    prey_growth_rate = params['beute_wachstumsrate']
    predation_rate = params['raeuber_rate']
    predator_death_rate = params['raeuber_todesrate']
    predator_efficiency = params['raeuber_effizienz']
    food_growth_rate = params['nahrungs_wachstumsrate']
    food_consumption_rate = params['nahrungs_verbrauchsrate']

    # -- Zeitsettings --
    time_step = params['zeit_schritt']
    num_steps = params['anzahl_schritte']

    # -- Anfangswerte --
    prey_population = params['beute_population']
    predator_population = params['raeuber_population']
    food_availability = params['nahrungs_verfuegbarkeit']

    # -- Listen zur Speicherung --
    time_values = [0]
    prey_values = [prey_population]
    predator_values = [predator_population]
    food_values = [food_availability]

    # -- Definiere Systemgleichungen (dPrey, dPredator, dFood) --
    def system_odes(state, t):
        prey, predator, food = state
        d_pre = (prey_growth_rate * prey
                 - predation_rate * prey * predator
                 + food_consumption_rate * prey * food)
        d_pred = (-predator_death_rate * predator
                  + predator_efficiency * prey * predator)
        d_food = (food_growth_rate * food
                  - food_consumption_rate * prey * food)
        return np.array([d_pre, d_pred, d_food], dtype=float)

    # -- 4th Order Runge-Kutta (Kutter) Methode --
    def runge_kutta_step(func, current_state, t, dt):
        k1 = func(current_state, t)
        k2 = func(current_state + 0.5 * dt * k1, t + 0.5 * dt)
        k3 = func(current_state + 0.5 * dt * k2, t + 0.5 * dt)
        k4 = func(current_state + dt * k3, t + dt)
        return current_state + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

    # -- Vorbereiten der Figure --
    fig, ax = plt.subplots(figsize=(12, 6))
    line_prey, = ax.plot([], [], label="Beutetiere (Prey)", color="blue")
    line_predator, = ax.plot([], [], label="Raeuber (Predators)", color="red")
    line_food, = ax.plot([], [], label="Nahrung (Food)", color="green")

    # -- Update-Funktion fuer das Animation-Framework --
    def update(frame):
        nonlocal prey_population, predator_population, food_availability

        # Runge-Kutta Schritt durchfuehren
        current_state = np.array([prey_population, predator_population, food_availability])
        next_state = runge_kutta_step(system_odes, current_state, frame * time_step, time_step)

        # aktualisieren
        prey_population, predator_population, food_availability = next_state

        prey_population = max(0, prey_population)
        predator_population = max(0, predator_population)
        food_availability = max(0, food_availability)

        time_values.append(time_values[-1] + time_step)
        prey_values.append(prey_population)
        predator_values.append(predator_population)
        food_values.append(food_availability)

        # Daten anpassen
        line_prey.set_data(time_values, prey_values)
        line_predator.set_data(time_values, predator_values)
        line_food.set_data(time_values, food_values)

        # Hier wird das neu skaliert:
        ax.relim()
        ax.autoscale_view()

        return line_prey, line_predator, line_food

    # -- Legend und Titel --
    ax.set_xlabel("Zeit")
    ax.set_ylabel("Population / Menge")
    ax.set_title("Korrigiertes Jaeger-Beute-System mit Nahrung (Runge-Kutta Live)")
    ax.legend()

    # -- Erstellen der Animation --
    # Wichtig: blit=False, damit die Achsen sauber updaten können!
    ani = animation.FuncAnimation(fig, update, frames=num_steps,
                                  interval=1, blit=False, repeat=False)

    plt.show()

    # -- Mittelwerte nach Abschluss (fuer Interessierte) --
    mean_prey_population = np.mean(prey_values)
    mean_predator_population = np.mean(predator_values)
    mean_food_availability = np.mean(food_values)
    print("Durchschnitt Beute (Prey):", mean_prey_population)
    print("Durchschnitt Raeuber (Predators):", mean_predator_population)
    print("Durchschnitt Nahrung (Food):", mean_food_availability)

def read_params(yaml_file):
    with open(yaml_file, 'r') as file:
        params = yaml.safe_load(file)
    return params

if __name__ == "__main__":
    run_simulation()
