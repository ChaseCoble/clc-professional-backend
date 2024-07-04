from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_bcrypt import Bcrypt



app = Flask(__name__)
#basedir = os.path.abspath(os.path.dirname(__file__))
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, 'app.sqlite')
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://ufn5c1gf0v1ltq:p71e8ce7d3088ba3fb2739237e4ff7d0fdae3b99f202c415d6f0d2d753bf7ce4a@c5p86clmevrg5s.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/dalbsh3n64d8jb"

db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
CORS(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String, nullable = False, unique = True)
    password = db.Column(db.String, nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "email", "password")

user_schema = UserSchema()

class PortfolioItem(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, nullable = False, unique = True)
    category = db.Column(db.String, nullable = False)
    projectURL = db.Column(db.String)
    repoURL = db.Column(db.String)
    imgURL = db.Column(db.String)
    description = db.Column(db.String)
    date = db.Column(db.String)
    language = db.Column(db.String)
    languagedetail = db.Column(db.String)

    def __init__(self, title, category, projectURL, repoURL, imgURL, description, date, language, languagedetail):
        self.title = title
        self.category = category
        self.projectURL = projectURL
        self.repoURL = repoURL
        self.imgURL = imgURL
        self.description = description
        self.date = date
        self.language = language
        self.languagedetail = languagedetail


class PortfolioSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'category', 'projectURL', 'repoURL', 'imgURL', 'description', 'date', 'perPage', 'language', 'languagedetail')

portfolio_schema = PortfolioSchema()
all_portfolio_schema = PortfolioSchema(many=True)

class BlogItem(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, nullable = False, unique = True)
    date = db.Column(db.String)
    content = db.Column(db.String)
    flavorImgURL = db.Column(db.String)
    refURL = db.Column(db.String)

    def __init__(self, title, date, content, flavorImgURL, refURL):
        self.title = title
        self.date = date
        self.content = content
        self.flavorImgURL = flavorImgURL
        self.refURL = refURL

class BlogSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'date', 'content', 'flavorImgURL', 'refURL')

blog_schema = BlogSchema()
all_blog_schema = BlogSchema(many=True)



@app.route('/sZLdScPBTu', methods = ["POST"])
def initAdmin():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be sent as JSON')

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    new_admin = User(email, pw_hash)
    db.session.add(new_admin)
    db.session.commit()

    return jsonify(user_schema.dump(new_admin))
    
@app.route('/auth', methods=["POST"])
def verification():
    if request.content_type != "application/json":
        return jsonify("Error improper validation content type")
    
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = db.session.query(User).filter(User.email == email).first()

    if user is None:
        return jsonify("User could not be Verified")
    
    if user.email != "coblexdevelopment@gmail.com":
        return jsonify("User not authorized")
    
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify("User could not be Verified")
    
    return jsonify("Authenticated")

@app.route('/portfolio/get', methods=["GET"])
def get_portfolio_items():
    portfolioItems = db.session.query(PortfolioItem).all()
    return jsonify(all_portfolio_schema.dump(portfolioItems))
    
@app.route('/portfolio/get/<id>', methods=["GET"])
def get_portfolio_item(id):
    portfolioItem = db.session.query(PortfolioItem).filter_by(id=id).first()
    return jsonify(portfolio_schema.dump(portfolioItem))

@app.route("/portfolio/add", methods=["POST"])
def add_portfolio_item():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be sent as JSON')

    data = request.get_json()
    title = data.get('title')
    category = data.get('category')
    projectURL = data.get('projectURL')
    repoURL = data.get('repoURL')
    imgURL = data.get('imgURL')
    description = data.get('description')
    date = data.get('date')
    language = data.get('language')
    languagedetail = data.get('languagedetail')

    new_portfolio_item = PortfolioItem(title, category, projectURL, repoURL, imgURL, description, date, language, languagedetail)
    db.session.add(new_portfolio_item)
    db.session.commit()

    return jsonify(portfolio_schema.dump(new_portfolio_item))

@app.route('/portfolio/add/many', methods=["POST"])

def add_many_portfolioItems():
    if request.content_type != "application/json":
        return jsonify("Error: Your data must be sent as JSON")
    
    data = request.get_json()
    portfolioItems = data.get('portfolioItems')

    new_portfolioItems = []

    for portfolioItem in portfolioItems:
        title = portfolioItem.get('title')
        category = portfolioItem.get('category')
        projectURL = portfolioItem.get('projectURL')
        repoURL = portfolioItem.get('repoURL')
        imgURL = portfolioItem.get('imgURL')
        description = portfolioItem.get('description')
        date = portfolioItem.get('date')
        language = portfolioItem.get('language')
        languagedetail = portfolioItem.get('languagedetail')

        existing_portfolioItem_check = db.session.query(PortfolioItem).filter(PortfolioItem.title == title).first()
        if existing_portfolioItem_check is None:
            new_record = PortfolioItem(title, category, projectURL, repoURL, imgURL, description, date, language, languagedetail)
            db.session.add(new_record)
            db.session.commit()
            new_portfolioItems.append(portfolio_schema.dump(new_record))

    return jsonify(all_portfolio_schema.dump(new_portfolioItems))

