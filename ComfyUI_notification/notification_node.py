import torch
from PIL import Image
from io import BytesIO
import numpy as np
import requests
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .settings import FROM_EMAIL, TO_EMAIL, PASSWORD, TELEGRAM_TOKEN, CHAT_ID

# Helper function to convert image to byte array
def convert_image_to_byte_array(image):
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr

# Function to send Telegram message with optional image
def send_telegram_message(token, chat_id, message, image=None):
    # Send the text message
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print("Failed to send message.")

    # If an image is provided, send it
    if image is not None:
        url = f"https://api.telegram.org/bot{token}/sendPhoto"
        files = {
            'photo': image
        }
        data = {
            'chat_id': chat_id,
        }
        response = requests.post(url, files=files, data=data)
        if response.status_code == 200:
            print("Photo sent successfully!")
        else:
            print("Failed to send photo.")

# Function to send email with optional image
def send_email(to_address, subject, body, from_address="your_email@gmail.com", password="your_app_password", image=None):
    # Set up the server
    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.starttls()
    server.login(from_address, password)

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Attach the image
    if image is not None:
        img = MIMEImage(image.read(), name="result_image.png")
        msg.attach(img)

    # Send the email
    server.send_message(msg)
    server.quit()

# Function to resize image
def resize_image(images):
    img = images[0]
    img_np = 255. * img.cpu().numpy()
    img_pil = Image.fromarray(np.clip(img_np, 0, 255).astype(np.uint8))
    # Resize the image to the desired size
    width = 400
    height = int(img_pil.height * (width / img_pil.width))
    img_pil_resized = img_pil.resize((width, height))
    return img_pil_resized

# Define EmailNode class
class EmailNode:
    def __init__(self):
        super().__init__()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "trigger_image": ("IMAGE",),
                "from_email": ("STRING", {"default": FROM_EMAIL, "multiline": False}),
                "to_email": ("STRING", {"default": TO_EMAIL, "multiline": False}),
                "subject": ("STRING", {"default": "Queue Finished", "multiline": False}),
                "password": ("STRING", {"default": PASSWORD, "multiline": False}),
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "execute"
    INPUT_NODE = True
    OUTPUT_NODE = True
    CATEGORY = "Notifications"

    @classmethod
    def IS_CHANGED(s, *args, **kwargs):
        return torch.rand(1).item()

    def execute(self, trigger_image, from_email, to_email, subject, password):
        if trigger_image is not None:
            image = resize_image(trigger_image)
            img_byte_arr = convert_image_to_byte_array(image)
            body = "The queue processing has been completed."
            send_email(to_email, subject, body, from_email, password, img_byte_arr)
            return "Email sent successfully"
        return "No trigger image provided"

# Define TelegramNode class
class TelegramNode:
    def __init__(self):
        super().__init__()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "trigger_image": ("IMAGE",),
                "telegram_token": ("STRING", {"default": TELEGRAM_TOKEN, "multiline": False}),
                "chat_id": ("STRING", {"default": CHAT_ID, "multiline": False}),
                "message": ("STRING", {"default": "Queue Finished", "multiline": False}),
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "execute"
    INPUT_NODE = True
    OUTPUT_NODE = True
    CATEGORY = "Notifications"

    @classmethod
    def IS_CHANGED(s, *args, **kwargs):
        return torch.rand(1).item()

    def execute(self, trigger_image, telegram_token, chat_id, message):
        if trigger_image is not None:
            image = resize_image(trigger_image)
            img_byte_arr = convert_image_to_byte_array(image)
            send_telegram_message(telegram_token, chat_id, message, img_byte_arr)
            return "Message and photo sent successfully"
        send_telegram_message(telegram_token, chat_id, message)
        return "Message sent successfully"

# Define node mappings for ComfyUI
NODE_CLASS_MAPPINGS = {
    "EmailNode": EmailNode,
    "TelegramNode": TelegramNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmailNode": "Email Notification",
    "TelegramNode": "Telegram Notification",
}
