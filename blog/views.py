from flask import render_template, request, redirect, url_for, flash
from flask.ext.login import login_user, login_required, current_user, logout_user, user_logged_in
from werkzeug.security import check_password_hash

from blog import app
from .database import session
from .models import Post, User

import mistune

@app.route("/")
@app.route("/page/<int:page>")
def posts(page=1, paginate_by=10):
    # Zero-indexed page
    page_index = page - 1

    count = session.query(Post).count()

    start = page_index * paginate_by
    end = start + paginate_by

    total_pages = (count - 1) / paginate_by + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0

    posts = session.query(Post)
    posts = posts.order_by(Post.datetime.desc())
    posts = posts[start:end]

    return render_template("posts.html",
        posts=posts,
        has_next=has_next,
        has_prev=has_prev,
        page=page,
        total_pages=total_pages
    )

@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = session.query(User).filter_by(email=email).first()
    user.user_logged_in = True
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))

    login_user(user)
    return redirect(request.args.get('next') or url_for("posts"))

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    user = current_user
    user.user_logged_in = False
    logout_user()
    return redirect(url_for("posts"))

@app.route("/post/add", methods=["GET"])
@login_required
def add_post_get():
    return render_template("add_post.html")

@app.route("/post/add", methods=["POST"])
@login_required
def add_post_post():
    post = Post(
        title=request.form["title"],
        content=mistune.markdown(request.form["content"]),
        author = current_user
    )
    session.add(post)
    session.commit()
    return redirect(url_for("posts"))

@app.route("/post/<id>", methods=["GET", "POST"])
def view_post(id):
    post = session.query(Post).get(id)
    return render_template("view_post.html", post=post)

@app.route("/post/<id>/edit", methods=["GET"])
@login_required
def edit_post_get(id):
    post = session.query(Post).get(id)
    return render_template("edit_post.html", post=post)

@app.route("/post/<id>/edit", methods=["GET", "POST"])
@login_required
def edit_post_post(id):
    post = session.query(Post).get(id)
    post.title=request.form["title"]
    post.content=mistune.markdown(request.form["content"])
    session.add(post)
    session.commit()
    return redirect(url_for("view_post", id=post.id))

@app.route("/post/<id>/delete", methods=["GET", "POST", "DELETE"])
@login_required
def delete_post(id):
    post = session.query(Post).get(id)
    session.delete(post)
    session.commit()
    return redirect(url_for("posts"))


