import streamlit as st
from PIL import Image
import cv2
import numpy as np
from config import CLASSES, COLORS
from settings import DEFAULT_CONFIDENCE_THRESHOLD, DEMO_IMAGE #, MODEL, PROTOTXT

st.write("""
# Определение типа мусора \u267B\uFE0F
""")

def process_image(image):
    blob = cv2.dnn.blobFromImage(
        cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5
    )
    #net = cv2.dnn.readNetFromCaffe(PROTOTXT, MODEL)
    #net.setInput(blob)
    #detections = net.forward()
    return blob


@st.cache_data 
def annotate_image(
    image, detections, confidence_threshold=DEFAULT_CONFIDENCE_THRESHOLD
):
    # loop over the detections
    (h, w) = image.shape[:2]
    labels = []
    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > confidence_threshold:
            # extract the index of the class label from the `detections`,
            # then compute the (x, y)-coordinates of the bounding box for
            # the object
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # display the prediction
            label = f"{CLASSES[idx]}: {round(confidence * 100, 2)}%"
            labels.append(label)
            cv2.rectangle(image, (startX, startY), (endX, endY), COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(
                image, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2
            )
    return image, labels


img_file_buffer = st.file_uploader("Загрузить фото или видео", type=["png", "jpg", "jpeg", "mp4"])
confidence_threshold = st.slider(
    "Confidence threshold", 0.0, 1.0, DEFAULT_CONFIDENCE_THRESHOLD, 0.05
)

st.write(f'Фоточка с камеры:')
if img_file_buffer is not None:
    image = np.array(Image.open(img_file_buffer))

else:
    demo_image = DEMO_IMAGE
    image = np.array(Image.open(demo_image))

detections = process_image(image)
image, labels = annotate_image(image, detections, confidence_threshold)
labels = 'Грунт'
st.image(
    image, caption=f"Красивая фоточка с камеры", use_column_width=True,
)

st.write(f'Похоже, привезли {labels}')
if labels == 'Дерево':
    st.image(Image.open("images/tree.jpg").resize((100,100)), use_column_width=False
)

if labels == 'Бетон':
    st.image(Image.open("images/concrete.jpg").resize((100,100)), use_column_width=False
)

if labels == 'Кирпич':
    st.image(Image.open("images/brick.png").resize((100,100)), use_column_width=False
)

if labels == 'Грунт':
    st.image(Image.open("images/sand.jpg").resize((100,100)), use_column_width=False
)
