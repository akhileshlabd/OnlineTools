with open('templates/blog_post.html', 'r') as f:
    content = f.read()
content = content.replace('{{ blog.content }}', '{{ blog.content | safe }}')
with open('templates/blog_post.html', 'w') as f:
    f.write(content)

with open('templates/blog_hub.html', 'r') as f:
    content = f.read()
content = content.replace('{{ blog.content[:150] }}...', '{{ blog.content | striptags | truncate(150) }}')
with open('templates/blog_hub.html', 'w') as f:
    f.write(content)

with open('templates/admin_dashboard.html', 'r') as f:
    content = f.read()
content = content.replace('{{ blog.content[:200] }}...', '{{ blog.content | striptags | truncate(200) }}')
with open('templates/admin_dashboard.html', 'w') as f:
    f.write(content)
