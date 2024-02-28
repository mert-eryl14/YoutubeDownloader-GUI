from sqlalchemy import create_engine, inspect, String, Float, Integer, select
from sqlalchemy.orm import DeclarativeBase, Session, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Video(Base):
    __tablename__ = 'videos'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    url: Mapped[str] = mapped_column(String(250), nullable=False)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    thumbnail: Mapped[str] = mapped_column(String(250), nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    size: Mapped[float] = mapped_column(Float, nullable=False)
    length: Mapped[float] = mapped_column(Float, nullable=False)
    type: Mapped[str] = mapped_column(String(250), nullable=False)

    def __repr__(self):
        return f"<Video Object: {self.title}>"


class DbManager:
    def __init__(self):
        self.db = create_engine("sqlite:///./db\\videos.db", echo=False)
        if not inspect(self.db).has_table('videos'):  # If table don't exist, Create.
            Base.metadata.tables["videos"].create(bind=self.db)

    def get_video_by_id(self, video_id):
        with Session(self.db) as session:
            video = session.get(Video, video_id)
        return video

    def get_video_by_title(self, video_title):
        with Session(self.db) as session:
            video = session.execute(select(Video).where(Video.title == video_title)).scalar()
        return video

    def get_all_videos(self):
        with Session(self.db) as session:
            videos = session.execute(select(Video).order_by(Video.id)).scalars().all()
        return videos

    def add_video(self, url: str, title: str, thumbnail: str, author: str, size: float, length: float, v_type: str):
        new_video = Video(
            url=url,
            title=f"{title}.{v_type}",
            thumbnail=thumbnail,
            author=author,
            size=size,
            length=length,
            type=v_type
        )
        with Session(bind=self.db) as session:
            session.add(new_video)
            session.commit()

    def delete_video(self, video: Video):
        with Session(self.db) as session:
            session.delete(video)
            session.commit()

    def update_db(self, all_downloads_in_dir):
        all_downloads_by_title = [download.split('\\')[-1] for download in all_downloads_in_dir]
        all_videos_in_db = self.get_all_videos()
        with Session(self.db) as session:
            for video in all_videos_in_db:
                if video.title not in all_downloads_by_title:
                    session.delete(video)
                    session.commit()
