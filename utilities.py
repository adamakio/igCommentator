import os
import json


import logging
from instagrapi import Client, exceptions
from instagrapi.exceptions import LoginRequired


logger = logging.getLogger()

def login_user(USERNAME, PASSWORD) -> Client:
    """
    Attempts to login to Instagram using either the provided session information
    or the provided username and password.
    """

    cl = Client()
    cl.delay_range = [1, 3] # adds a random delay between 1 and 3 seconds after each request
    session = cl.load_settings("session.json") if os.path.exists("session.json") else None

    login_via_session = False
    login_via_pw = False

    if session:
        try:
            cl.set_settings(session)
            cl.login(USERNAME, PASSWORD)

            # check if session is valid
            try:
                cl.get_timeline_feed()
                login_via_session = True
            except LoginRequired:
                logger.info("Session is invalid, need to login via username and password")

                old_session = cl.get_settings()

                # use the same device uuids across logins
                cl.set_settings({})
                cl.set_uuids(old_session["uuids"])

                if cl.login(USERNAME, PASSWORD):
                    login_via_session = True
                    cl.dump_settings("session.json")
        except Exception as e:
            logger.info("Couldn't login user using session information: %s" % e)

    if not login_via_session:
        try:
            logger.info("Attempting to login via username and password. username: %s" % USERNAME)
            if cl.login(USERNAME, PASSWORD):
                login_via_pw = True
                cl.dump_settings("session.json")
        except Exception as e:
            logger.info("Couldn't login user using username and password: %s" % e)

    if not login_via_pw and not login_via_session:
        raise Exception("Couldn't login user with either password or session")
    
    return cl


def fetch_posts_from_hashtag(client : Client, hashtag, max_posts=20):
    """
    An iterator that yields post links from a specific hashtag.
    """
    posts = client.hashtag_medias_recent(hashtag, amount=max_posts)
    for post in posts:
        media = client.media_info(post.pk)
        yield media.id, media.caption_text


def save_commented_media_ids(media_ids, filename="commented_media_ids.json"):
    with open(filename, "w") as file:
        json.dump(list(media_ids), file)

def load_commented_media_ids(filename="commented_media_ids.json"):
    try:
        with open(filename, "r") as file:
            return set(json.load(file))
    except FileNotFoundError:
        return set()