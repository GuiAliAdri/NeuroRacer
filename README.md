# 🏎️ NeuroRacer - Evolutionary AI

A self-driving car simulation where vehicles learn to drive autonomously using Neural Networks and Genetic Algorithms (NEAT). With every generation, the AI evolves, learning to navigate curves, avoid obstacles, and optimize its path on a procedurally generated track.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Pygame](https://img.shields.io/badge/Library-Pygame-green)
![NEAT](https://img.shields.io/badge/Algorithm-NEAT-orange)

## 🧠 How It Works

The project utilizes the **NEAT-Python** (NeuroEvolution of Augmenting Topologies) library.

1.  **Sensors (Input):** Each car is equipped with 5 "rays" (LIDAR-like sensors) that measure the distance to walls or obstacles.
2.  **Neural Network:** These distance values are fed into the car's neural network as input.
3.  **Action (Output):** The network processes the inputs and decides whether to steer **Left** or **Right**.
4.  **Evolution:** Cars that travel further and pass through more checkpoints are rewarded with higher "fitness". The worst performers are eliminated, and the best ones pass their "genes" (weights and biases) to the next generation with slight mutations.

## 🚀 Key Features

* **Procedural Track Generation:** The track layout, finish line, and obstacles are mathematically generated via code every time the game runs, ensuring the IA generalizes rather than memorizing a static map.
* **AI Vision Visualization:** Real-time rendering of sensor rays (green lines) showing exactly what the car detects.
* **Checkpoint System:** Robust logic using invisible checkpoints to ensure cars follow the correct track direction.
* **Performance Tracking:** Displays the current generation, best score, and the number of cars that successfully crossed the finish line.

## 🛠️ Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/NeuroRacer.git](https://github.com/your-username/NeuroRacer.git)
    cd NeuroRacer
    ```

2.  **Create a virtual environment (Optional but recommended):**
    ```bash
    # Windows:
    python -m venv venv
    .\venv\Scripts\activate

    # Linux/Mac:
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install pygame neat-python
    ```

## 🎮 How to Run

1.  **Generate Assets (First run only):**
    Run this script to create the `assets` folder and generate the pixel art car sprite automatically.
    ```bash
    python setup_assets.py
    ```

2.  **Start the Simulation:**
    ```bash
    python main.py
    ```

## ⚙️ Configuration (NEAT)

You can tweak the Artificial Intelligence parameters by editing the `config-neat.txt` file:

* **`pop_size`**: The number of cars per generation (Default: 30). Increase this for faster evolution if your CPU can handle it.
* **`fitness_threshold`**: The score required to consider the simulation "won".
* **Mutation Rates**: Adjust how much the neural network changes between generations.

## 📂 Project Structure

* `main.py`: Entry point that initializes the NEAT loop.
* `src/`: Contains the game source code.
    * `game.py`: Manages the game window, loop, and rendering.
    * `car.py`: Handles car physics, sensor logic, and collision detection.
    * `track_generator.py`: Algorithm that procedurally draws the visual track and collision masks.
    * `config.py`: Global constants (colors, speed, screen dimensions).
* `assets/`: Game images (generated via script).

---
Developed with 🐍 Python.
##### Made By: Guilherme Ali Adri