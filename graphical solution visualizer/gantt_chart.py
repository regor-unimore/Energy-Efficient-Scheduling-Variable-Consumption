import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.colors as mcolors

def plot_gantt_chart(solution_file, instance_file, consumption_file):
    with open(solution_file, 'r') as file:
        solution_data = eval(file.read())

    with open(instance_file, 'r') as file:
        instance_data = file.readlines()

    with open(consumption_file, 'r') as file:
        consumption_data = eval(file.read().split(': ')[1])

    num_jobs = int(instance_data[0].split(': ')[1])
    processing_times = eval(instance_data[1].split(': ')[1])
    num_machines = int(instance_data[2].split(': ')[1])
    time_horizon = int(instance_data[5].split(': ')[1])

    df = pd.DataFrame(solution_data, columns=['Job', 'Machine', 'Start'])
    df['Duration'] = df['Job'].apply(lambda x: processing_times[x])

    colors = list(mcolors.TABLEAU_COLORS.values())

    fig, ax = plt.subplots()

    for t in range(time_horizon + 1):
        ax.axvline(x=t, color='gray', linestyle='--', linewidth=0.5)

    for i, row in df.iterrows():
        ax.broken_barh([(row['Start'], row['Duration'])],
                       (row['Machine'] - 0.4, 0.8),
                       facecolors=(colors[row['Job'] % len(colors)]))
        ax.text(row['Start'] + row['Duration'] / 2, row['Machine'],
                f'Job {row["Job"]}', va='center', ha='center', color='white', fontsize=8)

    ax.set_xlim(0, time_horizon)
    ax.set_xlabel('Time')
    ax.set_ylabel('Machine')
    ax.set_yticks(range(num_machines))
    ax.set_yticklabels(['Machine {}'.format(i) for i in reversed(range(num_machines))])
    ax.set_title('Gantt Chart for Scheduling Solution')

    handles = [plt.Line2D([0], [0], color=colors[i % len(colors)], lw=4) for i in range(num_jobs)]
    labels = ['Job {}'.format(i) for i in range(num_jobs)]
    ax.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=3, fontsize='small')

    fig.tight_layout()
    return fig
