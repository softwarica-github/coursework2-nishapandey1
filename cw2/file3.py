import socket
import tkinter as tk
from tkinter import messagebox
import threading

# Define the IP address and port to listen on
LISTEN_IP = '127.0.0.1'
LISTEN_PORT = 1234

# Define a list of allowed connections
allowed_connections = [
    {'ip': '192.168.56.107', 'port': 80},
    {'ip': '192.168.0.2', 'port': 10002},
]

# Define a list of denied ports
denied_ports = [21, 443]

# Create a Tkinter window
root = tk.Tk()

# Define a flag to indicate that the firewall is running
running = False

def close():
    root.destroy()

# Define a function to handle incoming connections
def handle_connection(connection, client_address):
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

    # Check if the connection is trying to connect to a denied port
    if client_address[1] in denied_ports:
        print(f"Connection from {client_address[0]}:{client_address[1]} is denied")
        connection.close()
        return

    # Check if the connection is allowed based on the allowed connections list
    connection_allowed = False
    for rule in allowed_connections:
        if client_address[0] == rule['ip'] and client_address[1] == rule['port']:
            connection_allowed = True
            break

    # Send a response to the client based on whether the connection is allowed or not
    if connection_allowed:
        connection.sendall(b'Connection allowed')
        print(f"Connection from {client_address[0]}:{client_address[1]} is allowed")
    else:
        connection.sendall(b'Connection not allowed')
        print(f"Connection from {client_address[0]}:{client_address[1]} is not allowed")

    # Wait for a short period to allow the client to receive the response
    connection.settimeout(1)

    # Close the connection
    connection.close()

# Define a function to start the firewall
def start_firewall():
    global sock

    # Create a socket and bind it to the IP address and port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((LISTEN_IP, LISTEN_PORT))

    # Start listening for incoming connections
    sock.listen()
    print(f"Listening for connections on {LISTEN_IP}:{LISTEN_PORT}")

    # Set the flag to indicate that the firewall is running
    running = True

    # Start accepting incoming connections in a loop
    while running:
        connection, client_address = sock.accept()
        threading.Thread(target=handle_connection, args=(connection, client_address)).start()

# Define a function to stop the firewall
def stop_firewall():
    global running
    running = False
    print("Firewall stopped")


# Define a function to add a rule
def add_rule():
    ip = ip_entry.get()
    port = int(port_entry.get())
    allowed_connections.append({'ip': ip, 'port': port})
    print(f"Added rule: {ip}:{port}")
    update_gui()

# Define a function to update the GUI
def update_gui():
    # Clear the allowed connections list
    allowed_connections_listbox.delete(0, tk.END)

    # Add the allowed connections to the listbox
    for rule in allowed_connections:
        allowed_connections_listbox.insert(tk.END, f"{rule['ip']}:{rule['port']}")


root.configure(bg='gray')
root.geometry("800x800")

# Create a Start button
start_button = tk.Button(root, text="Start Firewall",font=("Times New Roman",16),bg='silver', command=start_firewall)
start_button.pack()

# Create a Stop button
stop_button = tk.Button(root, text="Stop Firewall",font=("Times New Roman",16),bg='silver', command=stop_firewall)
stop_button.pack()

# Create a form to add rules
ip_label = tk.Label(root, text="IP Address:",font=("Times New Roman",16),bg='silver')
ip_label.pack()
ip_entry = tk.Entry(root)
ip_entry.pack()

port_label = tk.Label(root, text="Port:",font=("Times New Roman",16),bg='silver',)
port_label.pack()
port_entry = tk.Entry(root)
port_entry.pack()

add_button = tk.Button(root, text="Add Rule", command=add_rule,font=("Times New Roman",16),bg='silver',)
add_button.pack()

allowed_connections_listbox = tk.Listbox(root)
allowed_connections_listbox.pack()

close_button=tk.Button(root, text="Close",font=("Times New Roman",14), background="red", foreground="white",command=root.destroy)
close_button.pack()
root.mainloop()