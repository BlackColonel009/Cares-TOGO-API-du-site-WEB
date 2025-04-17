from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

# ✅ Table intermédiaire pour la relation Many-to-Many entre BlogPost et Category
blog_post_categories = Table(
    "blog_post_categories",
    Base.metadata,
    Column("blog_post_id", Integer, ForeignKey("blog_posts.id")),
    Column("category_id", Integer, ForeignKey("categories.id"))
)

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    blog_posts = relationship("BlogPost", secondary=blog_post_categories, back_populates="categories")
