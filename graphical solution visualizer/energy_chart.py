import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import matplotlib.colors as mcolors
import tkinter
import numpy as np

# Variabile globale per tenere traccia della figura corrente
current_figure = None
current_axes = None
current_canvas = None

def plot_energy_consumption_interactive(solution_file, instance_file, consumption_file, frame):
    global current_figure, current_axes, current_canvas

    # Chiudi la figura precedente se esiste
    if current_figure is not None:
        plt.close(current_figure)
    if current_canvas is not None:
        current_canvas.get_tk_widget().pack_forget()
        current_canvas = None
        current_axes = None

    # Leggi i dati dal file delle soluzioni
    with open(solution_file, 'r') as file:
        solution_data = eval(file.read())

    # Leggi i dati dal file delle istanze
    with open(instance_file, 'r') as file:
        instance_data = file.readlines()

    # Leggi i dati dal file di consumo energetico
    with open(consumption_file, 'r') as file:
        consumption_data = eval(file.read().split(': ')[1])

    # Estrai informazioni dalle istanze
    num_jobs = int(instance_data[0].split(': ')[1])
    processing_times = eval(instance_data[1].split(': ')[1])
    num_machines = int(instance_data[2].split(': ')[1])
    time_horizon = int(instance_data[5].split(': ')[1])
    energy_budget = float(instance_data[4].split(': ')[1])
    energy_panels = eval(instance_data[8].split(': ')[1])
    cost_energy = eval(instance_data[6].split(': ')[1])


    # Creare un DataFrame dai dati della soluzione
    df = pd.DataFrame(solution_data, columns=['Job', 'Machine', 'Start'])

    # Aggiungere una colonna di durata usando i tempi di elaborazione
    df['Duration'] = df['Job'].apply(lambda x: processing_times[x])

    # Calcolare il consumo energetico totale per ogni time slot
    energy_consumption = [0] * (time_horizon)
    for i, row in df.iterrows():
        job = row['Job']
        machine = row['Machine']
        start_time = row['Start']
        duration = processing_times[job]
        for t in range(duration):
            energy_consumption[start_time + t] += consumption_data[job][machine][t]

    # Creare il frame per la lista dei job e il grafico
    check_frame = tkinter.Frame(frame)
    check_frame.pack(side='left', fill='y')

    job_vars = []
    for i in range(num_jobs):
        var = tkinter.IntVar()
        chk = tkinter.Checkbutton(check_frame, text=f'Job {i}', variable=var)
        chk.pack(anchor='w')
        job_vars.append(var)

    def update_plot():
        selected_jobs = [i for i, var in enumerate(job_vars) if var.get() == 1]
        new_solution_data = [row for row in solution_data if row[0] in selected_jobs]
        df = pd.DataFrame(new_solution_data, columns=['Job', 'Machine', 'Start'])
        df['Duration'] = df['Job'].apply(lambda x: processing_times[x])

        new_energy_consumption = [0] * (time_horizon)
        for i, row in df.iterrows():
            job = row['Job']
            machine = row['Machine']
            start_time = row['Start']
            duration = processing_times[job]
            for t in range(duration):
                new_energy_consumption[start_time + t] += consumption_data[job][machine][t]

        current_axes.lines[0].set_ydata(new_energy_consumption)
        current_figure.canvas.draw_idle()

    # Creare il pulsante per aggiornare il grafico
    update_button = tkinter.Frame(check_frame)
    update_button.pack(pady=5)
    btn_update = tkinter.Button(update_button, text="Update", command=update_plot)
    btn_update.pack(side=tkinter.LEFT)

    # Creare un frame per il grafico
    plot_frame = tkinter.Frame(frame)
    plot_frame.pack(side='right', fill='both', expand=True)

    # Creare il grafico del consumo energetico
    fig, ax = plt.subplots(figsize=(10, 6))
    current_figure = fig  # Assegna la figura corrente alla variabile globale
    current_axes = ax

    plt.subplots_adjust(left=0.1, bottom=0.25)

    # Aggiungere il consumo energetico per ogni time slot
    l, = ax.step(range(time_horizon), energy_consumption, label='Energy Consumption', color='blue')

    # Aggiungere il limite di consumo energetico
    ax.axhline(y=energy_budget, color='red', linestyle='--', label='Energy Budget')

    # Aggiungere energia pannelli
    ax.step(range(time_horizon),energy_panels, color='green', linestyle='--', label='Energy Photovoltaic')



    # Impostare le etichette e il titolo
    ax.set_xlim(0, time_horizon - 1)
    ax.set_xlabel('Time Slot')
    ax.set_ylabel('Energy Consumption')
    ax.set_title('Energy Consumption per Time Slot')
    ax.legend()

    # Embeddare il grafico in tkinter usando FigureCanvasTkAgg
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
    current_canvas = canvas

    return canvas