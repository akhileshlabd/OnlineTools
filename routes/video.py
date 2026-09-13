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
    },
    {
        "id": "trim",
        "name": "Trim Video",
        "desc": "Cut out a specific section of your video without losing quality.",
        "icon": "fa-cut",
        "url": "video.tool_trim"
    },
    {
        "id": "convert_mp4",
        "name": "Convert to MP4",
        "desc": "Convert MOV, MKV, or AVI files to standard MP4 format instantly.",
        "icon": "fa-exchange-alt",
        "url": "video.tool_convert_mp4"
    },
    {
        "id": "thumbnail",
        "name": "Extract Thumbnail",
        "desc": "Grab a high-quality JPG snapshot from your video.",
        "icon": "fa-image",
        "url": "video.tool_thumbnail"
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

@video_bp.route('/trim-video')
def tool_trim():
    tool = next((t for t in VIDEO_TOOLS if t['id'] == 'trim'), None)
    return render_template('video_tool.html', tool=tool)

@video_bp.route('/convert-to-mp4')
def tool_convert_mp4():
    tool = next((t for t in VIDEO_TOOLS if t['id'] == 'convert_mp4'), None)
    return render_template('video_tool.html', tool=tool)

@video_bp.route('/extract-thumbnail')
def tool_thumbnail():
    tool = next((t for t in VIDEO_TOOLS if t['id'] == 'thumbnail'), None)
    return render_template('video_tool.html', tool=tool)
