from flask import Blueprint, render_template, request, redirect
from ..extensions import db
from ..models.post import Post

post = Blueprint('post', __name__)

@post.route('/', methods=['POST', 'GET'])
def all():
    return render_template('post/all.html')



# Функция создания поста на сайте
@post.route('/post/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        created_at = request.form.get('created_at')
        image_url = request.form.get('image_url')
        video_url = request.form.get('video_url')


        post = Post(title=title, content=content, created_at=created_at, image_url=image_url, video_url=video_url)
        print('Успешно добавлено ', post.title)


        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(str(e))
    else:
        return render_template('post/create.html')