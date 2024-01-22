from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Campaign(Base):
    __tablename__ = 'campaigns'

    id = Column(Integer, primary_key=True)
    inner_id = Column(Integer, nullable=False, unique=True)
    project_name = Column(String(length=250), nullable=True)
    image_url = Column(String(length=50), nullable=True)
    min_score = Column(Integer, nullable=True)
    reward_points = Column(Integer, nullable=True)
    winners_count = Column(Integer, nullable=True)
    reward_text = Column(String(length=250), nullable=True)
    twitter_url = Column(String(length=100), nullable=True)
    discord_url = Column(String(length=100), nullable=True)
    site_url = Column(String(length=100), nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
