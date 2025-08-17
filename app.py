from flask import Flask, render_template, request, send_file
from pydub import AudioSegment
from PIL import Image
from moviepy.editor import VideoFileClip
import io
import os
from werkzeug.utils import secure_filename

pillow_heif.register_heif_opener()
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/convert-audio", methods=["POST"])
def convert_audio():
    audio = request.files["audio"]
    output_format = request.form["audio_format"].lower()
    filename = secure_filename(audio.filename)
    temp_input = f"temp_input_{filename}"
    temp_output = f"temp_output.{output_format}"
    audio.save(temp_input)
    try:
        song = AudioSegment.from_file(temp_input)
        song.export(temp_output, format=output_format)
        out_data = io.BytesIO(open(temp_output, "rb").read())
    finally:
        if os.path.exists(temp_input):
            os.remove(temp_input)
        if os.path.exists(temp_output):
            os.remove(temp_output)
    out_data.seek(0)
    mime = f"audio/{'mpeg' if output_format=='mp3' else output_format}"
    return send_file(
        out_data,
        mimetype=mime,
        as_attachment=True,
        download_name=f"converted.{output_format}",
    )


@app.route("/convert-image", methods=["POST"])
def convert_image():
    img = request.files["image"]
    output_format = request.form["format"].lower()
    im = Image.open(img)  # Will now open .heic files, thanks to pillow-heif
    img_io = io.BytesIO()
    im.save(img_io, output_format.upper())
    img_io.seek(0)
    return send_file(
        img_io,
        mimetype=f"image/{output_format}",
        as_attachment=True,
        download_name=f"converted.{output_format}",
    )


@app.route("/convert-video", methods=["POST"])
def convert_video():
    video = request.files["video"]
    output_format = request.form["video_format"].lower()
    filename = secure_filename(video.filename)
    temp_input = f"temp_input_{filename}"
    temp_output = f"temp_output.{output_format}"
    video.save(temp_input)

    clip = VideoFileClip(temp_input)
    mime = None
    try:
        if output_format == "gif":
            clip.write_gif(temp_output)
            mime = "image/gif"
        elif output_format == "webm":
            clip.write_videofile(temp_output, codec="libvpx", audio_codec="libvorbis")
            mime = "video/webm"
        else:
            # Use libx264 for mp4/avi/mov, add audio_codec for mp4
            audio_codec = "aac" if output_format in ("mp4", "mov", "m4v") else None
            clip.write_videofile(temp_output, codec="libx264", audio_codec=audio_codec)
            mime = f"video/{output_format}"
    except Exception as e:
        return f"Video conversion failed: {str(e)}", 500
    finally:
        clip.close()
        if os.path.exists(temp_input):
            os.remove(temp_input)

    if not os.path.exists(temp_output):
        return "Output video file was not created.", 500

    with open(temp_output, "rb") as f:
        data = io.BytesIO(f.read())
    if os.path.exists(temp_output):
        os.remove(temp_output)

    data.seek(0)
    return send_file(
        data,
        mimetype=mime,
        as_attachment=True,
        download_name=f"converted.{output_format}",
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
