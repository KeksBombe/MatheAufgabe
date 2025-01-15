import itertools
import yaml
import numpy as np
from multiprocessing import Pool, cpu_count
from autoSim import simulation_durchfuehren, berechne_periodenabweichung

def evaluate(args):
    params, param_keys, zeit_schritt, anzahl_schritte, beute_population, raeuber_population, nahrungs_verfuegbarkeit = args

    params_dict = dict(zip(param_keys, params))

    param_list = list(params_dict.values())

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


def parameter_suche(parameter_datei, grid_density=5):
    with open(parameter_datei, 'r') as datei:
        parameter = yaml.safe_load(datei)

    zeit_schritt = parameter['zeit_schritt']
    anzahl_schritte = parameter['anzahl_schritte']
    beute_population = parameter['beute_population']
    raeuber_population = parameter['raeuber_population']
    nahrungs_verfuegbarkeit = parameter['nahrungs_verfuegbarkeit']

    # Define multipliers and parameter ranges
    multipliers = np.linspace(0.9, 1.1, grid_density)
    param_keys = [
        'beute_wachstumsrate',
        'raeuber_rate',
        'raeuber_todesrate',
        'raeuber_effizienz',
        'nahrungs_wachstumsrate',
        'nahrungs_verbrauchsrate'
    ]
    parameter_bereiche = {
        key: [parameter[key] * m for m in multipliers]
        for key in param_keys
    }

    # Generate all parameter combinations
    parameter_combinations = list(itertools.product(*parameter_bereiche.values()))
    print("Number of parameter combinations:", len(parameter_combinations))

    # Build arguments for parallel execution
    args = [
        (params, param_keys, zeit_schritt, anzahl_schritte, beute_population, raeuber_population, nahrungs_verfuegbarkeit)
        for params in parameter_combinations
    ]

    results = []
    total_combinations = len(args)

    # Use multiprocessing Pool to evaluate combinations
    with Pool(cpu_count()) as pool:
        for i, result in enumerate(pool.imap(evaluate, args, chunksize=1), start=1):
            results.append(result)
            if i % 100 == 0:
                print(f"Processed {i} / {total_combinations} combinations...")

    # Find the best result
    beste_fitness, beste_parameter = min(results, key=lambda x: x[0])

    print("Beste Parameter:", beste_parameter)
    print("Beste Fitness:", beste_fitness)


if __name__ == "__main__":
    parameter_suche('params.yaml', grid_density=10)
