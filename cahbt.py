import re
import random
import twitter
import json
import time
import logging
import sys
import config


SETTINGS = {'since_id': None}
MAX_TWEET_LENGTH = 140
BOT_NAME = "cahbt"

white_cards = []
black_cards = []

BLANK = "____"

api = twitter.Api(config.consumer_key,
                  config.consumer_secret,
                  config.access_token_key,
                  config.access_token_secret)


def load_cards():
    global white_cards, black_cards
    with open("cards/black.txt") as f:
        black_cards = [l.strip() for l in f.readlines() if l.strip()]

    with open("cards/white.txt") as f:
        white_cards = [l.strip() for l in f.readlines() if l.strip()]


def setup_logging():
    log_format = '%(asctime)s %(levelname)s %(message)s'
    formatter = logging.Formatter(log_format)
    logging.basicConfig(filename='cahbt.log', level=logging.INFO, format=log_format)
    soh = logging.StreamHandler(sys.stdout)
    soh.setLevel(logging.DEBUG)
    soh.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(soh)


def load_settings():
    global SETTINGS
    try:
        f = open('settings.json')
        SETTINGS = json.loads(f.read())
        f.close()
    except IOError:
        logging.warning("Could not load settings.json")


def save_settings():
    global SETTINGS
    f = open('settings.json', 'w')
    f.write(json.dumps(SETTINGS))
    f.close()


def clean_text(text):
    text = text.replace("..", ".")
    text = text.replace(".?", "?")
    text = text.replace(".:", ":")
    text = text.replace("\r\n", " -")
    text = text.strip()
    return text


def reply(status):
    text = re.sub("_+", BLANK, status.text)
    text = text.replace("@%s" % BOT_NAME, "")

    item_count = max(1, text.count(BLANK))

    for i in range(0, int(item_count)):
        white_card = random.choice(white_cards).strip()
        white_card = white_card.strip('.')
        if BLANK in text:
            text = text.replace(BLANK, white_card, 1)
        else:
            text = text + "- " + white_card

    text = clean_text(text)
    tweet = u"@%s %s" % (status.user.screen_name, text)
    logging.info(tweet.encode('utf8'))

    if len(tweet) > MAX_TWEET_LENGTH:
        tweet = tweet[:MAX_TWEET_LENGTH - 2] + u".."

    try:
        api.PostUpdate(tweet, in_reply_to_status_id=status.id)
    except Exception, e:
        logging.exception("Failed to tweet update: %s" % str(e))


setup_logging()
load_cards()
load_settings()


running = True
while running:
    logging.info("Fetching new mentions..")
    statuses = api.GetMentions(since_id=SETTINGS['since_id'])
    for status in statuses:
        # Check if we already replied to it, or if it's too old
        if status.user.screen_name == BOT_NAME:
            continue
        print status.user.name
        print status.user.screen_name
        if '__' in status.text:
            reply(status)

        SETTINGS['since_id'] = status.id
        save_settings()

    logging.info("Sleeping..")
    time.sleep(30)
