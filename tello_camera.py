import cv2
import socket
import threading
import KeyPressModule as kp
from time import sleep

# PC1 Tailscale IP
PC1_TAILSCALE_IP = '100.78.31.97'
COMMAND_PORT = 9000

# Setup UDP socket for sending commands
sock_cmd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Initialize KeyPress
kp.init()

def send_commands():
    while True:
        vals, cmd = getKeyboardInput()
        if cmd:
            message = cmd
        else:
            message = f"rc {vals[0]} {vals[1]} {vals[2]} {vals[3]}"

        sock_cmd.sendto(message.encode(), (PC1_TAILSCALE_IP, COMMAND_PORT))
        sleep(0.05)

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

# Start sending commands in background
threading.Thread(target=send_commands, daemon=True).start()

# ⚡ OpenCV way to read video stream via UDP
# **Connect to local UDP port (which PC1 forwards)**
cap = cv2.VideoCapture('udp://0.0.0.0:11111', cv2.CAP_FFMPEG)

if not cap.isOpened():
    print("❌ Cannot open video stream")
    exit()

while True:
    ret, frame = cap.read()
    if ret:
        frame = cv2.resize(frame, (720, 480))
        cv2.imshow("Tello Video", frame)
    else:
        print("No frame received...")

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
