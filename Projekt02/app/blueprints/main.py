from flask import Blueprint, render_template, request
from app.models import Post

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    search_query = request.args.get('search')
    if search_query:
        posts = Post.query.filter(Post.title.ilike(f'%{search_query}%') | Post.location.ilike(f'%{search_query}%')).order_by(Post.date_posted.desc()).all()
    else:
        posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('index.html', posts=posts, search_query=search_query)