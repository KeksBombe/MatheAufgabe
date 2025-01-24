import numpy as np
import yaml

# Diese Klasse implementiert das Beute-Räuber-Nahrungsdynamik-Modell und führt Simulationen durch.
# Die Simulationen werden durch das Runge-Kutta-Verfahren durchgeführt.

# Differentialgleichungen
def systemgleichungen(zustand, t, parameters):
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



