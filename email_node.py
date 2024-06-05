import torch
from PIL import Image, ImageOps
from io import BytesIO
import numpy as np
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Define the function to send emails using Gmail's SMTP server with image attachment
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
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        img = MIMEImage(img_byte_arr.read(), name="result_image.png")
        msg.attach(img)

    # Send the email
    server.send_message(msg)
    server.quit()
    
def resize_image(images):
    img = images[0]
    img_np = 255. * img.cpu().numpy()
    img_pil = Image.fromarray(np.clip(img_np, 0, 255).astype(np.uint8))
    # Resize the image to the desired size
    width = 400
    height = int(img_pil.height * (width / img_pil.width))
    img_pil_resized = img_pil.resize((width, height))
    return img_pil_resized
    
# Define the EmailNode class with proper input types
class EmailNode:
    def __init__(self):
        super().__init__()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "trigger_image": ("IMAGE",),
                "from_email": ("STRING", {"multiline": False}),
                "to_email": ("STRING", {"multiline": False}),
                "subject" : ("STRING", {"default": "Queue Finished", "multiline": False}),
                "password": ("STRING", {"multiline": False}),
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
            body = "The queue processing has been completed."
            send_email(to_email, subject, body, from_email, password, image)
            return "Email sent successfully"
        return "No trigger image provided"


# Define node mappings for ComfyUI
NODE_CLASS_MAPPINGS = {
    "EmailNode": EmailNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmailNode": "Email Notification",
}
