import customtkinter as ctk
import tkinter as tk
from scrollableText import ScrollableText
import json
import subprocess
import threading

class NoCGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.data = {}  # This dictionary stores all the testbench architecture
        self.algorithm_settings = {}  # Dictionary to store algorithm settings entries
        self.title("NoC Testbench Configuration")
        #self.geometry("600x500")
        self.process = None  # Process object to run the simulation
        label_font = ("Arial", 14)
        entry_font = ("Arial", 12)
        button_font = ("Arial", 14)
        optionmenu_font = ("Arial", 12)
        # Adjusted geometry for the window
        # Adjusted geometry for the window
        self.geometry("900x700")

        # Split the window into two main frames: top and bottom
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.pack(side="top", fill="both", expand=True, padx=20, pady=10)

        self.bottom_frame = ctk.CTkFrame(self)
        self.bottom_frame.pack(side="bottom", fill="both", expand=True, padx=20, pady=10)

        # Configure top_frame grid layout for three parts
        self.top_frame.grid_columnconfigure(3, weight=2, uniform="top")  # First part (buttons and inputs)
        self.top_frame.grid_columnconfigure(2, weight=2, uniform="top")  # Second part (dynamic algorithm settings)
        self.top_frame.grid_columnconfigure(1, weight=1, uniform="top")  # Third part (dynamic explanations)

        # --- First part: Fixed controls (Rows, Columns, Architecture, Algorithm dropdown) ---

        self.label_rows = ctk.CTkLabel(self.top_frame, text="Rows:", font=label_font)
        self.label_rows.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.entry_rows = ctk.CTkEntry(self.top_frame, placeholder_text="Enter number of rows", font=entry_font)
        self.entry_rows.grid(row=0, column=1, padx=20, pady=10, sticky="w")
        self.entry_rows.insert(0, "4")

        self.label_columns = ctk.CTkLabel(self.top_frame, text="Columns:", font=label_font)
        self.label_columns.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.entry_columns = ctk.CTkEntry(self.top_frame, placeholder_text="Enter number of columns", font=entry_font)
        self.entry_columns.grid(row=1, column=1, padx=20, pady=10, sticky="w")
        self.entry_columns.insert(0, "4")

        self.label_architecture = ctk.CTkLabel(self.top_frame, text="Architecture:", font=label_font)
        self.label_architecture.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.architecture_var = tk.StringVar(value="Mesh")
        self.optionmenu_architecture = ctk.CTkOptionMenu(self.top_frame, values=["Mesh", "Torus"], variable=self.architecture_var, font=optionmenu_font)
        self.optionmenu_architecture.grid(row=2, column=1, padx=20, pady=10, sticky="w")

        self.label_algorithm = ctk.CTkLabel(self.top_frame, text="Algorithm:", font=label_font)
        self.label_algorithm.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        self.algorithm_var = tk.StringVar(value="GA")
        self.optionmenu_algorithm = ctk.CTkOptionMenu(self.top_frame, values=["GA", "DE", "PSO"], variable=self.algorithm_var, command=self.update_algorithm_settings, font=optionmenu_font)
        self.optionmenu_algorithm.grid(row=3, column=1, padx=20, pady=10, sticky="w")

        # Buttons for starting/stopping simulation
        self.start = ctk.CTkButton(self.top_frame, text="Start Simulation", command=self.start_simulation, font=button_font)
        self.start.grid(row=4, column=0, columnspan=2, padx=20, pady=20, sticky="w")

        self.stop = ctk.CTkButton(self.top_frame, text="Stop Simulation", command=self.stop_simulation, font=button_font)
        self.stop.grid(row=5, column=0, columnspan=2, padx=20, pady=10, sticky="w")


        # --- Second part: Algorithm-specific dynamic settings ---
        self.settings_frame = ctk.CTkFrame(self.top_frame)
        self.settings_frame.grid(row=0, column=2, rowspan=6, padx=20, pady=10, sticky="nsew")

        # --- Third part: Explanation of algorithm variables ---
        self.explanation_frame = ctk.CTkFrame(self.top_frame)
        self.explanation_frame.grid(row=0, column=3, rowspan=6, padx=20, pady=10, sticky="nsew")
        self.exp_label = None

        # Bottom frame: Terminal-like output
        self.scrollable_text = ScrollableText(self.bottom_frame, width=80, height=15)
        self.scrollable_text.pack(padx=10, pady=10, fill="both", expand=True)
        self.update_algorithm_settings(event=None)  # Initialize the dynamic fields
        self.scrollable_text.add_text(" "*20+"  Welcome to NoC Testbench  "+" "*20+"\n\n")
        self.scrollable_text.add_text("_"*100)
        self.scrollable_text.add_text("\n\n--> Please select the architecture, algorithm and provide the required parameters before starting the simulation.\n\n")
        self.scrollable_text.add_text("--> Press the start button to start the simulation\n\n")
        self.scrollable_text.add_text("--> The simulation output will be displayed here.\n\n")
        self.scrollable_text.add_text("--> Press the stop button to stop the simulation.\n\n")
        self.scrollable_text.add_text("_"*100)
    def start_simulation(self):
        """Start the simulation in a separate thread to avoid freezing the GUI."""
        row_value = self.entry_rows.get()
        col_value = self.entry_columns.get()
        algorithm = self.algorithm_var.get()
        Topology = self.architecture_var.get()
        # Gather algorithm-specific settings
        self.data["row_value"] = int(row_value)
        self.data["col_value"] = int(col_value)
        self.data["algorithm"] = algorithm
        self.data["Topology"] = Topology
        self.scrollable_text.add_text("_"*100)
        algorithm_params = {key: entry.get() for key, entry in self.algorithm_settings.items()}
        self.data["algorithm_params"] = algorithm_params
        with open("config.json", "w") as config_file:
            json.dump(self.data, config_file)
            config_file.close()
            self.scrollable_text.add_text("\n\nTestbench Settings Updated and dumped to config_file.json\n\n")
        self.scrollable_text.add_text(f"\n Starting simulation with \n rows={row_value}, columns={col_value}\n Topology={Topology}\n algorithm={algorithm}\n params={algorithm_params}\n")
        self.scrollable_text.text_widget.see(tk.END)

        # Use a thread to run the make command so the GUI stays responsive
        sim_thread = threading.Thread(target=self.run_make_command)
        sim_thread.start()


    def stop_simulation(self):
        """Stop the running simulation by terminating the process."""
        if self.process and self.process.poll() is None:  # Check if process is running
            self.scrollable_text.add_text("Stopping simulation...\n")
            self.process.terminate()  # Send a termination signal to the process
            self.process.wait()  # Wait for the process to finish
            self.scrollable_text.add_text("Simulation stopped.\n")
        else:
            self.scrollable_text.add_text("No simulation is running.\n")


    def run_make_command(self):
        """Run the make command and update the GUI with the output."""
        try:
            # Ensure the correct working directory for the makefile
            self.scrollable_text.add_text("\nRunning simulation using 'make'...\n")

            # Use `cwd` argument to specify the correct working directory
            self.process = subprocess.Popen(["make"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=".")

            for line in iter(self.process.stdout.readline, ""):
                self.scrollable_text.add_text( line)
                self.scrollable_text.see(tk.END)  # Auto-scroll to the bottom

            # Check for errors in stderr and display them
            stderr_output = self.process.stderr.read()
            if stderr_output:
                self.scrollable_text.add_text(f"\nErrors:\n{stderr_output}\n")

            self.process.stdout.close()
            self.process.wait()
            self.scrollable_text.add_text("\nSimulation Finished!\n")

        except Exception as e:
            self.scrollable_text.add_text( f"Error running simulation: {str(e)}\n")

    def update_algorithm_settings(self, event):
        """Update the dynamic fields based on selected algorithm."""
        # Clear the previous settings
        for widget in self.settings_frame.winfo_children():
            widget.destroy()
            print(f"widget destroyed: {widget}")

        # Dynamically add fields based on the selected algorithm
        algorithm = self.algorithm_var.get()
        print(f"algorithm selected: {algorithm}")
        self.add_explanation_fields(algorithm)
        if algorithm == "GA":
            self.add_algorithm_fields("n_iter", "n_pop", "r_cross", "r_mut", default_values=["4000", "20", "0.9", "0.9"])
        elif algorithm == "PSO":
            self.add_algorithm_fields("iter_size", "pop_size", default_values=["4100", "600"])
        elif algorithm == "DE":
            self.add_algorithm_fields("gen", "popsize", "crossover_rate", "mutation_rate", default_values=["4032", "10", "0.7", "0.9"])

    def add_algorithm_fields(self, *fields, default_values=None):
        """Add fields for algorithm settings."""
        print(f"add algorithm fields function is invoked: {fields}")
        if default_values is None:
            default_values = [""] * len(fields)

        self.algorithm_settings.clear()  # Clear previous settings

        for i, (field, default_value) in enumerate(zip(fields, default_values)):
            label = ctk.CTkLabel(self.settings_frame, text=f"{field}:", font=("Arial", 16))
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = ctk.CTkEntry(self.settings_frame, placeholder_text=f"Enter {field}", font=("Arial", 16))
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            entry.insert(0, default_value)
            self.algorithm_settings[field] = entry
    def add_explanation_fields(self, algo):
        """Add fields for algorithm settings."""
        
        # Destroy any existing label before adding a new one
        if self.exp_label is not None:
            self.exp_label.destroy()

        # Define the explanation text based on the selected algorithm
        if algo == "GA":
            text = (
                "Genetic Algorithm (GA) Settings:\n\n"
                "n_iter : Number of Iterations\n"
                "n_pop  : Population Size\n"
                "r_cross: Crossover Rate\n"
                "r_mut  : Mutation Rate"
            )
        elif algo == "PSO":
            text = (
                "Particle Swarm Optimization (PSO) Settings:\n\n"
                "iter_size : Number of Iterations\n"
                "pop_size  : Population Size"
            )
        elif algo == "DE":
            text = (
                "Differential Evolution (DE) Settings:\n\n"
                "gen             : Number of Generations\n"
                "popsize         : Population Size\n"
                "crossover_rate  : Crossover Rate\n"
                "mutation_rate   : Mutation Rate"
            )
        else:
            text = "No Explanation Available"

        # Create a new label with improved formatting
        self.exp_label = ctk.CTkLabel(
            self.explanation_frame, text=text, font=("Arial", 16), anchor="w", justify="left"
        )
        
        # Display the label in the grid
        self.exp_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")


# Running the app
if __name__ == "__main__":
    app = NoCGUI()
    app.mainloop()