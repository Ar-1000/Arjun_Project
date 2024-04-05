
import tkinter as tk

from tkinter import ttk

import backend_apache

import backend_ssh



# Define global variables

apache_var = None

ssh_var = None

output_text = None



def start_selected_services():

    """Start selected services based on checkbox states."""

    if apache_var.get():

        backend_apache.start_services()

        backend_apache.backup_config_file(backend_apache.config_file_path, backend_apache.backup_file_path)

        root.after(10000, change_apache_port)  # Schedule port change after 10 seconds

    if ssh_var.get():

        backend_ssh.start_stop_ssh_service("start")



def stop_selected_services():

    """Stop selected services based on checkbox states."""

    if apache_var.get():

        backend_apache.stop_services()

    if ssh_var.get():

        backend_ssh.start_stop_ssh_service("stop")



def change_apache_port():

    """Change Apache port and update output."""

    new_port = backend_apache.generate_random_port()

    backend_apache.edit_port_config(backend_apache.config_file_path, new_port)

    output_text.config(state=tk.NORMAL)

    output_text.insert(tk.END, f"Apache port changed to {new_port}\n")

    output_text.see(tk.END)

    output_text.config(state=tk.DISABLED)

    root.after(10000, change_apache_port)  # Schedule next port change after 10 seconds



def run_frontend():

    global apache_var, ssh_var, output_text, root



    root = tk.Tk()

    root.title("Service Manager")



    window_width = 800

    window_height = 600

    screen_width = root.winfo_screenwidth()

    screen_height = root.winfo_screenheight()

    x = (screen_width - window_width) // 2

    y = (screen_height - window_height) // 2

    root.geometry(f"{window_width}x{window_height}+{x}+{y}")



    button_frame = ttk.Frame(root)

    button_frame.pack(pady=20)



    start_button = ttk.Button(button_frame, text="Start Selected Services", command=start_selected_services)

    start_button.grid(row=0, column=0, padx=10)



    stop_button = ttk.Button(button_frame, text="Stop Selected Services", command=stop_selected_services)

    stop_button.grid(row=0, column=1, padx=10)



    service_frame = ttk.Frame(root)

    service_frame.pack(pady=20)



    apache_var = tk.BooleanVar()

    apache_checkbox = ttk.Checkbutton(service_frame, text="Apache", variable=apache_var)

    apache_checkbox.grid(row=0, column=0, padx=10)



    ssh_var = tk.BooleanVar()

    ssh_checkbox = ttk.Checkbutton(service_frame, text="SSH", variable=ssh_var)

    ssh_checkbox.grid(row=0, column=1, padx=10)



    output_frame = ttk.Frame(root)

    output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)



    output_text = tk.Text(output_frame, width=50, height=20)

    output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)



    scrollbar = ttk.Scrollbar(output_frame, orient=tk.VERTICAL, command=output_text.yview)

    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    output_text.config(yscrollcommand=scrollbar.set)



    root.mainloop()



if __name__ == "__main__":

    run_frontend()
