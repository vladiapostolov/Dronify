import cv2

def scan_qr(camera_index: int = 0):
    cap = cv2.VideoCapture(camera_index)
    detector = cv2.QRCodeDetector()

    if not cap.isOpened():
        return None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        data, bbox, _ = detector.detectAndDecode(frame)
        if data:
            cap.release()
            cv2.destroyAllWindows()
            return data.strip()

        cv2.imshow("QR Scanner (press Q to cancel)", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None
