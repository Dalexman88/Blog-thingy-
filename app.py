from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class blogpost(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False)
  content= db.Column(db.Text, nullable= False)
  author=db.Column(db.String, nullable=False, default='N/A')
  date_posted=db.Column(db.DATETIME, nullable=False, default=datetime.utcnow)

  def __repr__(self):
    return 'blog post ' + str(self.id)





@app.route('/')
def index():
    return render_template('index.html')


@app.route('/post', methods=['GET','POST'])
def posts():

    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_Author = request.form['Author']
        new_post = blogpost(title=post_title, content=post_content, author=post_Author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/post')
    else:
        all_posts = blogpost.query.order_by(blogpost.date_posted).all()
        return render_template ('posts.html', posts=all_posts)


@app.route('/post/delete/<int:id>')
def delete(id):
    post =blogpost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/post')

@app.route('/post/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    post =blogpost.query.get_or_404(id)
    if request.method == "POST":
       
       post.title = request.form['title']
       post.Author = request.form['Author']
       post.content = request.form['content']
       db.session.commit()
       return redirect('/post')
    else:
       return render_template('edit.html', post=post)


if __name__ == "__main__":
    app.run(debug=True)
