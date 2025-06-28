import socket

# IP address of PC 1 (Tailscale IP)
PC1_TAILSCALE_IP = '100.78.31.97'  # <-- replace with PC1's Tailscale IP
PC1_PORT = 9000  # Same port you used in proxy script

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Example command you want to send
command = "land"





# Send the command
sock.sendto(command.encode(), (PC1_TAILSCALE_IP, PC1_PORT))

print(f"Sent command: {command}")

sock.close()
