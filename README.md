
1) Set `server.py` as your entry point.
1) Create a new Telegram bot using [BotFather](https://t.me/botfather)
1) Store the bot token into a BOT_TOKEN environment variable
1) Create a SECRET_TOKEN and set it in the SECRET_TOKEN environment variable
1) Run the following curl substituting the appropriate variables:
    ```
    curl https://api.telegram.org/bot${BOT_TOKEN}/setWebhook
        -F "url=https://${CYCLIC_URL}/webhook/" \
        -F "secret_token=${SECRET_TOKEN}"
    ```
1) Check your bot's status: `https://api.telegram.org/bot${BOT_TOKEN}/getWebhookInfo`
