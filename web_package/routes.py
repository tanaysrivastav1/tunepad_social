import base64
from flask import render_template, redirect, url_for, flash, request, jsonify, make_response, abort, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import func
from web_package import app, db, bcrypt
from web_package.forms import RegisterForm, LoginForm, PostForm
from web_package.models import User, Post, TestPost, ProjectLibrary
from web_package.helpers import helper_save_pic, helper_extract_hashtags


#troubleshooting: https://stackoverflow.com/questions/37307346/is-the-server-running-on-host-localhost-1-and-accepting-tcp-ip-connections
# home - see all the chat

#get the posts to show on home
@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
@login_required
def home():
    posts = Post.query.all()
    print(posts)
    return render_template('home.html', posts=posts)

# search for a specific post
@app.route('/search')
@login_required
def search():
    # form = SearchForm()
    keyword = str(request.args.get('query')).lower()
    # search by title and description
    # Model.query.filter(Model.columnName.contains('sub_string'))
    contain_description = func.lower(Post.description).contains(keyword)
    contain_title = func.lower(Post.title).contains(keyword)
    post_posts = Post.query.filter(contain_description | contain_title).all()

    # search by username
    user = User.query.filter(User.username.contains(keyword)).all()
    user_posts = sum(list(map(lambda i: i.post, user)), [])

    # combine search
    posts = list(set(post_posts + user_posts))
    return render_template('home.html', posts=posts)

# register page
@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf8')
        if form.profile_pic.data:
            try: 
                profile_pic = helper_save_pic(form.profile_pic.data, 'static/profile_pics')
            except:
                flash('picture is an invalid picture!', 'danger')
                return redirect(url_for('register'))
            # create a new user with a custom profile pic
            new_user = User(username=form.username.data, email=form.email.data, password=hash_password, profile_pic=profile_pic)
        # else just use default profile pic
        else:
            new_user = User(username=form.username.data, email=form.email.data, password=hash_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# login page
@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user_exist = User.query.filter_by(username=form.username.data).first()
        if user_exist:
            correct_key = bcrypt.check_password_hash(user_exist.password, form.password.data)
            if correct_key:
                to_login_user = user_exist
                login_user(to_login_user)
                try_page = request.args.get('next')
                flash('welcome', 'success')
                return redirect(try_page) if try_page else redirect(url_for('home'))
            else:
                flash('wrong password', 'danger')
        else:
            flash('wrong username', 'danger')
    return render_template('login.html', form=form)

# upload the post
@app.route('/post', methods=['POST', 'GET'])
@login_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        # initilize 
        title = form.title.data
        description = form.description.data
        #add tags textbox in html
        tags = helper_extract_hashtags(description)
        #have project_id equal input from site 
        project_id = form.project_id.data
        # tags_text = helper_extract_hashtags(description, make_string=True)
        user_id = current_user.id
        print(title, description, tags, project_id)
        #if you didn't get ANY projuct id, then error
        if not project_id:
            flash('invalid project id!', 'danger')
            return redirect(url_for('post')) 
        
        # if there is an artwork add an artwork to the post
        if form.artwork.data:
            # catch the exception
            try: 
                artwork = helper_save_pic(form.artwork.data, 'static/artwork_pics')
            except:
                flash('picture is an invalid picture!', 'danger')
                return redirect(url_for('post')) 
            # create a new  post
            new_post = Post(title=title, tags=tags, description=description, artwork=artwork, user_id=user_id, project_id=project_id)
        # else do not add an artwork
        else:
            new_post = Post(title=title, tags=tags, description=description, user_id=user_id, project_id=project_id)        
        # add a new post to a database
        db.session.add(new_post)
        db.session.commit()
        flash('you just post!', 'success')
        return redirect(url_for('home')) 
    return render_template('post.html', form=form)

@app.route('/post/<post_id>')
@login_required
def lookup_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    return render_template('lookup_post.html', post=post)

@app.route('/userpost/<username>')
@login_required
def lookup_user_post(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(user=user).order_by(Post.date.desc()).all()
    return render_template('home.html', posts=posts)

@app.route('/tagpost/<tag>')
@login_required
def lookup_tag_post(tag):
    posts = Post.query.filter(func.lower(Post.description).contains(tag.lower())).all()
    return render_template('home.html', posts=posts)

# logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# like
@app.route('/like/<post_id>/<action>')
def like(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
        post.like_count = post.likes.count()
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()
        post.like_count = post.likes.count()
        db.session.commit()
    return jsonify({'likes':post.likes.count()})


# test
def decodeAudioFile(audiodata):
    header, data = audiodata.split(',')
    print(header)
    if header and data:
        ctype, encoding = header.split(';')
        if ctype[0:10] == 'data:audio' and encoding == 'base64':
            ctype = ctype[5:]
            response = make_response(base64.b64decode(data))
            response.headers['Content-Type'] = ctype
            return response
    return None

# @app.route('/library/project/audio/<int:project_id>', methods=['GET'])
@app.route('/library/<project_id>', methods=['GET'])
def libraryProjectAudioPreview(project_id):
    # project = db_session.query(ProjectLibrary).get({ "id" : id })
    project = ProjectLibrary.query.filter_by(project_id=project_id).first()
    if not project: abort(404)
    response = None
    if project and project.preview:
        response = decodeAudioFile(project.preview)
    if response:
        return response
    else:
        abort(404)

@app.route('/rawdata', methods=['GET'])
def getRawData():
    data = {}
    data["post"] = "my post"
    data["comment"] = "this is a cool post"
    
    return jsonify(data)

    