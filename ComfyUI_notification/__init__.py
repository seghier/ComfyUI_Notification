from .notification_node import EmailNode, TelegramNode

NODE_CLASS_MAPPINGS = {
    "EmailNode": EmailNode,
    "TelegramNode": TelegramNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmailNode": "Email Notification",
    "TelegramNode": "Telegram Notification",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]