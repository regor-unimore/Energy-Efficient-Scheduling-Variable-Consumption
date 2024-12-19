import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from gantt_chart import plot_gantt_chart
from energy_chart import plot_energy_consumption_interactive
import matplotlib.pyplot as plt

import io
import sys
import re
import os

solution_file = None
instance_file = None
consumption_file = None
gantt_canvas = None
energy_canvas = None
entry_solution = None
entry_instance = None
entry_consumption = None
lbl_solution_status = None
lbl_instance_status = None
lbl_consumption_status = None
code_output = None
tab_control = None
tab_energy = None
instance_number = None

def load_file(file_type, entry_widget):
    file_path = filedialog.askopenfilename(title=f'Select {file_type} file')
    if file_path:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, file_path)
    return file_path

def select_solution_file():
    global solution_file
    solution_file = load_file('solution', entry_solution)
    update_file_status('solution')

def select_instance_file():
    global instance_file
    instance_file = load_file('instance', entry_instance)
    update_file_status('instance')

def select_consumption_file():
    global consumption_file
    consumption_file = load_file('consumption', entry_consumption)
    update_file_status('consumption')

def update_file_status(file_type):
    if file_type == 'solution':
        if solution_file:
            lbl_solution_status.config(text="Solution File Loaded", fg="green")
        else:
            lbl_solution_status.config(text="Failed to Load Solution File", fg="red")
    elif file_type == 'instance':
        if instance_file:
            lbl_instance_status.config(text="Instance File Loaded", fg="green")
        else:
            lbl_instance_status.config(text="Failed to Load Instance File", fg="red")
    elif file_type == 'consumption':
        if consumption_file:
            lbl_consumption_status.config(text="Consumption File Loaded", fg="green")
        else:
            lbl_consumption_status.config(text="Failed to Load Consumption File", fg="red")

def update_file_path(file_type, *args):
    global solution_file, instance_file, consumption_file
    if file_type == 'solution':
        solution_file = entry_solution.get()
    elif file_type == 'instance':
        instance_file = entry_instance.get()
    elif file_type == 'consumption':
        consumption_file = entry_consumption.get()
    update_file_status(file_type)

def visualize_gantt_chart(tab):
    global gantt_canvas
    if gantt_canvas:
        gantt_canvas.get_tk_widget().pack_forget()
    gantt_canvas = None

    if solution_file and instance_file and consumption_file:
        fig = plot_gantt_chart(solution_file, instance_file, consumption_file)
        gantt_canvas = FigureCanvasTkAgg(fig, master=tab)
        gantt_canvas.draw()
        gantt_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    else:
        print("Please select solution, instance, and consumption files")

def visualize_energy_consumption_interactive(tab):
    global energy_canvas
    if energy_canvas:
        energy_canvas.get_tk_widget().pack_forget()
    energy_canvas = None

    if solution_file and instance_file and consumption_file:
        energy_canvas = plot_energy_consumption_interactive(solution_file, instance_file, consumption_file, tab)
    else:
        print("Please select solution, instance, and consumption files")

def execute_python_code():
    if solution_file and instance_file and consumption_file:
        code = """code_to_execute(solution_file,instance_file,consumption_file)"""
        old_stdout = sys.stdout
        redirected_output = sys.stdout = io.StringIO()

        try:
            exec(code)
            output = redirected_output.getvalue()
        except Exception as e:
            output = str(e)
        finally:
            sys.stdout = old_stdout

        code_output.delete("1.0", tk.END)
        code_output.insert(tk.END, output)
    else:
        print("Please select solution, instance, and consumption files")


def reset_all(root):
    global solution_file, instance_file, consumption_file, gantt_canvas, energy_canvas
    global entry_solution, entry_instance, entry_consumption
    global lbl_solution_status, lbl_instance_status, lbl_consumption_status
    global code_output, tab_control, tab_energy

    # Non resettiamo i file paths e i campi di input per mantenere i nomi dei file
    # solution_file = None
    # instance_file = None
    # consumption_file = None

    # Reset status labels
    lbl_solution_status.config(text="No Solution File Loaded", fg="red")
    lbl_instance_status.config(text="No Instance File Loaded", fg="red")
    lbl_consumption_status.config(text="No Consumption File Loaded", fg="red")

    # Clear code output
    code_output.delete("1.0", tk.END)

    # Reset charts
    if gantt_canvas:
        gantt_canvas.get_tk_widget().pack_forget()
        gantt_canvas = None

    if energy_canvas:
        energy_canvas.get_tk_widget().pack_forget()
        energy_canvas = None

        # Trova e distruggi tutti i widget nel frame dell'energia
        for widget in tab_energy.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    child.destroy()
                widget.destroy()
            else:
                widget.destroy()

        # Ricrea il bottone di visualizzazione
        btn_visualize_energy = tk.Button(tab_energy, text='Visualize Interactive Energy Consumption',
                                         command=lambda: visualize_energy_consumption_interactive(tab_energy))
        btn_visualize_energy.pack(pady=20)

    # Close all matplotlib figures
    plt.close('all')

    # Reset notebook to first tab
    tab_control.select(0)

    # Dopo il reset, se i percorsi dei file sono ancora presenti, aggiorniamo gli status
    if entry_solution.get():
        lbl_solution_status.config(text="Solution File Loaded", fg="green")
    if entry_instance.get():
        lbl_instance_status.config(text="Instance File Loaded", fg="green")
    if entry_consumption.get():
        lbl_consumption_status.config(text="Consumption File Loaded", fg="green")


