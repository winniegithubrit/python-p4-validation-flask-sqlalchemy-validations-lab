from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    @validates('name')
    def validate_name(self,key,name):
        if not name:
            raise ValueError('Authors name is not here hence required')
        if Author.query.filter(db.func.lower(Author.name) == name.lower()).first():
            raise ValueError('Author with the same name already exists in the database.')
        return name
    @validates('phone_number')
    def validate_phonenumber(self,key,phone_number):
        if phone_number and len(phone_number) !=10:
            raise ValueError('Authors phone number is not valid')
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    
    # @validates('title')
    # def validate_title(self, key, title):
    #     if not title:
    #         raise ValueError('Post title is not available and its needed.')
    #     return title
    
    @validates('title')
    def validate_title(self, key, title):
        clickbait_words = ["Bummer", "Setter", "Gena"]
        if not any(word in title for word in clickbait_words):
            raise ValueError("Title should not contain clickbait.")
        return title

    
    @validates('content')
    def validate_content(self, key, content):
        if content and len(content) < 250:
            raise ValueError('Post content must be at least 250 characters long.')
        return content
    
    @validates('summary')
    def validate_summary(self, key, summary):
        if summary and len(summary) > 250:
            raise ValueError('Post summary cannot go beyond 250 characters.')
        return summary
    
    @validates('category')
    def validate_category(self, key, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError('Post category must be either Fiction or Non-Fiction.')
        return category
    



    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
