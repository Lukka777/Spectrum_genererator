import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # Встановлюємо інтерактивний бекенд
import matplotlib.pyplot as plt
import json


def calc_spectrum():
    lines, background_params, energy_range, channels, offset, a0, a1 = load_json()

    def find_nearest(array, value):
        idx = (np.abs(array - value)).argmin()
        return idx

    energy = np.linspace(energy_range[0], energy_range[1], channels) + offset

    def generate_spectrum(lines):
        spectrum = np.zeros_like(energy)
        for i in lines:
            e_center, intensity, width = i
            idx_chanel = find_nearest(energy, e_center)
            spectrum[idx_chanel] = intensity
        return spectrum

    def generate_spectrum_w(lines):
        spectrum = np.zeros_like(energy)
        for line in lines:
            e_center, intensity, width = line
            spectrum += intensity * np.exp(-((energy - e_center) ** 2) / (2 * width ** 2))
        return spectrum

    def generate_background(background_params):
        a1, a2, b1, b2 = background_params
        return a1 * np.exp(-a2 * energy) + b1 * energy + b2

    def add_statistical_fluctuations(spectrum):
        noisy_spectrum = np.zeros_like(spectrum)
        for i, count in enumerate(spectrum):
            if count > 0:
                if count < 10:
                    noisy_spectrum[i] = np.random.poisson(count)
                else:
                    noisy_spectrum[i] = max(0, int(np.random.normal(count, np.sqrt(count))))
            else:
                noisy_spectrum[i] = 0
        return noisy_spectrum

    a = generate_spectrum(lines)
    b = generate_background(background_params)
    b[b < 0] = 0
    c = generate_spectrum_w(lines)
    d = add_statistical_fluctuations(b + c)

    return energy, a, b, c, d


def load_json():
    input_file = "data.json"
    with open(input_file, "r") as f:
        data = json.load(f)

    lines = np.array(data["lines"])
    background_params = np.array(data["background_params"])
    energy_range = np.array(data["energy_range"])
    channels = data["channels"]
    offset = data["offset"]
    a0 = data["a0"]
    a1 = data["a1"]

    return lines, background_params, energy_range, channels, offset, a0, a1


def list_to_numpy(energy_lines):
    rows = energy_lines.strip(';').split(';')
    rows = [row.strip().split(',') for row in rows]
    array = np.array(rows, dtype=float)
    return array


def str_to_array(csv):
    data = csv.strip().split(',')
    array = np.array(data, dtype=float)
    return array


def write_to_json(energy_lines, background_params, energy_range, channels, offset, a0, a1):
    lines = list_to_numpy(energy_lines).tolist()
    background_params = str_to_array(background_params).tolist()
    energy_range = str_to_array(energy_range).tolist()

    data = {
        "lines": lines,
        "background_params": background_params,
        "energy_range": energy_range,
        "channels": channels,
        "offset": offset,
        "a0": a0,
        "a1": a1,
    }

    output_file = "data.json"
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)


def save_simulated_spectrum():
    try:
        energy, a, b, c, d = calc_spectrum()

        data = {
            "energy": energy.tolist(),
            "line_spectrum": a.tolist(),
            "line_spectrum+background": (a + b).tolist(),
            "gauss_spectrum+background": (c + b).tolist(),
            "all_in_one": d.tolist()
        }

        output_filename = "simulated_spectrum_output.npy"
        np.save(output_filename, data)

        print(f"Симульований спектр успішно збережено у файл: {output_filename}")
    except Exception as e:
        print(f"Помилка під час збереження симульованого спектру: {e}")


def display_plots():
    en, a, b, c, d = calc_spectrum()

    plt.figure(figsize=(10, 5))
    plt.plot(en, a, label='line_spectrum')
    plt.plot(en, a + b, label='line_spectrum+background')
    plt.plot(en, c + b, label='gauss_spectrum+background')
    plt.plot(en, d, label='all in one')

    plt.legend()
    plt.grid(True)
    plt.show()
    plt.savefig('img.png')

    data = np.vstack((en, a, a + b, c + b, d)).T
    np.savetxt("output.csv", data, delimiter=",")


def save_and_simulate():
    try:
        energy_lines = energy_lines_entry.get()
        background_params = background_params_entry.get()
        energy_range = energy_range_entry.get()
        channels = int(channels_entry.get())
        offset = float(offset_entry.get())
        a0 = float(a0_entry.get())
        a1 = float(a1_entry.get())

        write_to_json(energy_lines, background_params, energy_range, channels, offset, a0, a1)
        display_plots()
        save_simulated_spectrum()

        messagebox.showinfo("Успіх", "Симуляція успішно завершена та збережена!")
    except Exception as e:
        messagebox.showerror("Помилка", f"Сталася помилка: {str(e)}")


def default_simulation():
    try:
        # Використовуємо функцію calc_spectrum для обчислення спектру на основі даних з data.json
        energy, a, b, c, d = calc_spectrum()

        # Відображення графіків та збереження результатів
        plt.figure(figsize=(10, 5))
        plt.plot(energy, a, label='line_spectrum')
        plt.plot(energy, a + b, label='line_spectrum+background')
        plt.plot(energy, c + b, label='gauss_spectrum+background')
        plt.plot(energy, d, label='all in one')

        plt.legend()
        plt.grid(True)
        plt.show()
        plt.savefig('img.png')

        data = np.vstack((energy, a, a + b, c + b, d)).T
        np.savetxt("default_simulation_output.csv", data, delimiter=",")

        messagebox.showinfo("Успіх", "Симуляція за замовчуванням успішно завершена!")
    except Exception as e:
        messagebox.showerror("Помилка", f"Сталася помилка: {str(e)}")


# Графічний інтерфейс
root = tk.Tk()
root.title("Введення параметрів для симуляції")

tk.Label(root, text="Енергетичні лінії").grid(row=0, column=0)
energy_lines_entry = tk.Entry(root, width=50)
energy_lines_entry.grid(row=0, column=1)

tk.Label(root, text="Параметри фону").grid(row=1, column=0)
background_params_entry = tk.Entry(root, width=50)
background_params_entry.grid(row=1, column=1)

tk.Label(root, text="Енергетичний діапазон").grid(row=2, column=0)
energy_range_entry = tk.Entry(root, width=50)
energy_range_entry.grid(row=2, column=1)

tk.Label(root, text="Кількість каналів").grid(row=3, column=0)
channels_entry = tk.Entry(root, width=50)
channels_entry.grid(row=3, column=1)

tk.Label(root, text="Початковий зсув").grid(row=4, column=0)
offset_entry = tk.Entry(root, width=50)
offset_entry.grid(row=4, column=1)

tk.Label(root, text="a0 (уширення)").grid(row=5, column=0)
a0_entry = tk.Entry(root, width=50)
a0_entry.grid(row=5, column=1)

tk.Label(root, text="a1 (уширення)").grid(row=6, column=0)
a1_entry = tk.Entry(root, width=50)
a1_entry.grid(row=6, column=1)

tk.Button(root, text="Зберегти параметри та запустити симуляцію", command=save_and_simulate).grid(row=7, columnspan=2, pady=10)

# Додаємо кнопку для симуляції за замовчуванням
tk.Button(root, text="Симуляція за замовчуванням", command=default_simulation).grid(row=8, columnspan=2, pady=10)

root.mainloop()
