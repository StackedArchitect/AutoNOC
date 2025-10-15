from tkinter import scrolledtext, ttk
import subprocess
import threading
import json
import tkinter as tk

class TestbenchGUI:
    def __init__(self, root):
        self.data = {}
        self.root = root
        self.root.title("NOC Testbench GUI")
        self.root.geometry("800x600")
        # Initialize variables
        self.process = None  # To store the running process
        self.algorithm_settings = {}  # For storing dynamically created text fields

        # Create a vertically split window
        self.paned_window = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=1)

        # Left frame for testbench settings
        self.left_frame = tk.Frame(self.paned_window)
        self.paned_window.add(self.left_frame)

        # Right frame for terminal output
        self.right_frame = tk.Frame(self.paned_window)
        self.paned_window.add(self.right_frame)

        # Testbench settings (Left side)
        self.create_testbench_settings(self.left_frame)

        # Terminal output (Right side)
        self.create_terminal_output(self.right_frame)



    def toggle_mode(self):
        """Toggle between dark mode and color mode."""
        if self.is_dark_mode:
            self.set_color_mode()
        else:
            self.set_dark_mode()
        self.is_dark_mode = not self.is_dark_mode

    def create_testbench_settings(self, parent):
        """Create the widgets for testbench settings on the left side."""
        ttk.Label(parent, text="Testbench Settings", font=("Arial", 14)).pack(pady=10)

        # Row Input
        ttk.Label(parent, text="Rows:").pack(anchor='w', padx=10, pady=5)
        self.row_input = ttk.Entry(parent)
        self.row_input.insert(0, "2")  # Default value for Rows
        self.row_input.pack(fill=tk.X, padx=10, pady=5)

        # Column Input
        ttk.Label(parent, text="Columns:").pack(anchor='w', padx=10, pady=5)
        self.column_input = ttk.Entry(parent)
        self.column_input.insert(0, "2")  # Default value for Columns
        self.column_input.pack(fill=tk.X, padx=10, pady=5)

        # Topology Input
        ttk.Label(parent, text="Topology(0 for mesh, 1 for torus):").pack(anchor='w', padx=10, pady=5)
        self.Topology = ttk.Entry(parent)
        self.Topology.insert(0, "0")  # Default value for Topology
        self.Topology.pack(fill=tk.X, padx=10, pady=5)

        # Algorithm Selection Dropdown
        ttk.Label(parent, text="Select Algorithm:").pack(anchor='w', padx=10, pady=5)
        self.algorithm_var = tk.StringVar(parent)
        self.algorithm_menu = ttk.Combobox(parent, textvariable=self.algorithm_var)
        self.algorithm_menu['values'] = ["GA", "PSO", "DE"]
        self.algorithm_menu.bind("<<ComboboxSelected>>", self.update_algorithm_settings)
        self.algorithm_menu.pack(fill=tk.X, padx=10, pady=5)

        # Frame to hold dynamic algorithm settings
        self.settings_frame = ttk.Frame(parent)
        self.settings_frame.pack(fill=tk.X, padx=10, pady=5)

        # Frame to hold buttons
        self.button_frame = ttk.Frame(parent)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        # Button to start the simulation
        self.start_button = ttk.Button(self.button_frame, text="Start Simulation", command=self.start_simulation)
        self.start_button.pack(side=tk.LEFT, padx=5)

        # Button to stop the simulation
        self.stop_button = ttk.Button(self.button_frame, text="Stop Simulation", command=self.stop_simulation)
        self.stop_button.pack(side=tk.LEFT, padx=5)

   

    def create_terminal_output(self, parent):
        """Create the terminal output display on the right side."""
        ttk.Label(parent, text="Terminal Output", font=("Arial", 14)).pack(pady=10)

        # Scrolled Text widget to display logs
        self.log_output = scrolledtext.ScrolledText(parent, wrap=tk.WORD, width=60, height=20, font=("Arial", 12))
        self.log_output.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def update_algorithm_settings(self, event):
        """Update the dynamic fields based on selected algorithm."""
        # Clear the previous settings
        for widget in self.settings_frame.winfo_children():
            widget.destroy()

        # Dynamically add fields based on the selected algorithm
        algorithm = self.algorithm_var.get()

        if algorithm == "GA":
            self.add_algorithm_fields("n_iter", "n_pop", "r_cross", "r_mut", default_values=["4000", "20", "0.9", "0.9"])
        elif algorithm == "PSO":
            self.add_algorithm_fields("iter_size", "pop_size", default_values=["4100", "600"])
        elif algorithm == "DE":
            self.add_algorithm_fields("gen", "popsize", "crossover_rate", "mutation_rate", default_values=["4032", "10", "0.7", "0.9"])

    def add_algorithm_fields(self, *args, default_values=None):
        """Dynamically add text fields for algorithm-specific parameters."""
        self.algorithm_settings = {}
        if default_values is None:
            default_values = [""] * len(args)  # Default to empty strings if no defaults provided

        for field, default_value in zip(args, default_values):
            ttk.Label(self.settings_frame, text=f"{field}:").pack(anchor='w', padx=5, pady=5)
            entry = ttk.Entry(self.settings_frame)
            entry.insert(0, default_value)  # Set the default value for each entry
            entry.pack(fill=tk.X, padx=5, pady=5)
            self.algorithm_settings[field] = entry

    def start_simulation(self):
        """Start the simulation in a separate thread to avoid freezing the GUI."""
        row_value = self.row_input.get()
        col_value = self.column_input.get()
        algorithm = self.algorithm_var.get()
        Topology = self.Topology.get()
        # Gather algorithm-specific settings
        self.data["row_value"] = int(row_value)
        self.data["col_value"] = int(col_value)
        self.data["algorithm"] = algorithm
        self.data["Topology"] = int(Topology)

        algorithm_params = {key: entry.get() for key, entry in self.algorithm_settings.items()}
        self.data["algorithm_params"] = algorithm_params
        with open("config.json", "w") as config_file:
            json.dump(self.data, config_file)
            config_file.close()
            self.log_output.insert(tk.END, "\n\nTestbench Settings Updated and dumped to config_file.json\n\n")
        self.log_output.insert(tk.END, f"\n Starting simulation with rows={row_value}, columns={col_value}\n Topology={Topology}\n algorithm={algorithm}\n params={algorithm_params}...\n")
        self.log_output.see(tk.END)

        # Use a thread to run the make command so the GUI stays responsive
        sim_thread = threading.Thread(target=self.run_make_command)
        sim_thread.start()

    def run_make_command(self):
        """Run the make command and update the GUI with the output."""
        try:
            # Ensure the correct working directory for the makefile
            self.log_output.insert(tk.END, "\nRunning simulation using 'make'...\n")

            # Use `cwd` argument to specify the correct working directory
            self.process = subprocess.Popen(["make"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=".")

            for line in iter(self.process.stdout.readline, ""):
                self.log_output.insert(tk.END, line)
                self.log_output.see(tk.END)  # Auto-scroll to the bottom

            # Check for errors in stderr and display them
            stderr_output = self.process.stderr.read()
            if stderr_output:
                self.log_output.insert(tk.END, f"\nErrors:\n{stderr_output}\n")

            self.process.stdout.close()
            self.process.wait()
            self.log_output.insert(tk.END, "\nSimulation Finished!\n")

        except Exception as e:
            self.log_output.insert(tk.END, f"Error running simulation: {str(e)}\n")

    def stop_simulation(self):
        """Stop the running simulation by terminating the process."""
        if self.process and self.process.poll() is None:  # Check if process is running
            self.log_output.insert(tk.END, "Stopping simulation...\n")
            self.process.terminate()  # Send a termination signal to the process
            self.process.wait()  # Wait for the process to finish
            self.log_output.insert(tk.END, "Simulation stopped.\n")
        else:
            self.log_output.insert(tk.END, "No simulation is running.\n")

# Create the GUI window
root = tk.Tk()
app = TestbenchGUI(root)

# Start the Tkinter event loop
root.mainloop()