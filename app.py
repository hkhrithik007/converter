
from flask import Flask, render_template, request, send_file
from PIL import Image
from moviepy.editor import VideoFileClip
import io
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/convert-video", methods=["POST"])
def convert_video():
    video = request.files["video"]
    output_format = request.form["video_format"].lower()
    filename = secure_filename(video.filename)
    temp_input = f"temp_input_{filename}"
    temp_output = f"temp_output.{output_format}"
    video.save(temp_input)

    clip = VideoFileClip(temp_input)
    try:
        if output_format == "gif":
            clip.write_gif(temp_output)
            mime = "image/gif"
        elif output_format == "webm":
            clip.write_videofile(temp_output, codec="libvpx", audio_codec="libvorbis")
            mime = "video/webm"
        else:
            clip.write_videofile(temp_output, codec="libx264")
            mime = f"video/{output_format}"
    except Exception as e:
        clip.close()
        # Clean up temp input
        if os.path.exists(temp_input):
            os.remove(temp_input)
        # Return error message or 500 response
        return f"Video conversion failed: {str(e)}", 500

    clip.close()

    if not os.path.exists(temp_output):
        # Clean up temp input
        if os.path.exists(temp_input):
            os.remove(temp_input)
        return "Output video file was not created.", 500

    with open(temp_output, "rb") as f:
        data = io.BytesIO(f.read())

    # Clean up temp files
    if os.path.exists(temp_input):
        os.remove(temp_input)
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
    app.run(debug=True)
