import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.filedialog import asksaveasfilename
import threading
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from war_ver1 import war_game_ver1
from war_ver2 import war_game_ver2
from begger_my_neighbour import play_beggar_my_neighbour
from common import run_simulation_batch, fit_exponential_tail


"""
========================
Card Game Simulator GUI
========================

This is a graphical simulator for turn-based card games like "War" and 
"Beggar-my-Neighbour". It lets you run multiple simulations, visualize
the duration of games, fit an exponential tail to the results, and save
the histogram plot.

How to Use:
-----------
1. Run this file (Game_Simulater.py). A GUI window will open.
2. From the dropdown, choose one of the available games:
      - War Game Ver1
      - War Game Ver2
      - Beggar-my-Neighbour
3. Click "Start" to proceed to the simulation screen.
4. Set the number of games to simulate in each step.
5. Click:
    • "Run" to start the simulation.
    • "Pause" to stop and view an exponential fit to the data.
    • "Go Back" to return to game selection.
    • "Download Plot" to save the current histogram as a PNG file.

Plot Details:
-------------
- The X-axis shows game duration (in turns).
- The Y-axis shows how frequently games ended at that duration.
- The legend shows total games simulated and the exponential fit.

Adding a New Game:
------------------
To add a new game to the simulator:
1. Create a function that runs one game and returns the number of turns.
2. Import that function into this script.
3. Add its name to the dropdown list (`options` in setup_selection_screen).
4. Add the function to the `game_map` dictionary in `run_simulation_loop`.

Enjoy analyzing randomness in classic card games!
"""

class GameSimulator:
    """
    Main GUI Application class to manage game selection, simulation, plotting and controls.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Card Game Simulator")
        self.game_choice = tk.StringVar()
        self.batch_size = tk.IntVar(value=50)

        self.simulation_running = False
        self.simulation_thread = None
        self.hist_data = []

        self.setup_selection_screen()

    def setup_selection_screen(self):
        """
        Set up the initial screen to choose a game.
        """
        for widget in self.root.winfo_children():
            widget.destroy()

        label = tk.Label(self.root, text="Choose a Game:")
        label.pack(pady=10)

        options = ["-- Select a Game --", "War Game Ver1", "War Game Ver2", "Beggar-my-Neighbour"]
        self.game_choice.set(options[0])
        combo = ttk.Combobox(self.root, textvariable=self.game_choice, values=options, state="readonly")
        combo.pack(pady=10)

        start_button = tk.Button(self.root, text="Start", command=self.validate_game_selection)
        start_button.pack(pady=10)

    def validate_game_selection(self):
        """
        Check that a game is selected before starting simulation.
        """
        if self.game_choice.get() in ("War Game Ver1", "War Game Ver2", "Beggar-my-Neighbour"):
            self.setup_simulation_screen()
        else:
            messagebox.showwarning("Selection Required", "Please select a game before starting.")

    def setup_simulation_screen(self):
        """
        Set up the simulation GUI: batch size entry, control buttons, and plot.
        """
        for widget in self.root.winfo_children():
            widget.destroy()

        batch_frame = tk.Frame(self.root)
        batch_frame.pack(pady=5)
        tk.Label(batch_frame, text="Number of games per step:").pack(side=tk.LEFT)
        tk.Entry(batch_frame, textvariable=self.batch_size, width=5).pack(side=tk.LEFT)

        button_frame = tk.Frame(self.root)
        button_frame.pack()

        run_btn = tk.Button(button_frame, text="Run", command=self.start_simulation)
        run_btn.grid(row=0, column=0, padx=5)

        pause_btn = tk.Button(button_frame, text="Pause", command=self.pause_simulation)
        pause_btn.grid(row=0, column=1, padx=5)

        stop_btn = tk.Button(button_frame, text="Go Back", command=self.stop_simulation)
        stop_btn.grid(row=0, column=2, padx=5)

        save_btn = tk.Button(button_frame, text="Download Plot", command=self.save_plot)
        save_btn.grid(row=0, column=3, padx=5)

        self.legend_label = tk.Label(self.root, text="Games Simulated: 0")
        self.legend_label.pack(pady=5)

        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Frequency")
        self.update_title()
        self.canvas.draw()

    def update_title(self):
        """
        Update the plot title with the selected game name.
        """
        title_game = self.game_choice.get()
        self.ax.set_title(f"{title_game} Duration Histogram")

    def start_simulation(self):
        """
        Start the simulation loop in a background thread.
        """
        if not self.simulation_running:
            self.simulation_running = True
            self.simulation_thread = threading.Thread(target=self.run_simulation_loop)
            self.simulation_thread.start()

    def run_simulation_loop(self):
        """
        Loop that runs batches of simulations until paused or stopped.
        """
        while self.simulation_running:
            try:
                BATCH_SIZE = max(1, self.batch_size.get())
                game_map = {
                    "War Game Ver1": war_game_ver1,
                    "War Game Ver2": war_game_ver2,
                    "Beggar-my-Neighbour": play_beggar_my_neighbour
                }
                game_func = game_map.get(self.game_choice.get(), lambda: 0)
                new_steps = run_simulation_batch(game_func, BATCH_SIZE)

                self.hist_data.extend(new_steps)
                self.update_histogram()
                self.legend_label.config(text=f"Games Simulated: {len(self.hist_data)}")
            except Exception as e:
                print(f"Error during simulation: {e}")

    def update_histogram(self):
        """
        Update the histogram with current game duration data.
        """
        self.ax.clear()
        self.ax.hist(self.hist_data, bins=100, color='skyblue', edgecolor='black')
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Frequency")
        self.update_title()
        self.canvas.draw()

    def pause_simulation(self):
        """
        Pause simulation and fit an exponential tail to the histogram.
        """
        self.simulation_running = False
        if self.hist_data:
            try:
                x_fit, y_fit, lam, mean_val, count = fit_exponential_tail(self.hist_data)
                self.update_histogram()
                self.ax.plot(
                    x_fit,
                    y_fit,
                    color='red',
                    label=f"\u03bb = {lam:.4f}\nmean = {round(mean_val, 1)}\nNumber of Games= {count}"
                )
                self.ax.legend()
                self.canvas.draw()
            except Exception as e:
                print(f"Exponential fit failed: {e}")

    def stop_simulation(self):
        """
        Stop simulation, reset data, and return to game selection screen.
        """
        self.simulation_running = False
        if self.simulation_thread and self.simulation_thread.is_alive():
            self.simulation_thread.join(timeout=1)
            if self.simulation_thread.is_alive():
                print("Warning: Simulation thread did not terminate cleanly.")

        self.hist_data.clear()
        self.setup_selection_screen()

    def save_plot(self):
        """
        Save the current plot as a PNG file.
        """
        filename = asksaveasfilename(defaultextension=".png",
                                     filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                                     title="Save Plot As")
        if filename:
            self.canvas.draw()
            self.fig.savefig(filename)
            print(f"Plot saved as '{filename}'")

if __name__ == "__main__":
    import sys
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", lambda: (root.destroy(), sys.exit()))
    app = GameSimulator(root)
    root.mainloop()
