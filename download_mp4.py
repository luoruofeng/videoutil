import yt_dlp
import sys

def download_video(video_url):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'outtmpl': '%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',  # 确保转换为 mp4 格式
        }],
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(video_url, download=True)
            video_title = info_dict.get('title', None)
            video_ext = info_dict.get('ext', None)
            print(f"Downloaded video: {video_title}.{video_ext}")
        except yt_dlp.utils.DownloadError as e:
            print(f"Error downloading video: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python download_video.py <video_url>")
    else:
        video_url = sys.argv[1]
        download_video(video_url)
