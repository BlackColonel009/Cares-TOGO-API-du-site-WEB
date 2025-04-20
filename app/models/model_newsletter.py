from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class NewsletterSubscriber(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "newsletter_subscribers"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    subscribed_at = Column(DateTime, default=datetime.utcnow)
