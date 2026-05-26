from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from app import db
from app.models import Post, Comment
from app.forms import PostForm, CommentForm

posts = Blueprint('posts', __name__)

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, location=form.location.data, event_time=form.event_time.data,
                    organizer=form.organizer.data, description=form.description.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New post', form=form, legend='New post')

@posts.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('You need to login to comment.', 'error')
            return redirect(url_for('auth.login'))
        comment = Comment(content=form.content.data, author=current_user, post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash('Comment added!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    return render_template('post.html', title=post.title, post=post, form=form)

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.location = form.location.data
        post.event_time = form.event_time.data
        post.organizer = form.organizer.data
        post.description = form.description.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.location.data = post.location
        form.event_time.data = post.event_time
        form.organizer.data = post.organizer
        form.description.data = post.description
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))

@posts.route("/post/myposts", methods=['GET', 'POST'])
@login_required
def myposts():
    search_query = request.args.get('search')
    if search_query:
        posts = Post.query.filter_by(author=current_user).filter(Post.title.ilike(f'%{search_query}%') | Post.location.ilike(f'%{search_query}%')).order_by(Post.date_posted.desc()).all()
    else:
        posts = Post.query.filter_by(author=current_user).order_by(Post.date_posted.desc()).all()
    return render_template('my_posts.html', posts=posts, search_query=search_query)

@posts.route("/post/mycomments", methods=['GET', 'POST'])
@login_required
def mycomments():
    comments = Comment.query.filter_by(author=current_user).order_by(Comment.date_posted.desc()).all()
    return render_template('my_comments.html', comments=comments)

