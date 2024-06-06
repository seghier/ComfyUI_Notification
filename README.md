## Step-by-Step Implementation with Gmail

1. **Generate an App Password**:
   - Go to your Google Account settings.
   - Navigate to "Security" and then "App passwords".
   - Choose "Mail" and "Other (custom name)".
   - Follow the prompts to generate a 16-character password.

2. **Enable Less Secure Apps** (Optional but not recommended for main accounts):
   - Go to your Google Account settings.
   - Navigate to "Security".
   - Turn on "Less secure app access".

3. **Install Necessary Libraries**:
   - Make sure you have `smtplib` and `email` libraries installed. If not, install them using pip:
     ```
     pip install secure-smtplib
     pip install email
     ```
     or
     ```
     pip install -r requirements.txt
     ```

## Plug VAE Decode output image to the node

![image](https://github.com/seghier/ComfyUI_Email_Notification/assets/6026588/c0495771-2b04-475a-a7a5-8817531d6706)


![image](https://github.com/seghier/ComfyUI_Email_Notification/assets/6026588/8fc11211-74cd-4599-a5ad-11560c11b787)


## Step-by-Step Implementation with Telegram Bot

1. **Create a Telegram Bot**:
   - Open the Telegram app and search for "BotFather" (official Telegram bot for managing bots).
   - Start a chat with BotFather.
   - Type `/newbot` and send the message.
   - Follow the instructions to choose a name and username for your bot. The username must end in "bot" (e.g., MyComfyUIBot).
   - After creating the bot, BotFather will provide you with an HTTP API token. This token is required to send messages using your bot.

2. **Get Your Chat ID**:
   - Find your bot by searching for its username in Telegram.
   - Start a chat with your bot by clicking "Start".
   - To get your chat ID, you can send a message to your bot and then use the Telegram API to get your chat ID.
     - Open a web browser and navigate to:
       ```
       https://api.telegram.org/bot<YourBotToken>/getUpdates
       ```
       Replace `<YourBotToken>` with the token you received from BotFather.
     - Look for the `chat` object in the response. Your chat ID will be listed as `id`.

![image](https://github.com/seghier/ComfyUI_Email_Notification/assets/6026588/eee81ab1-4048-4bfc-8638-3216026b918a)
