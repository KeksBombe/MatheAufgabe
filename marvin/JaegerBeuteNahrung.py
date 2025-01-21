import numpy as np
import yaml
import matplotlib.pyplot as plt


def simulation_durchfuehren():
    parameter = lese_parameter('params.yaml')

    # Parameter zuweisen
    beute_wachstumsrate = parameter['beute_wachstumsrate']
    raeuber_rate = parameter['raeuber_rate']
    raeuber_todesrate = parameter['raeuber_todesrate']
    raeuber_effizienz = parameter['raeuber_effizienz']
    nahrungs_wachstumsrate = parameter['nahrungs_wachstumsrate']
    nahrungs_verbrauchsrate = parameter['nahrungs_verbrauchsrate']

    zeit_schritt = parameter['zeit_schritt']
    anzahl_schritte = parameter['anzahl_schritte']

    beute_population = parameter['beute_population']
    raeuber_population = parameter['raeuber_population']
    nahrungs_verfuegbarkeit = parameter['nahrungs_verfuegbarkeit']

    zeit_werte = [0]
    beute_werte = [beute_population]
    raeuber_werte = [raeuber_population]
    nahrungs_werte = [nahrungs_verfuegbarkeit]

    # Differentialgleichungen
    def systemgleichungen(zustand):
        beute, raeuber, nahrung = zustand
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
    def runge_kutta_schritt(funktion, aktueller_zustand, t, dt):
        k1 = funktion(aktueller_zustand, t)
        k2 = funktion(aktueller_zustand + 0.5 * dt * k1, t + 0.5 * dt)
        k3 = funktion(aktueller_zustand + 0.5 * dt * k2, t + 0.5 * dt)
        k4 = funktion(aktueller_zustand + dt * k3, t + dt)
        return aktueller_zustand + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

    # Simulation durchführen
    for schritt in range(anzahl_schritte):
        aktueller_zustand = np.array([beute_population, raeuber_population, nahrungs_verfuegbarkeit])
        naechster_zustand = runge_kutta_schritt(systemgleichungen, aktueller_zustand, schritt * zeit_schritt,
                                                zeit_schritt)

        beute_population, raeuber_population, nahrungs_verfuegbarkeit = naechster_zustand

        beute_population = max(0, beute_population)
        raeuber_population = max(0, raeuber_population)
        nahrungs_verfuegbarkeit = max(0, nahrungs_verfuegbarkeit)

        zeit_werte.append(zeit_werte[-1] + zeit_schritt)
        beute_werte.append(beute_population)
        raeuber_werte.append(raeuber_population)
        nahrungs_werte.append(nahrungs_verfuegbarkeit)

    # Mittelwerte berechnen
    beute_mittel = np.mean(beute_werte)
    raeuber_mittel = np.mean(raeuber_werte)
    nahrungs_mittel = np.mean(nahrungs_werte)

    fig, ax = plt.subplots(figsize=(12, 6))

    # Werte als Linien
    ax.plot(zeit_werte, beute_werte, label="Beutetiere", color="blue")
    ax.plot(zeit_werte, raeuber_werte, label="Räuber", color="red")
    ax.plot(zeit_werte, nahrungs_werte, label="Nahrung", color="green")

    # Mittelwerte als gestrichelte Linien
    ax.axhline(beute_mittel, color="blue", linestyle="--", label="Beute Mittelwert")
    ax.axhline(raeuber_mittel, color="red", linestyle="--", label="Räuber Mittelwert")
    ax.axhline(nahrungs_mittel, color="green", linestyle="--", label="Nahrung Mittelwert")

    # Achsenbeschriftungen und Titel
    ax.set_xlabel("Zeit")
    ax.set_ylabel("Population / Menge")
    ax.set_title("Jäger-Beute-System mit Nahrung")
    ax.legend()

    plt.show()

# Funktion zum Lesen der Parameter aus einer YAML-Datei
def lese_parameter(yaml_datei):
    with open(yaml_datei, 'r') as datei:
        parameter = yaml.safe_load(datei)
    return parameter


if __name__ == "__main__":
    simulation_durchfuehren()
