import itertools
import yaml
import numpy as np
from multiprocessing import Pool, cpu_count
from Simulation import simulation_durchfuehren

#Diese Klasse nutzt die Simulation.py, um die Simulation der Beute-Räuber-Nahrungsdynamik durchzuführen.
#Die Parameter werden aus einer YAML-Datei und variiert. Mit diesen Variationen wird die Simulation durchgeführt
#und die Ergebnisse werden bewertet. Die beste Parameterkombination wird ausgegeben und kann optional gespeichert werden.

# Funktion zum Lesen der Parameter aus einer YAML-Datei
def lese_parameter(yaml_datei):
    with open(yaml_datei, 'r') as datei:
        parameter = yaml.safe_load(datei)
    return parameter

# Bewertung der Parameterkombination
def bewerte(args):
    #Aufteilen der Argumente
    params, param_keys, zeit_schritt, anzahl_schritte, beute_population, raeuber_population, nahrungs_verfuegbarkeit = args

    # Parameter in Dictionary umwandeln, fuer bessere Uebersicht bei der Ausgabe
    params_dict = dict(zip(param_keys, params))

    # Parameterliste erstellen zur verbesserten Uebersicht
    param_list = list(params_dict.values())

    # Simulation durchfuehren, dafür wird die Funktion simulation_durchfuehren aus Simulation.py verwendet
    _, beute_werte, raeuber_werte, nahrungs_werte = simulation_durchfuehren(
        param_list,
        zeit_schritt,
        anzahl_schritte,
        beute_population,
        raeuber_population,
        nahrungs_verfuegbarkeit
    )

    fitness_beute = berechne_periodenabweichung(beute_werte)
    fitness_raeuber = berechne_periodenabweichung(raeuber_werte)
    fitness_nahrung = berechne_periodenabweichung(nahrungs_werte)
    fitness = (fitness_beute + fitness_raeuber + fitness_nahrung)/3
    return fitness, params_dict

#Berechnet die Standardabweichung der Abstände zwischen Maxima einer Zahlenreihe,
#um die Regelmäßigkeit periodischer Schwankungen zu beurteilen. Eine geringe
#Standardabweichung deutet auf eine stabile Population hin, eine hohe auf ein Aussterben oder eine Ueberpopulation.
def berechne_periodenabweichung(werte):
    maxima = [i for i in range(1, len(werte) - 1) if werte[i - 1] < werte[i] > werte[i + 1]]
    if len(maxima) < 2:
        return float('inf')  # Keine periodischen Schwankungen
    perioden = np.diff([maxima[i] for i in range(len(maxima))])
    return np.std(perioden)  # Standardabweichung der Perioden


def parameter_suche(parameter_datei, grid_dichte=5):
    # Einlesen der YAML-Datei
    with open(parameter_datei, 'r') as datei:
        parameter = yaml.safe_load(datei)

    # Parameter auslesen
    zeit_schritt = parameter['zeit_schritt']
    anzahl_schritte = parameter['anzahl_schritte']
    beute_population = parameter['beute_population']
    raeuber_population = parameter['raeuber_population']
    nahrungs_verfuegbarkeit = parameter['nahrungs_verfuegbarkeit']

    # Erstellen der Parameterbereiche. Originalwert +- 10%
    multipliers = np.linspace(0.9, 1.1, grid_dichte)
    param_keys = [
        'beute_wachstumsrate',
        'raeuber_rate',
        'raeuber_todesrate',
        'raeuber_effizienz',
        'nahrungs_wachstumsrate',
        'nahrungs_verbrauchsrate'
    ]
    # Erstellen der Parameterkombinationen
    parameter_bereiche = {
        key: [parameter[key] * m for m in multipliers]
        for key in param_keys
    }
    parameter_combinations = list(itertools.product(*parameter_bereiche.values()))

    # Ausgabe der Anzahl der Parameterkombinationen als Kontrolle
    print("Number of parameter combinations:", len(parameter_combinations))

    args = [
        (params, param_keys, zeit_schritt, anzahl_schritte, beute_population, raeuber_population, nahrungs_verfuegbarkeit)
        for params in parameter_combinations
    ]

    results = []
    total_combinations = len(args)

    # Multiprocessing Pool erstellen. Die Anzahl der Prozesse entspricht der Anzahl der CPU-Kerne
    with Pool(cpu_count()) as pool:
        for i, result in enumerate(pool.imap(bewerte, args, chunksize=1), start=1):
            results.append(result)
            if i % 100 == 0:
                print(f"Bereits {i} / {total_combinations} verarbeitet...")

    # Beste Parameterkombination finden
    beste_fitness, beste_parameter = min(results, key=lambda x: x[0])

    # Ausgabe der besten Parameterkombination
    print("Beste Parameter:", beste_parameter)
    print("Beste Fitness:", beste_fitness)

    native_beste_parameter = {key: float(value) for key, value in beste_parameter.items()}
    output_data = {
        **native_beste_parameter,  # Add best parameters
        'zeit_schritt': float(zeit_schritt),
        'anzahl_schritte': int(anzahl_schritte),
        'beute_population': float(beute_population),
        'raeuber_population': float(raeuber_population),
        'nahrungs_verfuegbarkeit': float(nahrungs_verfuegbarkeit),
    }

    # Abfrage, ob die Parameter gespeichert werden sollen
    speichern = input("Möchten Sie die besten Parameter in eine neue Datei speichern? (Y/N): ").strip().lower()
    if speichern == 'y':
        dateiname = input("Geben Sie einen Namen für die neue YAML-Datei ein: ").strip()
        if not dateiname.endswith('.yaml'):
            dateiname += '.yaml'
        with open(dateiname, 'w') as neue_datei:
            yaml.dump(output_data, neue_datei)
        print(f"Die besten Parameter wurden in der Datei '{dateiname}' gespeichert.")


if __name__ == "__main__":
    parameter_suche('params.yaml', grid_dichte=3)
