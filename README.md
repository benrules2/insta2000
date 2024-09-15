# insta2000

## Overview

These days, reading social media feeds is a constant barrage of infinite scrolling, intrusive discovery algorithms, and annoying ads. `insta2000` simplifies this experience by using [Instaloader](https://instaloader.github.io/) to scrape a user's Instagram posts and stories for a specific date range, allowing you to focus only on real updates from people you know.

The content is re-rendered on a locally hosted website with a delightful retro throwback design, without the distractions and chaff of modern social media. It also reorders your feed by users, sorted by their most recent updates. 

Here is a sample of the past day of public posts from my own network: 

![demo](/insta2000/assets/demo_insta_2000_4k.gif)


## Important Note

DISCLAIMER: While this project operates within my interpretation Instagram's Terms of Service (TOS), Instagram may not approve. There is a risk that your account could be flagged or banned. Use at your own risk! I personally haven't faced any issues, but accept the possibility of account loss.

## Getting Started

**Clone the Repository**  
   ```bash
   git clone https://github.com/yourusername/insta2000.git
   cd insta2000
   ```

**Create your python environment** 

```bash
python -m venv venv 
venv/bin/activate 
pip install -r requirements.txt 
```

**Create a .env file containing your username and password**
See sample.env for required variables to be set. 
Copy this to a file called `.env` and fill your own values in. 


**Run the script**
Once env vars and python is setup, you can simply run this command from the root directory.

`python insta2000/main.py`

This will run for a few minutes - polling and downloading your feed and stories within the instagram
rate limit constraints. Once finished, it will serve your website from the local url http://localhost:2000/index.html 

**Optional args:** 

- `--days` : Number of days to gather posts from, suggestin between 1-14 
- `--website_only` : Only render the webpage and start the served, do not scrape 
- `--public_only` : Only scrape public posts (useful for demos) 


# Contributing 

This project is a proof-of-concept but would be fun to expand on! I'm open to suggestions and collaborations. Feel free to open issues or start a discussion! If there's enough interest, I can create a Discord server for more interactive discussions.

If you want to contribute, please:

1. Fork the repository.
2. Create a new branch for your feature (git checkout -b feature-branch).
3. Submit a pull request (PR) with a description of your changes.
