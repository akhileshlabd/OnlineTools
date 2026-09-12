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
    },
    'speed-test': {
        'id': 'speed-test',
        'name': 'Internet Speed Test',
        'desc': 'Test your download speed instantly in your browser.',
        'icon': 'fa-tachometer-alt',
        'seo_title': 'Free Internet Speed Test - Check Your Download Speed',
        'seo_desc': 'Test your internet connection speed instantly. Our free browser-based speed test measures your download bandwidth without requiring flash or java.'
    },
    'dns-lookup': {
        'id': 'dns-lookup',
        'name': 'DNS Record Lookup',
        'desc': 'Find A, AAAA, CNAME, MX, and TXT records for any domain.',
        'icon': 'fa-server',
        'seo_title': 'DNS Record Lookup - Check Domain DNS Records',
        'seo_desc': 'Perform a free DNS lookup to find A, AAAA, CNAME, MX, and TXT records for any domain. Uses secure DNS-over-HTTPS.'
    },
    'browser-info': {
        'id': 'browser-info',
        'name': 'What Is My Browser?',
        'desc': 'View detailed information about your browser, OS, and device.',
        'icon': 'fa-laptop-code',
        'seo_title': 'What Is My Browser? - Free Device & Browser Info',
        'seo_desc': 'Instantly check your browser version, operating system, screen resolution, and user agent string.'
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
