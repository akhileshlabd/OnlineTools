with open('templates/sitemap.xml', 'r') as f:
    content = f.read()

blogs_block = """
    <!-- Blog Hub -->
    <url>
        <loc>{{ url_for('blogs.blog_hub', _external=True) }}</loc>
        <changefreq>daily</changefreq>
        <priority>0.9</priority>
    </url>

    <!-- SEO Blogs -->
    {% if blogs %}
    {% for blog in blogs %}
    <url>
        <loc>{{ url_for('blogs.view_blog', slug=blog['slug'], _external=True) }}</loc>
        <lastmod>{{ blog['created_at'][:10] }}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
    {% endfor %}
    {% endif %}
</urlset>"""

new_content = content.replace("</urlset>", blogs_block)

with open('templates/sitemap.xml', 'w') as f:
    f.write(new_content)
