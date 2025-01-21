import numpy as np
import yaml

## Die autoSim ist von der Logik identisch mit der JaegerBeuteNahrung.py, jedoch besitzt diese keine Ausgabe, sondern
## ist für evaluierungszwecke gedacht. Deswegen enthaelt sie anstatt grafischer Ausgabe eine Methode zur Berechnung von
## Periodenabweichungen. Diese wird in der optimise.py verwendet, um die Fitness der Parameterkombinationen zu bewerten.
## Aufgrund des Multi-Threading ist diese SImulation vom Aufbau her etwas anders. Die Mathematik ist jedoch identisch.

# Funktion zum Lesen der Parameter aus einer YAML-Datei
def lese_parameter(yaml_datei):
    with open(yaml_datei, 'r') as datei:
        parameter = yaml.safe_load(datei)
    return parameter

# Differentialgleichungen
def systemgleichungen(zustand, parameters):
    beute, raeuber, nahrung = zustand
    beute_wachstumsrate, raeuber_rate, raeuber_todesrate, raeuber_effizienz, nahrungs_wachstumsrate, nahrungs_verbrauchsrate = parameters
    d_beute = (beute_wachstumsrate * beute
               - raeuber_rate * beute * raeuber
               + nahrungs_verbrauchsrate * beute * nahrung)
    d_raeuber = (-raeuber_todesrate * raeuber
                 + raeuber_effizienz * beute * raeuber)
    d_nahrung = (nahrungs_wachstumsrate * nahrung
                 - nahrungs_verbrauchsrate * beute * nahrung)
    return np.array([d_beute, d_raeuber, d_nahrung], dtype=float)


# Runge-Kutta-Verfahren
# https://de.wikipedia.org/wiki/Runge-Kutta-Verfahren
def runge_kutta_schritt(funktion, aktueller_zustand, t, dt, params):
    k1 = funktion(aktueller_zustand, t, params)
    k2 = funktion(aktueller_zustand + 0.5 * dt * k1, t + 0.5 * dt, params)
    k3 = funktion(aktueller_zustand + 0.5 * dt * k2, t + 0.5 * dt, params)
    k4 = funktion(aktueller_zustand + dt * k3, t + dt, params)
    return aktueller_zustand + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)


# Simulation durchführen mit uebergebenen Parametern
def simulation_durchfuehren(params, zeit_schritt, anzahl_schritte, beute_population, raeuber_population,
                            nahrungs_verfuegbarkeit):
    zeit_werte = [0]
    beute_werte = [beute_population]
    raeuber_werte = [raeuber_population]
    nahrungs_werte = [nahrungs_verfuegbarkeit]

    aktueller_zustand = np.array([beute_population, raeuber_population, nahrungs_verfuegbarkeit])

    for schritt in range(anzahl_schritte):
        naechster_zustand = runge_kutta_schritt(systemgleichungen, aktueller_zustand, schritt * zeit_schritt,
                                                zeit_schritt, params)
        aktueller_zustand = np.maximum(0, naechster_zustand)  # Negative Werte vermeiden

        zeit_werte.append(zeit_werte[-1] + zeit_schritt)
        beute_werte.append(aktueller_zustand[0])
        raeuber_werte.append(aktueller_zustand[1])
        nahrungs_werte.append(aktueller_zustand[2])

    return zeit_werte, beute_werte, raeuber_werte, nahrungs_werte


#Berechnet die Standardabweichung der Abstände zwischen Maxima einer Zahlenreihe,
#um die Regelmäßigkeit periodischer Schwankungen zu beurteilen. Eine geringe
#Standardabweichung deutet auf eine stabile Population hin, eine hohe auf ein Aussterben oder eine Ueberpopulation.
def berechne_periodenabweichung(werte):
    maxima = [i for i in range(1, len(werte) - 1) if werte[i - 1] < werte[i] > werte[i + 1]]
    if len(maxima) < 2:
        return float('inf')  # Keine periodischen Schwankungen
    perioden = np.diff([maxima[i] for i in range(len(maxima))])
    return np.std(perioden)  # Standardabweichung der Perioden


if __name__ == "__main__":
    parameter = lese_parameter('marvin/params.yaml')
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

    zeit, beute, raeuber, nahrung = simulation_durchfuehren(params, zeit_schritt, anzahl_schritte, beute_population,
                                                            raeuber_population, nahrungs_verfuegbarkeit)
    abweichung = berechne_periodenabweichung(beute)
    print(f"Periodenabweichung: {abweichung}")
