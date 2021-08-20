from datetime import datetime
from flask_login import UserMixin
from web_package import db, login_manager
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils.types.ltree import LtreeType
import uuid



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    # id = db.Column(db.Integer, primary_key=True)
    #UUID - unique string
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    anonymous = db.Column(db.Boolean, nullable=False, default=False)
    oauth_id = db.Column(db.Text)
    confirmed = db.Column(db.Boolean, default=False)
    validation_code = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    log_activity = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer)
    user_source = db.Column(db.JSON)
    

    # additional columns
    profile_pic = db.Column(db.String(20), nullable=False, default='default.jpg')
    post = db.relationship('Post', backref='user', lazy=True, primaryjoin="User.id == Post.user_id")
    liked = db.relationship('PostLike', foreign_keys='PostLike.user_id', backref='user', lazy='dynamic')
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self.username}, {self.email})'

    def like_post(self, post):
        if not self.has_liked_post(post):
            like = PostLike(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            PostLike.query.filter_by(user_id=self.id, post_id=post.id).delete()

    def has_liked_post(self, post):
        return PostLike.query.filter(PostLike.user_id==self.id, PostLike.post_id==post.id).count() > 0

class Post(db.Model):
    __tablename__ = 'post'
    __searchable__ = ['title', 'description']  #indexed fields

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tags = db.Column(db.JSON, nullable=False)
    description = db.Column(db.Text)
    artwork = db.Column(db.String(20), nullable=False, default='default.jpg')
    like_count = db.Column(db.Integer, nullable=False, default=0)
    likes = db.relationship('PostLike', backref='post', lazy='dynamic')
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project_library.project_id'), nullable=False)
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self.id}, {self.title})'

class TestPost(db.Model):
    __tablename__ = 'test_post'
    __searchable__ = ['title', 'tags_string', 'description']  

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tags = db.Column(db.JSON, nullable=False)
    tags_string = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    artwork = db.Column(db.String(20), nullable=False, default='default.jpg')
    like_count = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id}, {self.title})'

# create whoose index which requires an app and a model class
# wa.whoosh_index(app, Post)

class PostLike(db.Model):
    __tablename__ = 'post_like'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'))
    post_id = db.Column(UUID(as_uuid=True), db.ForeignKey('post.id'))


class ProjectLibrary(db.Model):
    __tablename__ = 'project_library'

    id = db.Column(db.Integer, primary_key=True)
    # i set primary key for project id in sqlpostgres tho not sure if it's right
    project_id = db.Column(db.Integer, unique=True)
    name = db.Column(db.String, nullable=False)
    summary = db.Column(db.Text, nullable=False, default='')
    tags = db.Column(db.JSON, nullable=False)
    tracks = db.Column(db.JSON)
    ordering = db.Column(LtreeType)
    categories = db.Column(db.JSON, nullable=False)
    exportdata = db.Column(db.JSON, nullable=False)
    mdata = db.Column(db.JSON, nullable=False)
    bars = db.Column(db.SmallInteger, nullable=False, default=20)
    duration = db.Column(db.Integer, nullable=False, default=0)
    tempo = db.Column(db.SmallInteger, nullable=False, default=90)
    meter = db.Column(db.String, nullable=False, default='4/4')
    key = db.Column(db.String, nullable=False, default='C major')
    color = db.Column(db.String, nullable=False, default='black')
    user_id = db.Column(UUID(as_uuid=True))
    username = db.Column(db.String, nullable=False, default='')
    artwork = db.Column(db.String)
    preview = db.Column(db.String)
    line_count = db.Column(db.Integer, nullable=False, default=0)
    play_count = db.Column(db.Integer, nullable=False, default=0)
    like_count = db.Column(db.Integer, nullable=False, default=0)
    star_count = db.Column(db.Integer, nullable=False, default=0)
    remix_count = db.Column(db.Integer, nullable=False, default=0)
    public = db.Column(db.Boolean, nullable=False, default=False)
    deleted = db.Column(db.Boolean, nullable=False, default=False)
    created = db.Column(db.DateTime, nullable=False)
    modified = db.Column(db.DateTime, nullable=False)

    # addtional column
    # post = db.relationship('Post', backref='user', lazy=True, primaryjoin="User.id == Post.user_id")
    post = db.relationship('Post', foreign_keys='Post.project_id', backref='project', lazy='dynamic')


    def __init__(self, json=None):
        if json: self.fromDict(json)

    def fromDict(self, json):
        if 'id' in json and json['id'] > 0: self.id = json['id']
        if 'project_id' in json: self.project_id = json['project_id']
        if 'name' in json: self.name = json['name']
        if 'summary' in json: self.summary = json['summary']
        if 'tags' in json: self.tags = json['tags']
        if 'tracks' in json: self.tracks = json['tracks']
        if 'ordering' in json: self.ordering = json['ordering']
        if 'categories' in json: self.categories = json['categories']
        if 'exportdata' in json: self.exportdata = json['exportdata']
        if 'mdata' in json: self.mdata = json['mdata']
        if 'bars' in json: self.bars = json['bars']
        if 'duration' in json: self.duration = json['duration']
        if 'tempo' in json: self.tempo = json['tempo']
        if 'meter' in json: self.meter = json['meter']
        if 'key' in json: self.key = json['key']
        if 'color' in json: self.color = json['color']
        if 'user_id' in json: self.user_id = json['user_id']
        if 'username' in json: self.username = json['username']
        if 'artwork' in json: self.artwork = json['artwork']
        if 'preview' in json: self.preview = json['preview']
        if 'line_count' in json: self.line_count = json['line_count']
        if 'play_count' in json: self.play_count = json['play_count']
        if 'like_count' in json: self.like_count = json['like_count']
        if 'star_count' in json: self.star_count = json['star_count']
        if 'remix_count' in json: self.remix_count = json['remix_count']
        if 'public' in json: self.public = json['public']
        if 'deleted' in json: self.deleted = json['deleted']
        if 'created' in json: self.created = json['created']
        if 'modified' in json: self.modified = json['modified']

    def __repr__(self):
        return "ProjectLibrary(id='%d',name='%s')" % (self.id, self.name)


