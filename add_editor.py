with open('templates/admin_dashboard.html', 'r') as f:
    content = f.read()

# Add Summernote CSS to head
head_tag = '</head>'
css_inject = """
    <link href="https://cdn.jsdelivr.net/npm/summernote@0.8.18/dist/summernote-lite.min.css" rel="stylesheet">
</head>
"""
if 'summernote' not in content:
    content = content.replace(head_tag, css_inject)

# Add jQuery and Summernote JS to bottom before script
script_tag = '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>'
js_inject = """
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/summernote@0.8.18/dist/summernote-lite.min.js"></script>
<script>
  $(document).ready(function() {
      $('#new_content').summernote({ height: 300, toolbar: [['style', ['style']], ['font', ['bold', 'underline', 'clear']], ['color', ['color']], ['para', ['ul', 'ol', 'paragraph']], ['insert', ['link', 'picture', 'video']], ['view', ['fullscreen', 'codeview', 'help']]] });
      $('#edit_content').summernote({ height: 300, toolbar: [['style', ['style']], ['font', ['bold', 'underline', 'clear']], ['color', ['color']], ['para', ['ul', 'ol', 'paragraph']], ['insert', ['link', 'picture', 'video']], ['view', ['fullscreen', 'codeview', 'help']]] });
  });
</script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
"""
if 'summernote-lite.min.js' not in content:
    content = content.replace(script_tag, js_inject)

# Update the JS value fetching
# document.getElementById('new_content').value  ->  $('#new_content').summernote('code')
content = content.replace("document.getElementById('new_content').value", "$('#new_content').summernote('code')")
content = content.replace("document.getElementById('edit_content').value", "$('#edit_content').summernote('code')")

# Update the modal open function to set summernote code
# document.getElementById('edit_content').value = content; -> $('#edit_content').summernote('code', content);
content = content.replace("document.getElementById('edit_content').value = content;", "$('#edit_content').summernote('code', content);")

with open('templates/admin_dashboard.html', 'w') as f:
    f.write(content)

