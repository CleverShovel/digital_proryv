import cv2

import os

from tqdm import tqdm

# Функция для конвертации времени в формате чч:мм:сс в количество секунд
def convert_time_to_seconds(time_str):
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s

# Создайте директорию для сохранения кадров, если она еще не существует
frames_dir = '../data/extracted_frames_2'
os.makedirs(frames_dir, exist_ok=True)

train_dir = os.path.join(os.getcwd(), os.pardir, 'data/train')

folders = os.listdir(train_dir)
folders.sort()

not_skip = 4

for folder in folders:
    video_files = os.listdir(os.path.join(train_dir, folder))
    video_files = [vf for idx, vf in enumerate(video_files) if idx % not_skip == 0]
    for video_file in tqdm(video_files):
        try:
            # Загрузите видео
            video_path = os.path.join(train_dir, folder, video_file)
            cap = cv2.VideoCapture(video_path)

            # Убедитесь, что видео было успешно загружено
            if not cap.isOpened():
                raise Exception("Error opening video file")

            # Получите частоту кадров видео
            fps = cap.get(cv2.CAP_PROP_FPS)

            # Вычислите номера кадров для начального и конечного времени
            start_time = convert_time_to_seconds('00:00:40')
            end_time = convert_time_to_seconds('00:03:20')
            start_frame = int(start_time * fps)
            end_frame = int(end_time * fps)

            # Установите начальную позицию видео
            cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

            i = 0
            step = 50
            # Читайте видео с начальной до конечной позиции
            while cap.get(cv2.CAP_PROP_POS_FRAMES) < end_frame:
                ret, frame = cap.read()
                # Проверьте, успешно ли прочитан кадр
                if not ret:
                    break

                if i % step == 0:
                    # Сохраните кадр
                    frame_number = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                    frame_name = os.path.join(frames_dir, f'{os.path.split(video_file)[1]}_frame_{frame_number}.jpg')
                    if os.path.exists(frame_name):
                        break
                    cv2.imwrite(frame_name, frame)
                    
                
                i += 1

            # Освободите захват видео и закройте все окна
            cap.release()
        except Exception:
            pass
cv2.destroyAllWindows()