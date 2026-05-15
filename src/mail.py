from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from src.config import my_config
from pathlib import Path
import os

THE_BASE_DIR = Path(__file__).resolve().parent
the_folder_path = os.path.join(THE_BASE_DIR, "the_attachments")

the_attachments = [
    os.path.join(the_folder_path, file) for file in os.listdir(the_folder_path)
]

the_config = ConnectionConfig(
    MAIL_USERNAME=my_config.MAIL_USERNAME,
    MAIL_PASSWORD=my_config.MAIL_PASSWORD,
    MAIL_FROM=my_config.MAIL_FROM,
    MAIL_PORT=my_config.MAIL_PORT,
    MAIL_SERVER=my_config.MAIL_SERVER,
    MAIL_FROM_NAME=my_config.MAIL_FROM_NAME,
    MAIL_STARTTLS=my_config.MAIL_STARTTLS,
    MAIL_SSL_TLS=my_config.MAIL_SSL_TLS,
    USE_CREDENTIALS=my_config.USE_CREDENTIALS,
    VALIDATE_CERTS=my_config.VALIDATE_CERTS,
    TEMPLATE_FOLDER=Path(THE_BASE_DIR, "the_templates"),
)

the_mail = FastMail(config=the_config)


def create_the_message(the_recipients: list[str], the_subject: str, the_body: str):
    the_message = MessageSchema(
        recipients=the_recipients,
        subject=the_subject,
        # body= the_body,
        subtype=MessageType.html,
        attachments=the_attachments,
        template_body={"name": "Abdullah"},
    )

    return the_message


def create_verification_message(
    the_recipients: list[str],
    the_subject: str,
    the_name: str,
    the_link: str,
):
    ver_message = MessageSchema(
        recipients=the_recipients,
        subject=the_subject,
        subtype=MessageType.html,
        template_body={"name": the_name, "link": the_link},
    )

    return ver_message


def create_password_reset_message(
    the_recipients: list[str],
    the_subject: str,
    the_link: str,
):
    pass_reset_message = MessageSchema(
        recipients=the_recipients,
        subject=the_subject,
        subtype=MessageType.html,
        template_body={"link": the_link},
    )

    return pass_reset_message
