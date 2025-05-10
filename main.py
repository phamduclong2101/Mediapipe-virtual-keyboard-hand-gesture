import cv2
import mediapipe as mp
from time import sleep
from pynput.keyboard import Controller

# Khởi tạo camera
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Đặt chiều rộng khung hình
cap.set(4, 720)   # Đặt chiều cao khung hình

# Khởi tạo Mediapipe Hand
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.8)
mpDraw = mp.solutions.drawing_utils

# Các phím trên bàn phím ảo
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"," "],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", "<"]]
finalText = ""

# Khởi tạo bộ điều khiển bàn phím
keyboard = Controller()

# Lớp Button để định nghĩa các nút
class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text

# Hàm vẽ tất cả các nút
def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img

# Tạo danh sách các nút
buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

# Vòng lặp chính
while True:
    success, img = cap.read()
    if not success or img is None:
        print("Can't read image from camera !")
        break

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    # Vẽ các nút
    img = drawAll(img, buttonList)

    # Kiểm tra nếu có bàn tay
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lmList = []
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append((cx, cy))

            # Vẽ bàn tay
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            # Kiểm tra nếu ngón tay trỏ nằm trong vùng nút
            if lmList:
                for button in buttonList:
                    x, y = button.pos
                    w, h = button.size

                    if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                        cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (175, 0, 175), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 65),
                                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                        # Tính khoảng cách giữa ngón tay trỏ và ngón giữa
                        x1, y1 = lmList[8]
                        x2, y2 = lmList[12]
                        l = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
                        print(f"Distance: {l}")

                        # Khi nhấn nút
                        if l < 28:
                            keyboard.press(button.text)
                            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), cv2.FILLED)
                            cv2.putText(img, button.text, (x + 20, y + 65),
                                        cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                            if button.text == '<':
                                if len(finalText) != 0:
                                    finalText = finalText[:-1]
                            else:
                                finalText += button.text
                            sleep(0.5)

    # Hiển thị văn bản đã nhập
    cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (60, 430),
                cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    # Hiển thị hình ảnh
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()