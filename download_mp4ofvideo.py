import yt_dlp
import sys

def download_audio(video_url):
    ydl_opts = {
        'format': 'bestaudio/best',  # 只下载最好的音频格式
        'outtmpl': '%(title)s.%(ext)s',  # 输出文件名为视频标题
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',  # 转换为 mp3 格式
            'preferredquality': '192',  # mp3 音频质量 (例如 192 kbps)
        }],
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(video_url, download=True)
            audio_title = info_dict.get('title', None)
            print(f"Downloaded audio: {audio_title}.mp3")
        except yt_dlp.utils.DownloadError as e:
            print(f"Error downloading audio: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python download_audio.py <video_url>")
    else:
        video_url = sys.argv[1]
        download_audio(video_url)
