import os
import time
import random
import datetime
import utilities
import commenter

from dotenv import load_dotenv

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Get Instagram credentials from environment variables
    USERNAME = os.getenv('INSTAGRAM_USERNAME')
    PASSWORD = os.getenv('INSTAGRAM_PASSWORD')
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # Initialize the OpenAI client
    openai_client = commenter.openai_login(OPENAI_API_KEY)

    # Initialize the Instagram client
    ig_client = utilities.login_user(USERNAME, PASSWORD)

    # Keep track of the number of comments posted today
    comment_count = 0
    last_comment_date = datetime.date.today()
    commented_media_ids = utilities.load_commented_media_ids()

    while comment_count <= 20:
        current_date = datetime.date.today()
        if current_date > last_comment_date:
            comment_count = 0
            last_comment_date = current_date

        for media_id, caption in utilities.fetch_posts_from_hashtag(ig_client, "cars"):
            if media_id in commented_media_ids:
                continue  # Skip if already commented on this media_id

            try:
                # Comment using caption
                comment_text = commenter.comment(openai_client, caption)
                ig_client.media_comment(media_id, comment_text)
                comment_count += 1
                commented_media_ids.add(media_id)  # Add media_id to the set
                        
                print(f"Comment posted on media id {media_id}:\n{comment_text}")
                
                utilities.save_commented_media_ids(commented_media_ids) # Save the commented media ids to a file
            except Exception as e:
                print(f"Failed to comment on post: {e}")

            if comment_count == 20:
                # Wait until the next day
                comment_count = 0
                last_comment_date = current_date
                time_to_wait = (datetime.datetime.combine(current_date + datetime.timedelta(days=1), datetime.datetime.min.time()) - datetime.datetime.now()).total_seconds()
                print(f"Comment limit reached. Waiting for {time_to_wait} seconds (until next day).")
                time.sleep(time_to_wait)
                continue

            # Wait to respect the API rate limit
            time.sleep(30)  # 120 requests per hour < Limit of 200 requests per hour

        

        # Wait for 5-10 minutes before fetching again
        time_to_wait = random.randint(300, 600)
        print(f"Waiting for {time_to_wait} seconds before fetching again.")
        time.sleep(time_to_wait)
          

if __name__ == "__main__":
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print("Script terminated by user. Press enter to exit or c to continue...")
            user_input = input()
            if user_input == "c":
                continue
            else:
                exit()
            
