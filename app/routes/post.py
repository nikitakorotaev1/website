from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from ..extensions import db
from ..models.post import Post

post = Blueprint('post', __name__)

@post.route('/', methods=['POST', 'GET'])
def all():
    posts = Post.query.all()
    return render_template('post/all.html', posts=posts)


def check_admin():
    if not current_user.is_authenticated or current_user.role.title != 'Админ':
        return redirect(url_for('post.all'))


# Функция создания поста на сайте

@post.route('/post/create', methods=['POST', 'GET'])
@login_required
def create():

    admin_check = check_admin()

    if admin_check:
        return admin_check

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

# @post.route('/post/<int:post_id>', methods=['POST', 'GET'])
# def post():
#     post = Pos

@post.route('/post/<int:post_id>')
def post_details(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post/posts.html', post=post)



@post.route('/post/<int:post_id>/edit', methods=['POST', 'GET'])
@login_required
def edit_post(post_id):

    admin_check = check_admin()
    if admin_check:
        return admin_check

    post = Post.query.get_or_404(post_id)

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        created_at = request.form.get('created_at')
        image_url = request.form.get('image_url')
        video_url = request.form.get('video_url')

        post.title = title
        post.content = content
        post.created_at = created_at
        post.image_url = image_url
        post.video_url = video_url


        try:
            db.session.commit()
            print('Пост обновлён')
            return redirect(url_for('post.post_details', post_id=post.id))
        except Exception as e:
            print(f"Ошибка при добавлении поста: {str(e)}")
            db.session.rollback()

    return render_template('post/edit.html', post=post)


@post.route('/post/<int:post_id>/delete', methods=['POST', 'GET'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    admin_check = check_admin()
    if admin_check:
        return admin_check


    try:
        db.session.delete(post)
        db.session.commit()
        print('Пост удалён')
        flash('Пост удалён')
        return redirect(url_for('post.all'))
    except Exception as e:
        print(f"Ошибка при удалении поста: {str(e)}")
        flash('При удалении поста произошлв ошибка')
        db.session.rollback()
        return redirect(url_for('post.post_details', post_id=post.id))
