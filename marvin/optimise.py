import itertools
import yaml
from multiprocessing import Pool, cpu_count
from autoSim import simulation_durchfuehren, berechne_periodenabweichung

parameter_bereiche = {
    'beute_wachstumsrate': [0.48, 0.49, 0.50, 0.51, 0.52],
    'raeuber_rate': [0.018, 0.019, 0.02, 0.021, 0.022],
    'raeuber_todesrate': [0.48, 0.49, 0.50, 0.51, 0.52],
    'raeuber_effizienz': [0.009, 0.0095, 0.01, 0.0105, 0.011],
    'nahrungs_wachstumsrate': [0.4, 0.405, 0.41, 0.415, 0.42],
    'nahrungs_verbrauchsrate': [0.0085, 0.00875, 0.009, 0.00925, 0.0095],
}


def evaluate(args):
    params, zeit_schritt, anzahl_schritte, beute_population, raeuber_population, nahrungs_verfuegbarkeit = args
    params_dict = dict(zip(parameter_bereiche.keys(), params))

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


def parameter_suche(parameter_datei):
    with open(parameter_datei, 'r') as datei:
        parameter = yaml.safe_load(datei)

    zeit_schritt = parameter['zeit_schritt']
    anzahl_schritte = parameter['anzahl_schritte']
    beute_population = parameter['beute_population']
    raeuber_population = parameter['raeuber_population']
    nahrungs_verfuegbarkeit = parameter['nahrungs_verfuegbarkeit']

    # Prepare all combinations
    parameter_combinations = list(itertools.product(*parameter_bereiche.values()))
    print("Number of parameter combinations:", len(parameter_combinations))

    args = [
        (params, zeit_schritt, anzahl_schritte, beute_population, raeuber_population, nahrungs_verfuegbarkeit)
        for params in parameter_combinations
    ]

    results = []
    total_combinations = len(args)

    # Use imap instead of map so we can iterate over results as they arrive
    with Pool(cpu_count()) as pool:
        for i, result in enumerate(pool.imap(evaluate, args, chunksize=1), start=1):
            results.append(result)
            # Print a progress message every 100 combinations (adjust as needed)
            if i % 100 == 0:
                print(f"Processed {i} / {total_combinations} combinations...")

    # After collecting all results, find the best parameter set
    beste_fitness, beste_parameter = min(results, key=lambda x: x[0])

    print("Beste Parameter:", beste_parameter)
    print("Beste Fitness:", beste_fitness)


if __name__ == "__main__":
    parameter_suche('params.yaml')
