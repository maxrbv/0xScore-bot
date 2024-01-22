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

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        for i, arg in enumerate(args):
            setattr(self, self.__table__.columns.keys()[i], arg)

    def __repr__(self):
        return (
            f"<Campaign("
            f"id={self.id}, "
            f"inner_id={self.inner_id}, "
            f"project_name='{self.project_name}', "
            f"image_url='{self.image_url}', "
            f"min_score={self.min_score}, "
            f"reward_points={self.reward_points}, "
            f"winners_count={self.winners_count}, "
            f"reward_text='{self.reward_text}', "
            f"twitter_url='{self.twitter_url}', "
            f"discord_url='{self.discord_url}', "
            f"site_url='{self.site_url}', "
            f"start_date={self.start_date}, "
            f"end_date={self.end_date}"
            f")>"
        )
