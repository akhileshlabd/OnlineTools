with open('templates/admin_dashboard.html', 'r') as f:
    content = f.read()

# The dangling {% endfor %} is right above </div> \n </div> \n </div> \n <!-- Create Blog Modal -->
# Let's just find `{% endfor %}\n            </div>\n            \n        </div>` and remove the `{% endfor %}`

content = content.replace('{% endfor %}\n            </div>\n            \n        </div>\n    </div>\n\n</div>\n\n<!-- Create Blog Modal -->', 
                          '</div>\n            \n        </div>\n    </div>\n\n</div>\n\n<!-- Create Blog Modal -->')

with open('templates/admin_dashboard.html', 'w') as f:
    f.write(content)
