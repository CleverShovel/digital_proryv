from collections import Counter

from ultralytics import YOLO
import cv2

shot_model = YOLO('../artefacts/shots_detector_run2.pt')
shot_names = shot_model.names

waste_model = YOLO('../artefacts/waste_type_clf_m.pt')
waste_names = waste_model.names

def most_common(lst):
    data = Counter(lst)
    return data.most_common(1)[0][0]

def predict(video_file):
    prediction = None

    # Функция для конвертации времени в формате чч:мм:сс в количество секунд
    def convert_time_to_seconds(time_str):
        h, m, s = map(int, time_str.split(':'))
        return h * 3600 + m * 60 + s

    try:
        # Загрузите видео
        cap = cv2.VideoCapture(video_file)

        # Убедитесь, что видео было успешно загружено
        if not cap.isOpened():
            raise Exception("Error opening video file")

        fps = cap.get(cv2.CAP_PROP_FPS)      # OpenCV v2.x used "CV_CAP_PROP_FPS"
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count/fps

        if duration < 220:
            start_time = duration // 2 - 20
            end_time = duration // 2 + 20
        else:
            start_time = convert_time_to_seconds('00:01:40')
            end_time = convert_time_to_seconds('00:02:30')
        
        start_frame = int(start_time * fps)
        end_frame = int(end_time * fps)

        # Установите начальную позицию видео
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

        predictions = []
        
        i = 0
        step = 15
        # Читайте видео с начальной до конечной позиции
        while cap.get(cv2.CAP_PROP_POS_FRAMES) < end_frame:
            ret, frame = cap.read()
            # Проверьте, успешно ли прочитан кадр
            if not ret:
                break

            if i % step == 0:
                res = shot_model.predict(frame, verbose=False)[0].probs

                if shot_names[res.top1] == 'bad':
                    continue
                    
                res = waste_model.predict(frame, verbose=False)[0].probs
                predictions.append(res.top1)

            i += 1
        
        prediction = most_common(predictions)

        # Освободите захват видео и закройте все окна
        cap.release()
    except Exception as e:
        print(e)
        return 0
    cv2.destroyAllWindows()
    return prediction