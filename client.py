import math
import pickle
import socket
import cv2

max_lenght = 65000
host = "127.0.0.1"
port = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cap = cv2.VideoCapture(0)
ret, frame = cap.read()

while ret:
    # compress frame
    retval, buffer = cv2.imencode('.jpg', frame)

    if retval:
        # convert to byte array
        buffer = buffer.tobytes()
        # get size of the frame
        buffer_size = len(buffer)

        num_of_packs = 1
        if buffer_size > max_lenght:
            num_of_packs = math.ceil(buffer_size / max_lenght)

        frame_info = {"packs": num_of_packs}

        # send the number of packs to be expected
        print("Number of packs:", num_of_packs)
        sock.sendto(pickle.dumps(frame_info), (host, port))
        left = 0
        right = max_lenght

        for i in range(num_of_packs):
            print("left:", left)
            print("right:", right)

            # truncate the data to send
            data = buffer[left:right]
            left = right
            right += max_lenght

            # send the frames accordingly
            sock.sendto(data, (host, port))

    ret, frame = cap.read()

print("done")