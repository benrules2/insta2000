import os
import re
import webbrowser
import datetime as dt
from pathlib import Path
from collections import defaultdict
from http.server import SimpleHTTPRequestHandler, HTTPServer


# Function to parse the type (feed or story), username, and datetime from the filename
def parse_filename(filename):
    match = re.match(r'^:?([a-z]+)_(\w+)_(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})_UTC', filename)
    if match:
        file_type = match.group(1)
        username = match.group(2)
        datetime = match.group(3)
        return file_type, username, datetime
    return None, None, None

class WebpageGenerator:
    def __init__(self, directory, posts_per_page=10):
        self.directory = directory
        self.posts_per_page = posts_per_page
        self.users = defaultdict(list)
        self.html_files = []

    def write_cheesy_background(self, f, page):
        f.write('<!DOCTYPE html>\n')
        f.write('<html lang="en">\n')
        f.write('<head>\n')
        f.write('    <meta charset="UTF-8">\n')
        f.write('    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
        f.write(f"    <title>Instagram 2000: Page {page}</title>\n")
        f.write('    <style>\n')
        f.write('        body { font-family: Comic Sans MS, sans-serif; background-image: url("insta2000/assets/background.png"); background-repeat: repeat; background-color: #000; }\n')
        f.write('        .header-section { background-color: yellow; padding: 20px; text-align: center; }\n')  
        f.write('        .header-section h1 { color: #ff00ff; font-size: 70px; margin: 0; }\n') 
        f.write('        .header-section .sponsor { font-size: 40px; color: blue; margin-top: 10px; }\n') 
        f.write('        .header-section .sponsor a { color: blue; text-decoration: underline; }\n')  
        f.write('        .user-section { border: 5px solid lime; padding: 20px; margin-bottom: 50px; background-color: #ff00ff; color: #00ffff; text-align: center; box-shadow: 5px 5px 10px #000; }\n')
        f.write('        .user-header { font-size: 40px; color: blue; font-weight: bold; text-align: center; margin-bottom: 20px; }\n')
        f.write('        .user-posts-container { background-color: yellow; padding: 10px; margin-bottom: 20px; }\n')
        f.write('        .post { background-color: yellow; padding: 10px; margin-bottom: 20px; }\n')
        f.write('        img, video { max-width: 100%; height: auto; border: 5px solid blue; }\n')
        f.write('        h3 { color: red; }\n')
        f.write('        .caption { color: blue; font-size: 18px; text-shadow: 2px 2px 5px red; }\n')
        f.write('    </style>\n')
        f.write('</head>\n')
        f.write('<body>\n')
        f.write('<div class="header-section">\n')  # Start header section
        f.write('<h1>INSTAGRAM 2000!</h1>\n')
        f.write('<div class="sponsor">\n')
        f.write('    Sponsored by <a href="http://www.sandwichtshirts.com" target="_blank">sandwichtshirts.com</a>\n')
        f.write('</div>\n')
        f.write('</div>\n')  # End header section


    def load_posts(self):
        # Loop through the directory and group files by username
        for filename in os.listdir(self.directory):
            file_path = os.path.join(self.directory, filename)
            file_type, username, datetime = parse_filename(filename)

            if file_type and username and datetime:
                post_key = f"{username}_{datetime}"

                if filename.endswith('.txt'):
                    with open(file_path, 'r') as text_file:
                        text_content = text_file.read()
                        self.users[username].append({'type': 'text', 'content': text_content, 'datetime': datetime})
                elif filename.endswith('.jpg'):
                    paired_mp4 = filename.replace('.jpg', '.mp4')
                    is_thumbnail = os.path.exists(f"{self.directory}/{paired_mp4}")
                    self.users[username].append({'type': 'image', 'content': file_path, 'datetime': datetime, "is_thumbnail": is_thumbnail})
                elif filename.endswith('.mp4'):
                    self.users[username].append({'type': 'video', 'content': file_path, 'datetime': datetime})

        # Sort posts by datetime for each user
        for username in self.users:
            self.users[username].sort(key=lambda x: dt.datetime.strptime(x['datetime'], "%Y-%m-%d_%H-%M-%S"), reverse=True)

    def write_html_page(self, posts, page_num, total_pages):
        page_file = self.html_files[page_num - 1]
        with open(page_file, 'w') as f:
            self.write_cheesy_background(f, page_num)

            # Add pagination navigation
            if page_num > 1:
                f.write(f'<a href="{self.html_files[page_num - 2].name}" style="font-size: 50px; color:blue; background-color: white;">Previous</a>\n')
            if page_num < total_pages:
                f.write(f'<a href="{self.html_files[page_num].name}" style="font-size: 50px; color: blue; background-color: white; float: right;">Next</a>\n')

            # Write posts to this page
            for username, content_list in posts.items():
                # Start the user section container with a shared background
                f.write(f'<div class="user-section">\n')
                f.write(f'<div class="user-header">{username}</div>\n')

                # Add a common block to group the user's posts together
                f.write(f'<div class="user-posts-container">\n')  # New wrapper for user's posts

                post_count = len(content_list)
                max_visible_posts = 3

                for idx, content in enumerate(content_list):

                    #skip thumbnails
                    if content['type'] == 'image' and content['is_thumbnail']:
                        continue

                    # Show only the first 3 posts, the rest will be collapsed
                    display_style = "block" if idx < max_visible_posts else "none"
                    f.write(f'<div class="post" style="display: {display_style};" id="{username}_post_{idx}">\n')
                    f.write(f'<h3>Posted on {content["datetime"]}</h3>\n')
                    if content['type'] == 'image':
                        f.write(f'<img src="{content["content"]}" alt="Post from {username}">\n')
                    elif content['type'] == 'video':
                        f.write(f'<video controls>\n')
                        f.write(f'    <source src="{content["content"]}" type="video/mp4">\n')
                        f.write('    Your browser does not support the video tag.\n')
                        f.write('</video>\n')
                    elif content['type'] == 'text':
                        f.write(f'<p class="caption">{content["content"]}</p>\n')
                    f.write('</div>\n')

                # Close the user's posts container
                f.write(f'</div>\n')  # Close the user-posts-container div

                # If there are more than 3 posts, add a "Load more" button
                if post_count > max_visible_posts:
                    f.write(f'<button onclick="showMorePosts(\'{username}\', {post_count})">Load more</button>\n')

                f.write('</div>\n')  # Close the user-section div

            # Add pagination at the bottom
            if page_num > 1:
                f.write(f'<a href="{self.html_files[page_num - 2].name}" style="font-size: 50px; color: blue; background-color: white;">Previous</a>\n')
            if page_num < total_pages:
                f.write(f'<a href="{self.html_files[page_num].name}" style="font-size: 50px; color: blue; float: right; background-color: white;">Next</a>\n')

            # Add JavaScript for "Load more" functionality
            f.write('''
            <script>
            function showMorePosts(username, postCount) {
                for (let i = 3; i < postCount; i++) {
                    document.getElementById(username + "_post_" + i).style.display = "block";
                }
                // Hide the load more button after showing all posts
                event.target.style.display = "none";
            }
            </script>
            ''')

        return page_file


    def generate_html(self):
        self.load_posts()

        # Pagination setup
        current_post_count = 0
        total_posts = sum(len(content_list) for content_list in self.users.values())
        total_pages = (total_posts // self.posts_per_page) + (total_posts % self.posts_per_page > 0)

        for page_num in range(1, total_pages + 1):
            if page_num - 1 == 0:
                page_file = Path(f'index.html')
            else:
                page_file = Path(f'index_page_{page_num}.html')
            self.html_files.append(page_file)

        page_posts = defaultdict(list)
        page_number = 1

        # Split posts into pages
        for username, content_list in self.users.items():
            for content in content_list:
                if current_post_count == self.posts_per_page:
                    self.write_html_page(page_posts, page_number, total_pages)
                    page_number += 1
                    page_posts = defaultdict(list)
                    current_post_count = 0

                page_posts[username].append(content)
                current_post_count += 1

        # Write any remaining posts to the last page
        if current_post_count > 0:
            self.write_html_page(page_posts, page_number, total_pages)

    def serve_static_site(self, port=2000):
        PORT = port
        server_address = ("", PORT)
        handler = SimpleHTTPRequestHandler

        # Open the web browser to the first HTML page
        webbrowser.open(f'http://localhost:{PORT}/{self.html_files[0].name}')

        # Start the server
        with HTTPServer(server_address, handler) as httpd:
            print(f"Serving on http://localhost:{PORT}")
            httpd.serve_forever()

    def generate_and_serve(self):
        self.generate_html()
        print(f'Static HTML pages generated: {", ".join([str(f.resolve()) for f in self.html_files])}')
        self.serve_static_site()


if __name__ == "__main__":
    directory = f"_{os.getenv('INSTAGRAM_USERNAME')}"
    generator = WebpageGenerator(directory=directory)
    generator.generate_and_serve()
