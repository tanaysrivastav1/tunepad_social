import os
import secrets
from PIL import Image
from flask import current_app, flash,redirect, url_for
from web_package.models import ProjectLibrary

# function to genreate the unquie and limit the size for profile 
# pictures and artworks
def helper_save_pic(pic, root):
    _, ext = os.path.splitext(pic.filename)
    pic_file_name = secrets.token_hex(8) + ext
    pic_path_name = os.path.join(current_app.root_path, root, pic_file_name)
    my_pic = Image.open(pic).convert('RGB')
    if root == 'static/profile_pics':
        output_size = (225, 225)
    else:
        output_size = (800, 800)
    my_pic.thumbnail(output_size)
    my_pic.save(pic_path_name)
    return pic_file_name

# function to print all the hashtags in a text 
def helper_extract_hashtags(text, make_string=False):  
    # initializing hashtag_list variable 
    hashtag_list = [] 
    # splitting the text into words 
    for word in text.split(): 
        # checking the first charcter of every word 
        if word[0] == '#': 
            # adding the word to the hashtag_list 
            hashtag_list.append(word[1:]) 
    # make it into a string so we can search it
    if make_string:
        hashtag_list = ','.join(hashtag_list)
    return hashtag_list

# def helper_check_project_id(project_id):
#     if not ProjectLibrary.query.filter_by(project_id=project_id).first():
#         for _ in range(100):
#             print('helloooo')
#         flash('invalid project id!', 'danger')
#         return redirect(url_for('post')) 
#     else: 
#         return project_id

# function to print all the hashtags in a text 
# def helper_extract_hashtags(text):  
    # initializing hashtag_list variable 
    # hashtag_list = [] 
    # splitting the text into words 
    # for word in text.split(): 
        # checking the first charcter of every word 
        # if word[0] == '#': 
            # adding the word to the hashtag_list 
            # hashtag_list.append(word[1:]) 
    # return hashtag_list