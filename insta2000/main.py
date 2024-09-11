import argparse 
import os 

from user import User
from display.webpage import WebpageGenerator
from dotenv import load_dotenv

def main(days, public_only, webpage_only):
    print("Loading env vars for INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD from .env")
    load_dotenv()
    if not webpage_only:
        user = User(os.getenv("INSTAGRAM_USERNAME"))
        user.check_updates(days=days, public_only=public_only)  
    generator = WebpageGenerator(directory=f"_{os.getenv('INSTAGRAM_USERNAME')}")
    generator.generate_and_serve()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check Instagram updates for a given number of days.")
    parser.add_argument('--days', type=int, default=7, help="Number of days to check for updates (default: 7)")
    parser.add_argument('--public-only', action='store_true', help="Download only public posts if set.")
    parser.add_argument('--webpage_only', action='store_true', help="Download only public posts if set.")


    args = parser.parse_args()

    main(days=args.days, public_only=args.public_only, webpage_only=args.webpage_only)
