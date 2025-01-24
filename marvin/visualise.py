import matplotlib.pyplot as plt
import yaml
from Simulation import simulation_durchfuehren

#Diese Klasse nutzt die Simulation.py, um die Simulation der Beute-Räuber-Nahrungsdynamik durchzuführen.
#Die Parameter werden aus einer YAML-Datei gelesen und die Ergebnisse werden visualisiert.

def lese_parameter(datei_name):
    with open(datei_name, 'r') as datei:
        parameter = yaml.safe_load(datei)
    return parameter

def plot_simulation(zeit_werte, beute_werte, raeuber_werte, nahrungs_werte):
    plt.figure(figsize=(12, 6))

    plt.plot(zeit_werte, beute_werte, label='Beutepopulation', linestyle='-', marker='')
    plt.plot(zeit_werte, raeuber_werte, label='Räuberpopulation', linestyle='-', marker='')
    plt.plot(zeit_werte, nahrungs_werte, label='Nahrungsverfügbarkeit', linestyle='-', marker='')

    plt.title('Simulation der Beute-Räuber-Nahrungsdynamik')
    plt.xlabel('Zeit')
    plt.ylabel('Population/Verfügbarkeit')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    # Parameter aus der YAML-Datei lesen
    parameter = lese_parameter('params.yaml')

    # Parameter zuweisen
    params = [
        parameter['beute_wachstumsrate'],
        parameter['raeuber_rate'],
        parameter['raeuber_todesrate'],
        parameter['raeuber_effizienz'],
        parameter['nahrungs_wachstumsrate'],
        parameter['nahrungs_verbrauchsrate']
    ]
    zeit_schritt = parameter['zeit_schritt']
    anzahl_schritte = parameter['anzahl_schritte']
    beute_population = parameter['beute_population']
    raeuber_population = parameter['raeuber_population']
    nahrungs_verfuegbarkeit = parameter['nahrungs_verfuegbarkeit']

    # Simulation durchführen
    zeit_werte, beute_werte, raeuber_werte, nahrungs_werte = simulation_durchfuehren(
        params, zeit_schritt, anzahl_schritte, beute_population, raeuber_population, nahrungs_verfuegbarkeit
    )

    # Ergebnisse visualisieren
    plot_simulation(zeit_werte, beute_werte, raeuber_werte, nahrungs_werte)