def update_file_paths(*args):
    if not instance_number:
        return

    try:
        new_number = int(instance_number.get())

        # Aggiorna i path dei file se esistono
        for entry, file_type in [(entry_solution, 'solution'),
                                 (entry_instance, 'instance'),
                                 (entry_consumption, 'consumption')]:
            current_path = entry.get()
            if current_path:
                # Estrai il nome del file dal path completo
                directory, filename = os.path.split(current_path)
                # Trova il numero nell'attuale nome del file
                match = re.search(r'\d+', filename)
                if match:
                    # Sostituisci il numero trovato con il nuovo numero
                    new_filename = filename[:match.start()] + str(new_number) + filename[match.end():]
                    new_path = os.path.join(directory, new_filename)
                    entry.delete(0, tk.END)
                    entry.insert(0, new_path)
                    update_file_path(file_type)
    except ValueError:
        print("Please enter a valid number")


def create_instance_number_input(root):
    global instance_number

    # Frame per l'input del numero dell'istanza
    frame_instance_number = tk.Frame(root)
    frame_instance_number.pack(pady=5, fill=tk.X, padx=10)

    # Label per l'input
    lbl_instance_number = tk.Label(frame_instance_number, text="Instance Number:")
    lbl_instance_number.pack(side=tk.LEFT)

    # Entry per il numero dell'istanza
    instance_number = tk.Entry(frame_instance_number, width=10)
    instance_number.pack(side=tk.LEFT, padx=5)

    # Bottone per aggiornare i path
    btn_update_paths = tk.Button(frame_instance_number, text="Update Paths",
                                 command=update_file_paths)
    btn_update_paths.pack(side=tk.LEFT)



def create_gui(root):
    global lbl_solution_status, lbl_instance_status, lbl_consumption_status
    global entry_solution, entry_instance, entry_consumption
    global code_output, btn_reset
    global tab_control, tab_energy

    def on_closing():
        plt.close('all')
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Aggiungi l'input per il numero dell'istanza prima dei file inputs
    create_instance_number_input(root)

    # Solution file
    frame_solution = tk.Frame(root)
    frame_solution.pack(pady=5, fill=tk.X, padx=10)

    btn_solution = tk.Button(frame_solution, text='Select Solution File', command=select_solution_file)
    btn_solution.pack(side=tk.LEFT)

    entry_solution = tk.Entry(frame_solution)
    entry_solution.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0))
    entry_solution.bind("<FocusOut>", lambda e: update_file_path('solution'))

    lbl_solution_status = tk.Label(frame_solution, text="No Solution File Loaded", fg="red")
    lbl_solution_status.pack(side=tk.LEFT, padx=(5, 0))

    # Instance file
    frame_instance = tk.Frame(root)
    frame_instance.pack(pady=5, fill=tk.X, padx=10)

    btn_instance = tk.Button(frame_instance, text='Select Instance File', command=select_instance_file)
    btn_instance.pack(side=tk.LEFT)

    entry_instance = tk.Entry(frame_instance)
    entry_instance.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0))
    entry_instance.bind("<FocusOut>", lambda e: update_file_path('instance'))

    lbl_instance_status = tk.Label(frame_instance, text="No Instance File Loaded", fg="red")
    lbl_instance_status.pack(side=tk.LEFT, padx=(5, 0))

    # Consumption file
    frame_consumption = tk.Frame(root)
    frame_consumption.pack(pady=5, fill=tk.X, padx=10)

    btn_consumption = tk.Button(frame_consumption, text='Select Consumption File', command=select_consumption_file)
    btn_consumption.pack(side=tk.LEFT)

    entry_consumption = tk.Entry(frame_consumption)
    entry_consumption.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0))
    entry_consumption.bind("<FocusOut>", lambda e: update_file_path('consumption'))

    lbl_consumption_status = tk.Label(frame_consumption, text="No Consumption File Loaded", fg="red")
    lbl_consumption_status.pack(side=tk.LEFT, padx=(5, 0))

    tab_control = ttk.Notebook(root)
    tab_gantt = ttk.Frame(tab_control)
    tab_energy = ttk.Frame(tab_control)
    tab_python = ttk.Frame(tab_control)
    tab_control.add(tab_gantt, text='Gantt Chart')
    tab_control.add(tab_energy, text='Energy Consumption')
    #tab_control.add(tab_python, text='Python Execution')
    tab_control.pack(expand=1, fill='both')

    btn_visualize_gantt = tk.Button(tab_gantt, text='Visualize Gantt Chart',
                                   command=lambda: visualize_gantt_chart(tab_gantt))
    btn_visualize_gantt.pack(pady=20)

    btn_visualize_energy = tk.Button(tab_energy, text='Visualize Interactive Energy Consumption',
                                    command=lambda: visualize_energy_consumption_interactive(tab_energy))
    btn_visualize_energy.pack(pady=20)

    btn_reset = tk.Button(root, text='Reset', command=lambda: reset_all(root))
    btn_reset.pack(pady=10)

    # Python Execution Tab
    #btn_execute = tk.Button(tab_python, text='Execute Python Code', command=execute_python_code)
    #btn_execute.pack(pady=10)

    code_output = scrolledtext.ScrolledText(tab_python, height=20)
    code_output.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    root.geometry('800x600')