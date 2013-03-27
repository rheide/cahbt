# Cards Against Humanity bot for Twitter

## What does it do?

Any time you mention this bot, it will reply to your tweet, filling in the blanks from randomly selected white cards.

As an example, tweet "@cahbt I like ___" and cahbt will reply to you with "@<yourname> I like All-you-can-eat-shrimp for $4.99".

## Running it

- Rename example_config.py to config.py
- Create a Twitter account and update your config.py with API info from https://dev.twitter.com
- Use get_access_token.py to get your access_token_key and access_token_secret
- Run the bot with cahbt.py (you may want to tweak BOT_NAME)
