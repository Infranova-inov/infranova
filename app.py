from flask import Flask, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

FFMPEG_PATH = r"C:\Users\sceptix\Desktop\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe"

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    format_type = request.args.get('format', 'mp4')

    if not url:
        return "Aucune URL fournie", 400

    output_dir = "downloads"
    os.makedirs(output_dir, exist_ok=True)

    try:
        # Extraire le titre de la vidéo
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'video').replace("/", "_").replace("\\", "_")
    except Exception as e:
        return f"Erreur pendant l'extraction : {str(e)}", 500

    clean_title = f"infranovadowloaderfree - {title}"
    full_output = os.path.join(output_dir, clean_title + ".%(ext)s")

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': full_output,
        'ffmpeg_location': FFMPEG_PATH,
    }

    if format_type == "mp3":
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }]
        extension = ".mp3"
    else:
        extension = ".mp4"

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        final_path = os.path.join(output_dir, clean_title + extension)
        if not os.path.exists(final_path):
            return "Fichier non généré.", 500

        return send_file(final_path, as_attachment=True)

    except Exception as e:
        return f"Erreur : {str(e)}", 500

if __name__ == '__main__':
    app.run(port=5000)
