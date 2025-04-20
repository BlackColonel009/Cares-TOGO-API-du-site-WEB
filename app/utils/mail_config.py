from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
import os

load_dotenv()

class MailSettings(BaseModel):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr
    MAIL_FROM_NAME: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_STARTTLS: bool
    MAIL_SSL_TLS: bool

settings = MailSettings(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_FROM_NAME=os.getenv("MAIL_FROM_NAME"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=os.getenv("MAIL_STARTTLS") == "True",
    MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS") == "True"
)

conf = ConnectionConfig(**settings.dict())

async def send_contact_email(name: str, email: EmailStr, subject: str, message: str):
    html = f"""
    <h3>Message de Contact CARES TOGO</h3>
    <p><strong>Nom :</strong> {name}</p>
    <p><strong>Email :</strong> {email}</p>
    <p><strong>Sujet :</strong> {subject}</p>
    <p><strong>Message :</strong><br>{message}</p>
    """

    msg = MessageSchema(
        subject=f"[CARES TOGO] Nouveau message : {subject}",
        recipients=[os.getenv("MAIL_FROM")],
        body=html,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(msg)

async def send_newsletter_welcome_email(email: EmailStr):
    html = f"""
    <h3>Bienvenue dans la communauté CARES TOGO !</h3>
    <p>Merci de vous être inscrit à notre newsletter.</p>
    <p>Nous vous tiendrons informé(e) des nouveautés, événements et publications.</p>
    """

    msg = MessageSchema(
        subject="Bienvenue sur CARES TOGO 🎉",
        recipients=[email],
        body=html,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(msg)

