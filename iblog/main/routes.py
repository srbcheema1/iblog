from flask import render_template, request, Blueprint

from iblog.models import Post
from iblog.const import per_page
from iblog.utils import prefix

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=per_page)
    return render_template('home.html', posts=posts,prefix=prefix)


@main.route("/about")
def about():
    return render_template('about.html', title='About')
