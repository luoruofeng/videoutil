import cv2
import os

def save_frames_from_video(video_path, output_dir):
    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 打开视频文件
    cap = cv2.VideoCapture(video_path)
    frame_index = 1
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # 保存帧为图像文件
        frame_filename = os.path.join(output_dir, f"{frame_index}.jpg")
        print(frame_filename)
        cv2.imencode('.jpg', frame)[1].tofile(frame_filename)
        
        frame_index += 1
    
    cap.release()

def process_videos_in_directory(directory):
    # 遍历当前目录中的所有文件
    for filename in os.listdir(directory):
        if filename.endswith(".mp4"):
            video_path = os.path.join(directory, filename)
            output_dir = os.path.join(directory, os.path.splitext(filename)[0])
            save_frames_from_video(video_path, output_dir)

if __name__ == "__main__":
    current_directory = os.getcwd()
    process_videos_in_directory(current_directory)
