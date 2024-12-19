import matplotlib.pyplot as plt
import numpy as np

# Parameter definieren
a = 0.6  # Wachstumsrate der Beutetiere
b = 0.02  # Interaktionsrate zwischen Beutetiere und Räuber
c = 0.5  # Sterberate der Räuber
d = 0.01  # Zuwachsrate der Räuber durch Beute
r = 0.3  # Wachstumsrate der Nahrung
k = 0.009  # Konsumrate der Nahrung durch Beutetiere

dt = 0.01  # Zeitschrittgröße
steps = 10000  # Anzahl der Zeitschritte

# Anfangswerte
x = 50  # Anfangspopulation Beutetiere
y = 10  # Anfangspopulation Räuber
z = 60  # Anfangsmenge der Nahrung

# Listen zur Speicherung der Werte
t_values = [0]
x_values = [x]
y_values = [y]
z_values = [z]

# Werte berechnen
for step in range(steps):
    dx = (a * x - b * x * y + k * x * z) * dt
    dy = (-c * y + d * x * y) * dt
    dz = (r * z - k * x * z) * dt

    # Werte aktualisieren und begrenzen
    x = max(0, x + dx)
    y = max(0, y + dy)
    z = max(0, z + dz)

    # Zeit aktualisieren
    t_values.append(t_values[-1] + dt)
    x_values.append(x)
    y_values.append(y)
    z_values.append(z)

# Mittelwerte berechnen
x_mean = np.mean(x_values)
y_mean = np.mean(y_values)

# Plot erstellen
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlabel("Zeit")
ax.set_ylabel("Population / Menge")
ax.set_title("Lotka-Volterra Simulation (statisch)")

# Daten plotten
ax.plot(t_values, x_values, label="Beutetiere (x)", color='blue')
ax.plot(t_values, y_values, label="Räuber (y)", color='red')
ax.plot(t_values, z_values, label="Nahrung (z)", color='green')
ax.axhline(y=x_mean, color='blue', linestyle='--', label="Mittelwert x")
ax.axhline(y=y_mean, color='red', linestyle='--', label="Mittelwert y")

# Mittelwerte als Text anzeigen
ax.text(0.02, 0.95, f"Mittlere x (Beutetiere): {x_mean:.2f}\nMittlere y (Räuber): {y_mean:.2f}",
        transform=ax.transAxes, fontsize=10, verticalalignment='top')

ax.legend()
plt.show()
