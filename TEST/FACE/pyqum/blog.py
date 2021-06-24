# Loading Basics
from colorama import init, Back, Fore
init(autoreset=True) #to convert termcolor to wins color
from os.path import basename as bs
myname = bs(__file__).split('.')[0] # This py-script's name

from keyboard import press
import json, time, random, itertools, glob
from flask import (
    Flask, Blueprint, flash, g, redirect, render_template, request, url_for, Response, jsonify,
    stream_with_context
)
from werkzeug.exceptions import abort

from pyqum.auth import login_required
from pyqum import get_db, close_db

bp = Blueprint(myname, __name__) # to create endpoint for {{url_for(blog.XXX)}}

@bp.route('/')
def index():
    """render index.html"""
    return render_template('blog/index.html')
@bp.route('/basecolor')
def basecolor(): 
    return jsonify(base_color=g.base_color)

@bp.route('/reset')
def reset():
    '''simulate press-enter-key in cmd to clear the possible clog!'''
    # press('enter')
    return jsonify(message='OK')

@bp.route('/posts')
def posts():
    """Show all the posts, most recent first."""
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id' # join tables to link (id in user) and (author_id in post) to get username
        ' ORDER BY modified DESC' # ordered by modified
    ).fetchall()
    close_db()
    # JSON-Serialization:
    posts = [dict(p) for p in posts] # if (g.user['id'] == p['author_id'])] # convert sqlite3.row into list of dictionaries

    if g.user is None:
        guserid = g.user
    else:
        guserid = g.user['id']

    return jsonify(posts=posts,guserid=guserid)

def get_post(id, check_author=True):
    """Get a post and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    db = get_db()
    post = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()
    close_db()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """Create a new post for the current user."""
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            close_db()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    """Update a post if the current user is the author."""
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?, modified = ? WHERE id = ?',
                (title, body, time.strftime('%Y-%m-%d %H:%M:%S'), id)
            )
            db.commit()
            close_db()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    close_db()
    return redirect(url_for('blog.index'))


print(Back.BLUE + Fore.CYAN + myname + ".bp registered!") # leave 2 lines blank before this
