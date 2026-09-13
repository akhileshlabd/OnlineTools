from flask import Blueprint, render_template, request

video_bp = Blueprint('video', __name__, url_prefix='/video')

VIDEO_TOOLS = [
    {
        "id": "mute",
        "name": "Mute Video",
        "desc": "Remove audio tracks from a video completely free in your browser.",
        "icon": "fa-volume-mute",
        "url": "video.tool_mute"
    },
    {
        "id": "extract_audio",
        "name": "Video to MP3",
        "desc": "Extract high-quality audio from your video files.",
        "icon": "fa-music",
        "url": "video.tool_extract_audio"
    }
]

@video_bp.route('/')
def video_hub():
    return render_template('hub_video.html', tools=VIDEO_TOOLS)

@video_bp.route('/mute-video')
def tool_mute():
    tool = next((t for t in VIDEO_TOOLS if t['id'] == 'mute'), None)
    return render_template('video_tool.html', tool=tool)

@video_bp.route('/extract-audio')
def tool_extract_audio():
    tool = next((t for t in VIDEO_TOOLS if t['id'] == 'extract_audio'), None)
    return render_template('video_tool.html', tool=tool)
