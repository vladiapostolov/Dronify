import cv2
import numpy as np

def scan_qr(camera_index: int = 0):
    """
    Scan QR code using laptop camera with OpenCV
    Press 'q' to cancel scanning
    """
    cap = cv2.VideoCapture(camera_index)
    
    # Set camera properties for better quality
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    if not cap.isOpened():
        print("Error: Could not access camera")
        return None

    detector = cv2.QRCodeDetector()
    print("QR Scanner started. Position QR code in front of camera. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to read from camera")
            break

        # Detect and decode QR code
        data, bbox, _ = detector.detectAndDecode(frame)
        
        # Draw bounding box if QR code detected
        if bbox is not None:
            bbox = bbox.astype(int)
            # Draw polygon around QR code
            for i in range(len(bbox[0])):
                pt1 = tuple(bbox[0][i])
                pt2 = tuple(bbox[0][(i + 1) % len(bbox[0])])
                cv2.line(frame, pt1, pt2, (0, 255, 0), 3)
            
            # If QR code has data, display it and return
            if data:
                cv2.putText(frame, f"QR Code: {data}", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.imshow("QR Scanner - Code Detected!", frame)
                cv2.waitKey(2000)  # Show detected code for 2 seconds
                cap.release()
                cv2.destroyAllWindows()
                print(f"QR Code detected: {data}")
                return data.strip()
        
        # Display instructions on screen
        cv2.putText(frame, "Position QR code in view", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, "Press 'q' to cancel", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Show the frame
        cv2.imshow("QR Scanner (Dronify)", frame)
        
        # Check for 'q' key to quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            print("Scanning cancelled by user")
            break

    cap.release()
    cv2.destroyAllWindows()
    return None
