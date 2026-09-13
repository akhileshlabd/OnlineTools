import sys

with open('routes/video.py', 'r') as f:
    content = f.read()

# I will just rewrite the whole file cleanly since it's short
new_content = """from flask import Blueprint, render_template, request

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
    }
]

@video_bp.route('/')
def video_hub():
    return render_template('hub_video.html', tools=VIDEO_TOOLS)

@video_bp.route('/mute-video')
def tool_mute():
    tool = next((t for t in VIDEO_TOOLS if t['id'] == 'mute'), None)
    return render_template('video_tool.html', tool=tool)

@video_bp.route('/trim-video')
def tool_trim():
    tool = next((t for t in VIDEO_TOOLS if t['id'] == 'trim'), None)
    return render_template('video_tool.html', tool=tool)

@video_bp.route('/convert-to-mp4')
def tool_convert_mp4():
    tool = next((t for t in VIDEO_TOOLS if t['id'] == 'convert_mp4'), None)
    return render_template('video_tool.html', tool=tool)
"""

with open('routes/video.py', 'w') as f:
    f.write(new_content)
