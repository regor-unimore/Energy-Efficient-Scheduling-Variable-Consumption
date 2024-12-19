# On incorporating variable consumption functions within energy-efficient parallel machine scheduling

This repository contains the instances and solutions used in the paper **On incorporating variable consumption functions within energy-efficient
parallel machine scheduling**, as well as tools for visualizing the solutions. The repository is organized into structured folders to provide clear access to the data and methods used.

## Repository Structure

### `base configuration`
This folder contains the **base configuration files** for all instances. These files define the initial setup and parameters for the problem instances used in the experiments.

---

### `consumptions`
This folder contains the **consumption functions** used in the instances:
- **`fixed/`**: Includes the consumption functions for instances with fixed consumption.
- **`variable/`**: Includes the consumption functions for instances with variable consumption.

---

### `solutions`
This folder contains the **solutions found by the proposed models** in the paper:
- **`ILS/`**: Solutions obtained using the Iterated Local Search (ILS) algorithm:
  - **`fixed/`**: Solutions for instances with fixed consumption.
  - **`variable/`**: Solutions for instances with variable consumption.
- **`MILP/`**: Solutions obtained using the Mixed-Integer Linear Programming (MILP) model:
  - **`fixed/`**: Solutions for instances with fixed consumption.
  - **`variable/`**: Solutions for instances with variable consumption.

Each subfolder contains results in plain text format of the schedule for the corresponding instance.

---

### `graphical solution visualizer`
This folder contains a **Python GUI** for visualizing the solutions of the problem instances. 
- The visualizer provides an intuitive graphical representation of the solutions, with GANTT Chart and energy consumption Chart.

---

## How to Use

1. **Clone the repository**:
   ```bash
   git clone https://github.com/regor-unimore/Energy-Efficient-Scheduling-Variable-Consumption.git
   
2. **Launch solution visualizer**:
    ```bash
   python main.py