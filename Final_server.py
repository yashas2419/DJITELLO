import KeyPressModule as kp
import socket
from time import sleep

# PC1 Tailscale details
PC1_TAILSCALE_IP = '100.65.191.1'  # your PC1 Tailscale IP
PC1_PORT = 9000  # port where proxy server is running

# Setup UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Initialize KeyPress
kp.init()

def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50
    command = None

    if kp.getKey("LEFT"):
        lr = -speed
    elif kp.getKey("RIGHT"):
        lr = speed
    if kp.getKey("UP"):
        fb = speed
    elif kp.getKey("DOWN"):
        fb = -speed
    if kp.getKey("w"):
        ud = speed
    elif kp.getKey("s"):
        ud = -speed
    if kp.getKey("a"):
        yv = -speed
    elif kp.getKey("d"):
        yv = speed
    if kp.getKey("l"):
        command = "land"
    if kp.getKey("e"):
        command = "takeoff"

    return [lr, fb, ud, yv], command

while True:
    vals, cmd = getKeyboardInput()
    # Create a formatted string
    if cmd:
        message = cmd
    else:
        message = f"rc {vals[0]} {vals[1]} {vals[2]} {vals[3]}"

    # Send to PC1
    sock.sendto(message.encode(), (PC1_TAILSCALE_IP, PC1_PORT))
    print(f"Sent: {message}")

    sleep(0.05)
