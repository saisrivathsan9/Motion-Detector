import cv2 as cv
import serial
import time

# Initialize video capture and serial communication
cap = cv.VideoCapture(0)
ser = serial.Serial('/dev/cu.usbserial-0001', 115200, timeout=1)

# Turn on the LED initially
ser.write(b"ON\n")
time.sleep(1)  # Small delay to ensure the command is processed
first_frame = None

if not cap.isOpened():
    print("Camera not open")
    exit()

frame_count = 0
last_command_time = time.time()  # Track last command time
command_interval = 1  # Interval in seconds between serial commands

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame_count += 1

    if not ret:
        print("Can't receive frame")
        break

    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blurred_frame = cv.GaussianBlur(gray_frame, (21, 21), 0)

    if first_frame is None:
        time.sleep(2)  # Wait for 2 seconds to stabilize
        first_frame = blurred_frame
        continue

    frame_diff = cv.absdiff(first_frame, blurred_frame)
    
    # Apply a threshold to the difference image
    _, thresh_frame = cv.threshold(frame_diff, 25, 255, cv.THRESH_BINARY)

    # Dilate the threshold image to fill in holes
    thresh_frame = cv.dilate(thresh_frame, None, iterations=2)

    # Find contours in the thresholded frame
    contours, _ = cv.findContours(thresh_frame.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    motion_detected = False  # A flag to track if motion is detected

    for contour in contours:
        if cv.contourArea(contour) < 200:  # Ignore small motion
            continue

        motion_detected = True
        (x, y, w, h) = cv.boundingRect(contour)
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Check the time since the last command was sent
    current_time = time.time()
    if motion_detected:
        print("Motion detected")
        print(f"Frame count - {frame_count}")
        
        # Send command if enough time has passed since last command
        if current_time - last_command_time >= command_interval:
            ser.write(b'ON\n')
            print("motion detected")
            last_command_time = current_time  # Update last command time

    else:
        # Send command if enough time has passed since last command
        if current_time - last_command_time >= command_interval:
            ser.write(b'OFF\n')
            last_command_time = current_time  # Update last command time

    # Show the video feed
    cv.imshow('Camera feed', frame)

    if cv.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
cap.release()
ser.write(b'OFF\n')
cv.destroyAllWindows()