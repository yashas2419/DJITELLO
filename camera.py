import socket
import cv2
import numpy as np
import threading

latest_frame = None
lock = threading.Lock()

def receive_frames(sock):
    global latest_frame
    while True:
        try:
            packet, addr = sock.recvfrom(65536)
            npdata = np.frombuffer(packet, dtype=np.uint8)
            frame = cv2.imdecode(npdata, cv2.IMREAD_COLOR)
            if frame is not None:
                with lock:
                    latest_frame = frame
        except:
            continue

def display_frames():
    global latest_frame
    while True:
        with lock:
            frame = latest_frame
        if frame is not None:
            cv2.imshow('Received Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 11111))
sock.settimeout(0.01)

print("Receiving and displaying video...")

# Start receiving thread
recv_thread = threading.Thread(target=receive_frames, args=(sock,))
recv_thread.daemon = True
recv_thread.start()

display_frames()

sock.close()
cv2.destroyAllWindows()
