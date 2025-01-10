from marvin import JaegerBeuteNahrung
from philipp import KugelSim
import tkinter as tk
from tkinter import messagebox


def start_kugel_simulation():
    root.quit()
    root.destroy()
    KugelSim.Simulate()
    


def start_jaeger_beute_simulation():
    root.quit()
    root.destroy()
    JaegerBeuteNahrung.run_simulation()

if __name__ == "__main__":
    # Hauptfenster erstellen
    root = tk.Tk()
    root.title("Mathe Simulation")
    root.geometry("400x200")

    # Titel Label
    label = tk.Label(root, text="Mathe Simulation", font=("Arial", 16))
    label.pack(pady=20)

    # Buttons erstellen
    button_kugel = tk.Button(root, text="Kugel Kollision", font=("Arial", 12), command=start_kugel_simulation)
    button_kugel.pack(pady=10)

    button_jaeger_beute = tk.Button(root, text="Jäger Beute System", font=("Arial", 12),
                                    command=start_jaeger_beute_simulation)
    button_jaeger_beute.pack(pady=10)

    # Fenster starten
    root.mainloop()