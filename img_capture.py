import cv2

cap = cv2.VideoCapture(0)

# 引入Opencv訓練好的偵測臉部模型(haarcascade_frontalface_default.xml)
cascade_path = 'C:/Users/user/PycharmProjects/Auto-Check_in-System/File/haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(cascade_path)

# 輸入使用者ID(從1到...) ps.請輸入連續整數
input_flag = True
while input_flag:
    face_Id = input('Enter user ID(Integer) :')
    if not face_Id.isnumeric():
        print("Input Type Error, Please input again!")
        continue
    input_flag = False
    print("User data are inputting, Please look at the camera and wait...")

# 計算存取幾張照片
count = 0

while True:
    success, img = cap.read()
    if success:
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        break
    
    # 參數:detectMultiScale(img, scaleFactor:表示每次圖像尺寸減小的比例, minNeighbors:表示每一個目標至少要被檢測到n次才算是真的目標)
    faces = face_cascade.detectMultiScale(gray_img, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)

        # 存取數加一
        count += 1
        # 拍下並存取照片
        cv2.imwrite('C:/Users/user/PycharmProjects/Auto-Check_in-System/taining_img/User.' + str(face_Id) + '.' + str(count)+'.jpg'
                    ,gray_img[y : y+h, x : x+w])
        cv2.waitKey(10)
        cv2.imshow("Face", img)

    k = cv2.waitKey(1)

    # 超過900張就完成
    if count >= 900:
        break
    cv2.imshow("img", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
        