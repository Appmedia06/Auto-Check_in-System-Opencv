import cv2
import input_excel_module 

# 利用LBPH(Local Binary Patterns Histogram)取得各照片的像素的資料
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('C:/Users/user/PycharmProjects/Auto-Check_in-System/trainner/trainner.yml')

# 引入Opencv訓練好的偵測臉部模型(haarcascade_frontalface_default.xml)
cascade_path = 'C:/Users/user/PycharmProjects/Auto-Check_in-System/File/haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(cascade_path)

# 輸入有幾人以認證
people_Num = int(input("How many people have been identified? "))

# 輸入使用者名稱
user_Names = []
print("\nEnter the name that has been identified by Face: ")
for x in range(1, people_Num + 1):
    user_Names.append(input("User"+ str(x) +"'s name: "))

# 限制的flag
flagList = []
for x in range(0, people_Num):
    flagList.append(False)

keyList = []
for x in range(0, people_Num):
    keyList.append(0)

presentList = []
for x in range(0, people_Num):
    presentList.append(0)

# 取得鏡頭
cap = cv2.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)


while True:
    success, img = cap.read()
    if success:

        # 轉灰階圖片
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 參數:detectMultiScale(img, scaleFactor:表示每次圖像尺寸減小的比例, minNeighbors:表示每一個目標至少要被檢測到n次才算是真的目標)
        faces = face_cascade.detectMultiScale(gray_img, scaleFactor=1.2, minNeighbors=5)

        # 若有偵測到人臉
        if len(faces) > 0:
            keyId = 0
            id = ""
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3)
                # 取得前面訓練集匹配的人臉識別的標籤label和信賴值(越小越準，最小到0)
                id, confidence = recognizer.predict(gray_img[y:y+h, x:x+w])
                
                # 取到小數點第1位
                confidence = round(confidence, 1)
                # 拿100減得到正常百分比值
                cofidence = 100 - float(confidence)

                # 判斷是否有意外事件
                if confidence < 100:
                    keyId = id #判斷誰加入印出的值
                    id = user_Names[id - 1]
                # 未知的設成"unknown"
                else:
                    id = "unknown"

                # 限制的flag
                for i in range(1, people_Num + 1):
                    if keyId == i:
                        flagList[i - 1] = True

                # 使用者ID跟Confidence
                cv2.putText(img, str(id), (x+5, y-10), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(img, f'{str(confidence)}%', (x+w-30, y+h+10)
                            , cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0 ,255), 2)

            # 若信賴度大於55%，印出使用者打卡成功
            if confidence > 55:
                if id == user_Names[keyId - 1]: # 確認是否在名單中
                    if keyList[keyId - 1] == 0: # 確保只印一次出席成功
                        if flagList[keyId - 1] == True: # 確認有偵測到對應ID的臉
                            keyList[keyId - 1] = 1
                            print("[" + str(id)+ " identify successfully! Check in OK!!!]")
                            presentList[keyId - 1] = 1

                        
        else:
            flag1 = False
            flag2 = False
            flag3 = False
            key1 = 0
            key2 = 0
            key3 = 0

        cv2.imshow("img", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# 印出打卡出席結果
print("\n###############################")
print("\nToday's attendance results : \n{")
for x in range(0, people_Num):
    if presentList[x] == 1:
        print(user_Names[x] + " has checked in.")
    else:
        print(user_Names[x] + " didn't check in.")
print("}")

# 關閉視窗
cap.release()
cv2.destroyAllWindows()

# 建立寫入Excel物件
print("[INFO] Input the name of Excel file: ")
excel_name = input("==> ")

enter_excel = input_excel_module.Input_to_Excel(peopleNum=people_Num)
enter_excel.inputData(user_Names, presentList)
enter_excel.decorate_table()
enter_excel.save_Excel(excel_name)