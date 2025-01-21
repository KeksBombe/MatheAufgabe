import itertools
import yaml
import numpy as np
from multiprocessing import Pool, cpu_count
from autoSim import simulation_durchfuehren, berechne_periodenabweichung

# Bewertung der Parameterkombination
def bewerte(args):
    #Aufteilen der Argumente
    params, param_keys, zeit_schritt, anzahl_schritte, beute_population, raeuber_population, nahrungs_verfuegbarkeit = args

    # Parameter in Dictionary umwandeln, fuer bessere Uebersicht bei der Ausgabe
    params_dict = dict(zip(param_keys, params))

    # Parameterliste erstellen zur verbesserten Uebersicht
    param_list = list(params_dict.values())

    # Simulation durchfuehren, dafür wird die Funktion simulation_durchfuehren aus autoSim.py verwendet
    _, beute_werte, _, _ = simulation_durchfuehren(
        param_list,
        zeit_schritt,
        anzahl_schritte,
        beute_population,
        raeuber_population,
        nahrungs_verfuegbarkeit
    )

    fitness = berechne_periodenabweichung(beute_werte)
    return fitness, params_dict


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


if __name__ == "__main__":
    parameter_suche('params.yaml', grid_density=10)
