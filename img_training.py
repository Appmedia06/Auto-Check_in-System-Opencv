import cv2
import os
import numpy as np
from PIL import Image

# 圖片檔的資料夾
img_path = r'C:/Users/user/PycharmProjects/Auto-Check_in-System/taining_img/'

# 利用LBPH(Local Binary Patterns Histogram)取得各照片的像素的資料
recognizer = cv2.face.LBPHFaceRecognizer_create()

# 引入Opencv訓練好的偵測臉部模型(haarcascade_frontalface_default.xml)
detector = cv2.CascadeClassifier('C:/Users/user/PycharmProjects/Auto-Check_in-System/File/haarcascade_frontalface_default.xml')

# 取得臉部資料和標籤
def get_Img_and_Label(path):

    # 取得照片列表
    image_paths = [os.path.join(path, f) for f in os.listdir(path)]

    
    face_samples = []
    ids = []

    for image_path in image_paths:
        # 打開圖片並轉回灰階圖像
        img = Image.open(image_path).convert('L')
        
        # 取得照片陣列
        img_np = np.array(img, 'uint8')

        # 例外處理:如果有非照片時，無視並繼續迴圈
        if os.path.split(image_path)[-1].split(".")[-1] != "jpg":
            continue
        
        # 獲得臉部資料及ID
        id = int(os.path.split(image_path)[-1].split(".")[1]) # 利用路徑分割得知照片為甚麼ID
        faces = detector.detectMultiScale(img_np)

        for (x, y, w, h) in faces:
            face_samples.append(img_np[y:y+h, x:x+w])
            ids.append(id)

    return face_samples, ids

print("\n [INFO] Training face. It will take few second. Wait... [INFO]")
# 取得臉部資料和標籤
face, ids = get_Img_and_Label(img_path)
# 訓練拿到的臉部資料和ID
recognizer.train(face, np.array(ids))
# 儲存在trainner folder裡
recognizer.save('C:/Users/user/PycharmProjects/Auto-Check_in-System/trainner/trainner.yml')
print("\n [INFO] {} faces are Trained Successfully. Exited Program! [INFO]".format(len(np.unique(ids))))