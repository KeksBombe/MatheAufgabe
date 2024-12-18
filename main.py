import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# Parameter definieren
a = 0.6  # Wachstumsrate der Beutetiere
b = 0.02  # Interaktionsrate zwischen Beutetiere und Räuber
c = 0.5  # Sterberate der Räuber
d = 0.01  # Zuwachsrate der Räuber durch Beute
r = 0.3  # Wachstumsrate der Nahrung
k = 0.009  # Konsumrate der Nahrung durch Beutetiere

# Anfangswerte
x = 50  # Anfangspopulation Beutetiere
y = 10  # Anfangspopulation Räuber
z = 60  # Anfangsmenge der Nahrung
dt = 0.01  # Zeitschrittgröße

# Listen zur Speicherung der Werte
t_values = [0]
x_values = [x]
y_values = [y]
z_values = [z]

x_last50 = [x]  # Letzte 50 Beutetiere-Werte
y_last50 = [y]  # Letzte 50 Räuber-Werte


# Live-Simulation: Die Gleichungen berechnen
def update(frame):
    global x, y, z, t_values, x_values, y_values, z_values
    # Differentialgleichungen anwenden
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

    x_last50.append(x)
    y_last50.append(y)

    x_mean = np.mean(x_last50)
    y_mean = np.mean(y_last50)

    # X-Achse verschieben und Y-Achse automatisch skalieren
    ax.set_xlim(t_values[-1] - 50, t_values[-1] + 10)  # Verschiebende X-Achse
    ax.set_ylim(0, max(max(x_values), max(y_values), max(z_values)) + 10)  # Dynamische Y-Achse

    # Graphen aktualisieren
    line_x.set_data(t_values, x_values)
    line_y.set_data(t_values, y_values)
    line_z.set_data(t_values, z_values)
    line_x_avg.set_ydata([x_mean, x_mean])
    line_y_avg.set_ydata([y_mean, y_mean])

    mean_text.set_text(f"Mittlere x (Beutetiere): {x_mean:.2f}\nMittlere y (Räuber): {y_mean:.2f}")

    return line_x, line_y, line_z, line_x_avg, line_y_avg, mean_text


# Plot einrichten
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlabel("Zeit")
ax.set_ylabel("Population / Menge")
ax.set_title("Live Lotka-Volterra Simulation mit automatischer Skalierung")

# Linien für die Live-Daten
line_x, = ax.plot([], [], label="Beutetiere (x)", color='blue')
line_y, = ax.plot([], [], label="Räuber (y)", color='red')
line_z, = ax.plot([], [], label="Nahrung (z)", color='green')
line_x_avg = ax.axhline(y=0, color='blue', linestyle='--', label="Mittelwert x")
line_y_avg = ax.axhline(y=0, color='red', linestyle='--', label="Mittelwert y")
mean_text = ax.text(0.02, 0.95, "", transform=ax.transAxes, fontsize=10, verticalalignment='top')

ax.legend()

# Animation starten
ani = FuncAnimation(fig, update, frames=10000, interval=1, blit=True)
plt.show()
