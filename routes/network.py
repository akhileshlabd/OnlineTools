from flask import Blueprint, render_template, request

network_bp = Blueprint('network', __name__, url_prefix='/network')

NETWORK_TOOLS = {
    'what-is-my-ip': {
        'id': 'what-is-my-ip',
        'name': 'What Is My IP?',
        'desc': 'Check your public IP address, location, and ISP details.',
        'icon': 'fa-network-wired',
        'seo_title': 'What Is My IP Address? - Free Public IP & Location Lookup',
        'seo_desc': 'Instantly find out your public IPv4/IPv6 address. Check your exact location, Internet Service Provider (ISP), and network details completely free.'
    }
}

@network_bp.route('/')
def network_hub():
    return render_template('hub_network.html', network_tools=NETWORK_TOOLS)

@network_bp.route('/tool/<tool_id>')
def network_tool_page(tool_id):
    tool = NETWORK_TOOLS.get(tool_id)
    if not tool:
        return "Network Tool not found", 404
        
    # Get basic IP from Flask as a fallback (handles proxies)
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if client_ip and ',' in client_ip:
        client_ip = client_ip.split(',')[0]
        
    return render_template('network_tool.html', tool=tool, client_ip=client_ip)
