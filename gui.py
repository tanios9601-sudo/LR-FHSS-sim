import tkinter as tk
from tkinter import ttk, messagebox

from lrfhss.settings import Settings
from run import run_sim


def launch_simulation():
    try:
        number_nodes = int(nodes_entry.get())
        simulation_time = int(time_entry.get())
        headers = int(headers_entry.get())
        code = code_combo.get()
        base = base_combo.get()

        settings = Settings(
            number_nodes=number_nodes,
            simulation_time=simulation_time,
            headers=headers,
            code=code,
            base=base
        )

        result = run_sim(settings)

        # Extraction correcte depuis [[a],[b],[c]]
        success_ratio = result[0][0]
        goodput = result[1][0]
        transmitted = result[2][0]

        result_text = (
            f"Success ratio: {success_ratio:.4f}\n"
            f"Goodput (payload units): {goodput}\n"
            f"Transmitted packets: {transmitted}"
        )

        result_label.config(text=result_text)

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ==============================
#           GUI SETUP
# ==============================

root = tk.Tk()
root.title("LR-FHSS Simulator")
root.geometry("450x400")

main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(fill="both", expand=True)


# -------- Number of Nodes --------
tk.Label(main_frame, text="Number of Nodes").grid(row=0, column=0, sticky="w")
nodes_entry = tk.Entry(main_frame)
nodes_entry.insert(0, "1000")
nodes_entry.grid(row=0, column=1, pady=5)


# -------- Simulation Time --------
tk.Label(main_frame, text="Simulation Time (s)").grid(row=1, column=0, sticky="w")
time_entry = tk.Entry(main_frame)
time_entry.insert(0, "3600")
time_entry.grid(row=1, column=1, pady=5)


# -------- Headers --------
tk.Label(main_frame, text="Header Replicas").grid(row=2, column=0, sticky="w")
headers_entry = tk.Entry(main_frame)
headers_entry.insert(0, "3")
headers_entry.grid(row=2, column=1, pady=5)


# -------- Coding Rate --------
tk.Label(main_frame, text="Coding Rate").grid(row=3, column=0, sticky="w")
code_combo = ttk.Combobox(main_frame, values=["1/3", "1/2", "2/3", "5/6"])
code_combo.set("2/3")
code_combo.grid(row=3, column=1, pady=5)


# -------- Base Station Type --------
tk.Label(main_frame, text="Base Station Type").grid(row=4, column=0, sticky="w")
base_combo = ttk.Combobox(main_frame, values=["core", "acrda"])
base_combo.set("core")
base_combo.grid(row=4, column=1, pady=5)


# -------- Run Button --------
run_button = tk.Button(
    main_frame,
    text="Run Simulation",
    command=launch_simulation,
    bg="#4CAF50",
    fg="white",
    height=2
)
run_button.grid(row=5, column=0, columnspan=2, pady=15)


# -------- Results --------
result_label = tk.Label(
    main_frame,
    text="Results will appear here...",
    justify="left",
    anchor="w"
)
result_label.grid(row=6, column=0, columnspan=2, pady=10)


root.mainloop()