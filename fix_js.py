with open('templates/admin_dashboard.html', 'r') as f:
    content = f.read()

content = content.replace("$('#edit_content').summernote('code') = content;", "$('#edit_content').summernote('code', content);")

with open('templates/admin_dashboard.html', 'w') as f:
    f.write(content)