@app.route('/portfolio/update/<id>', methods=["PUT"])
def update_portfolio_item(id):
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be sent as JSON')
    
    data = request.get_json()
    title = data.get('title')
    projectURL = data.get('projectURL')
    repoURL = data.get('repoURL')
    imgURL = data.get('imgURL')
    description = data.get('description')
    date = data.get('date')
    language = data.get('language')
    languagedetail = data.get('languagedetail')

    portfolio_item_to_update = db.session.query(PortfolioItem).filter(PortfolioItem.id == id).first()

    if title != None:
        portfolio_item_to_update.title = title
    if projectURL != None:
        portfolio_item_to_update.projectURL = projectURL
    if repoURL != None:
        portfolio_item_to_update.repoURL = repoURL
    if imgURL != None:
        portfolio_item_to_update.imgURL = imgURL
    if description != None:
        portfolio_item_to_update.description = description
    if date != None:
        portfolio_item_to_update.date = date
    if language != None:
        portfolio_item_to_update.language = language
    if languagedetail != None:
        portfolio_item_to_update.languagedetail = languagedetail    

    db.session.commit()

    return jsonify(portfolio_schema.dump(portfolio_item_to_update))

@app.route('/portfolio/delete/<id>', methods=["DELETE"])
def delete_portfolio_item(id):
    delete_portfolio_item = db.session.query(PortfolioItem).filter(PortfolioItem.id == id).first()
    db.session.delete(delete_portfolio_item)

    db.session.commit()

    return jsonify(f"{delete_portfolio_item.title} has been deleted!")

@app.route('/blog/get', methods = ["GET"])
def get_all_blog_items():
    blogItems = db.session.query(BlogItem).all()
    return jsonify(all_blog_schema.dump(blogItems))

@app.route('/blog/get/<id>', methods = ["GET"])
def get_blog_item(id):
    blogItem = db.session.query(BlogItem).filter(BlogItem.id == id).first()
    return jsonify(blog_schema.dump(blogItem))
@app.route('/blog/add', methods = ["POST"])
def add_blog_item():
    if not request.is_json:
        return jsonify("Request body is not JSON")
    
    data = request.get_json()
    title = data.get('title')
    date = data.get('date')
    content = data.get('content')
    flavorImgURL = data.get('flavorImg')
    refURL = data.get('refURL')

    new_blog_item = BlogItem(title, date, content, flavorImgURL, refURL)
    db.session.add(new_blog_item)
    db.session.commit()

    return jsonify(blog_schema.dump(new_blog_item))

@app.route('/blog/add/many', methods=["POST"])
def add_many_blogItems():
    if request.content_type != "application/json":
        return jsonify("Error: Your data must be sent as JSON")
    
    data = request.get_json()
    blogItems = data.get('blogItems')

    new_blogItems = []

    for blogItem in blogItems:
        title = blogItem.get('title')
        date = blogItem.get('date')
        content = blogItem.get('content')
        flavorImgURL = blogItem.get('flavorImg')
        refURL = blogItem.get('refURL')

        existing_blogItem_check = db.session.query(PortfolioItem).filter(PortfolioItem.title == title).first()
        if existing_blogItem_check is None:
            new_record = BlogItem(title, date, content, flavorImgURL, refURL)
            db.session.add(new_record)
            db.session.commit()
            new_blogItems.append(all_blog_schema.dump(new_record))

    return jsonify(all_portfolio_schema.dump(new_blogItems))

@app.route('/blog/update/<id>', methods = ["PUT"])
def update_blog_item(id):
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be sent as JSON')
    
    data = request.get_json()
    title = data.get('title')
    refURL = data.get('refURL')
    flavorImgURL = data.get('flavorImgURL')
    content = data.get('content')
    date = data.get('date')

    blog_item_to_update = db.session.query(BlogItem).filter(BlogItem.id == id).first()

    if title != None:
        blog_item_to_update.title = title
    if refURL != None:
        blog_item_to_update.refURL = refURL
    if flavorImgURL != None:
        blog_item_to_update.flavorImgURL = flavorImgURL
    if content != None:
        blog_item_to_update.content = content
    if date != None:
        blog_item_to_update.date = date

    db.session.commit()

    return jsonify(blog_schema.dump(blog_item_to_update))

@app.route('/blog/delete/<id>', methods=["DELETE"])
def delete_blog_item(id):
    delete_blog_item = db.session.query(BlogItem).filter(BlogItem.id == id).first()
    db.session.delete(delete_blog_item) 
    db.session.commit()
    return jsonify(f"{delete_blog_item} has been deleted")


if __name__ == "__main__":
    app.run(debug=True)