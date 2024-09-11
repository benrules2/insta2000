from os import getenv
from datetime import datetime, timedelta
from instaloader import Instaloader, Profile, Hashtag
from itertools import takewhile, islice

class User:
    def __init__(self, username):
        self.username = username
        self.loader = Instaloader()
        self.loader.dirname_pattern = f"_{username}"
        self.loader.filename_pattern="{target}_{profile}_{date_utc}_UTC" 
        passwd_var = getenv("INSTAGRAM_PASSWORD", False)
        if passwd_var:
            self.loader.login(user=self.username, passwd=passwd_var)
        else:
            self.loader.interactive_login(self.username)
        self.loader.save_metadata = True 
        self.profile = Profile.from_username(self.loader.context, self.username)
        self.followees = None
        
    def get_followed_list(self):
        if not self.followees:
            self.followees = self.profile.get_followees()
        return [username for username in self.followees]
    
    def get_hashtag_posts(self, hashtags, days = 7, store = True):
        # Currently broken in instaloader 
        # https://github.com/instaloader/instaloader/issues/2144

        until = datetime.now()
        since = until - timedelta(days=days)

        for hashtag in hashtags:
            print(f"Fetching posts for hashtag: {hashtag}")
            hashtag_obj = Hashtag.from_name(self.loader.context, hashtag)
            hashtag_posts = hashtag_obj.get_top_posts()

            # Filter posts based on the time window and limit to top N
            filtered_posts = takewhile(lambda p: since < p.date_utc < until, hashtag_posts)
            top_n_posts = islice(filtered_posts, self.top_n)

            for post in top_n_posts:
                print(f"Post date: {post.date_utc}, Post ID: {post.shortcode}")
                
                if store:
                    self.loader.download_post(post, target=f":hashtag")

    def check_updates(self, store=True, days=14, public_only=False):
        feed_posts = self.loader.get_feed_posts()
        stories = self.loader.get_stories()

        if store:
            until = datetime.now()
            since = until - timedelta(days=days)
            for post in takewhile(lambda p: p.date_utc < until and p.date_utc > since, feed_posts):
                if public_only and not post.is_public:
                    print(f"Skipping private post from {post.date}")
                else:
                    print(f"Downloading {'public' if post.is_public else 'private'} post from {post.date}")
                    self.loader.download_post(post, target=":feed")                
                print(post.date)
                self.loader.download_post(post, target=":feed")
            self.loader.download_stories(fast_update=True)

        return feed_posts, stories
        
if __name__ == "__main__":
    username = getenv("INSTAGRAM_USERNAME")
    user = User(username)
    feed, stories = user.check_updates()
    print(f"{username} updates {feed}")
