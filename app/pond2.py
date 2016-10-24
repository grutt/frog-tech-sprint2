from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import time
import os
import sqlite3
import json

currentUser = 1

app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'pond.db'),
))
# app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

# interfaces
class JSONSerializable(object):
    def __repr__(self):
        return json.dumps(self.__dict__)

class User(JSONSerializable):
    def __init__(self, uid, name):
        self.uid = uid
        self.name = name

# standard getters
def userFactory(uid):
    db = get_db()
    db = db.cursor()
    db.execute("SELECT name \
    FROM users WHERE uid=?", [uid])
    one = db.fetchone()
    return User(uid, one[0])

class Respondent(JSONSerializable):
    def __init__(self, rid, name, details):
        self.rid = rid
        self.name = name
        self.details = details

# standard getters
def respondentFactory(rid):
    db = get_db()
    db = db.cursor()
    db.execute("SELECT name, description \
    FROM respondents WHERE rid=?", [rid])
    one = db.fetchone()
    return Respondent(rid, one[0], one[1])

# web handles
@app.route('/')
def dashboard():
    blurbs = []
    db = get_db()
    c = db.cursor()
    c.execute("SELECT bid, blurb, uid, rid, tid \
    FROM blurbs WHERE score > 0 ORDER BY score desc")
    blurbRows = c.fetchall()
    if len(blurbRows) > 0:
        for blurb in blurbRows:
            c.execute("SELECT tagType\
            FROM tags WHERE bid = ?", (blurb[0],))
            tagRows = c.fetchall()
            tags = []
            if len(tagRows) > 0:
                for t in tagRows:
                    tags.append(t[0])

            c.execute("SELECT blurb, uid, cid\
            FROM comments WHERE bid = ?", (blurb[0],))
            commentRows = c.fetchall()
            comments = []
            if len(commentRows) > 0:
                for comment in commentRows:
                    comments.append(Comment(
                        comment[2],
                        blurb[0],
                        comment[1],
                        comment[0]
                        ))
            blurbs.append(Blurb(
            blurb[0], respondentFactory(blurb[3]), blurb[2], blurb[4], blurb[1], comments, tags
            ))

    return render_template('dashboard.html', blurbs=blurbs, tags = getTagList())



class Highlight(JSONSerializable):
    def __init__(self, hid, bid, uid, string, score, comments, tags):
        self.hid = hid
        self.bid = bid
        self.uid = uid
        self.blurb = blurb
        self.comments = comments
        self.tags = tags

@app.route('/highlightsByTagType')
def highlightsByTagType():
    highlights = []
    db = get_db()
    c = db.cursor()
    c.execute("SELECT tagType \
    FROM tags")
    rows = c.fetchall()
    if len(rows) > 0:
        for row in rows:
            highlights.append(row[0])
    else:
        highlights = [-1]

    return str(highlights)

def getTagList():
        tags=[]
        db = get_db()
        c = db.cursor()
        c.execute("SELECT tagTypeid,name,color \
        FROM tagTypes")
        rows = c.fetchall()

        if len(rows) > 0:
            for row in rows:
                tags.append(TagType(row[0],row[1],row[2]))
        return tags


class TagType(JSONSerializable):
    def __init__(self, tagType, name, color):
        self.tagType = tagType
        self.name = name
        self.color = color

class Blurb(JSONSerializable):
    def __init__(self, bid, rid, uid, tid, blurb, comments, tags):
        self.bid = bid
        self.rid = rid
        self.uid = uid
        self.tid = tid
        self.blurb = blurb
        self.comments = comments
        self.tags = tags

class Transcript(JSONSerializable):
    def __init__(self, tid, rid, uid, blurbs):
        self.tid = tid
        self.rid = rid
        self.uid = uid
        self.blurbs = blurbs



@app.route('/respondent')
def respondent():
    r = respondentFactory(request.args.get('rid'))
    blurbs = []
    db = get_db()
    c = db.cursor()
    c.execute("SELECT tid, uid \
    FROM transcripts WHERE rid = ?", r.rid)
    rows = c.fetchall()
    if len(rows) > 0:
        for row in rows:
            tid = row[0]
            uid = row[1]
            c.execute("SELECT bid, blurb, uid, rid \
            FROM blurbs WHERE tid = ?", (tid,))
            blurbRows = c.fetchall()
            if len(rows) > 0:
                for blurb in blurbRows:
                    c.execute("SELECT tagType\
                    FROM tags WHERE bid = ?", (blurb[0],))
                    tagRows = c.fetchall()
                    tags = []
                    if len(tagRows) > 0:
                        for t in tagRows:
                            tags.append(t[0])

                    c.execute("SELECT blurb, uid, cid\
                    FROM comments WHERE bid = ?", (blurb[0],))
                    commentRows = c.fetchall()
                    comments = []
                    if len(commentRows) > 0:
                        for comment in commentRows:
                            comments.append(Comment(
                                comment[2],
                                blurb[0],
                                comment[1],
                                comment[0]
                                ))
                    blurbs.append(Blurb(
                    blurb[0], blurb[3], blurb[2], row[0], blurb[1], comments, tags
                    ))


    return render_template('respondentOverview.html',
     respondent = r,
     transcript = Transcript(tid, r.rid, uid, blurbs),
     tags = getTagList()
     )


class Comment(JSONSerializable):
    def __init__(self, cid, bid, uid, blurb):
        self.cid = cid
        self.bid = bid
        self.uid = uid
        self.blurb = blurb
        self.user = userFactory(uid)




@app.route('/postComment', methods=['POST','GET'])
def postComment():
    blurb = request.values.get('blurb')
    bid = int(request.values.get('bid'))

    db = get_db()
    c = db.cursor()

    c.execute('insert into comments \
    (bid, uid, blurb) values (?,?,?);',
    (bid,currentUser,blurb))

    db.commit()

    return json.dumps({"bid":c.lastrowid, "blurb":blurb, "uid":currentUser, "name":userFactory(currentUser).name})
    db.close()


class Tag(JSONSerializable):
    def __init__(self, tagId, hid, tagType, uid):
        self.tagId = tagId
        self.hid = hid
        self.uid = uid
        self.tagType = tagType

@app.route('/bird')
def bird():
    return render_template('bird.html',  tags = getTagList())

@app.route('/setTag')
def setTag():
    # @TODO SCORE ADJUSTMENT
    tagType = int(request.args.get('tagType'))
    bid = int(request.args.get('bid'))
    d = request.args.get('d') == "true"
    db = get_db()
    c = db.cursor()

    if d:
        c.execute('insert into tags \
        (tagType, uid, bid) values (?,?,?);',
        (tagType, currentUser, bid))

        c.execute('UPDATE blurbs SET score = score+1 WHERE bid=?', (bid,))
    else:
        c.execute('delete from tags \
        where tagType = ? AND bid = ?;',
        (tagType,bid))

        c.execute('UPDATE blurbs SET score = score-1 WHERE bid=?', (bid,))

    db.commit()

    return str(Tag(
        c.lastrowid,
        bid,
        tagType,
        currentUser
    ))

@app.route('/postHighlight')
def postHighlight():
    return "lskjdflkj"

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, threaded=True)
