from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_bcrypt import Bcrypt
#import os



app = Flask(__name__)
#basedir = os.path.abspath(os.path.dirname(__file__))
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, 'app.sqlite')
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://u8s73brhf81to4:p71309ff76c9a144c3320f62dab39f44d9e8fb92d01af2bd92c6b6276cce413f3@ccba8a0vn4fb2p.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d1ujdqnuehl93d"

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
    iframe = db.Column(db.Boolean)
    description = db.Column(db.String)
    date = db.Column(db.String)
    language = db.Column(db.String)
    languagedetail = db.Column(db.String)

    def __init__(self, title, category, projectURL, repoURL, iframe, imgURL, description, date, language, languagedetail):
        self.title = title
        self.category = category
        self.projectURL = projectURL
        self.repoURL = repoURL
        self.imgURL = imgURL
        self.iframe = iframe
        self.description = description
        self.date = date
        self.language = language
        self.languagedetail = languagedetail


class PortfolioSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'category', 'projectURL', 'repoURL', 'imgURL','iframe', 'description', 'date', 'perPage', 'language', 'languagedetail')

portfolio_schema = PortfolioSchema()
all_portfolio_schema = PortfolioSchema(many=True)

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
    print(data)
    title = data.get('title')
    category = data.get('category')
    projectURL = data.get('projectURL')
    repoURL = data.get('repoURL')
    imgURL = data.get('imgURL')
    iframe = data.get('iframe')
    description = data.get('description')
    date = data.get('date')
    language = data.get('language')
    languagedetail = data.get('languagedetail')

    new_portfolio_item = PortfolioItem(title, category, projectURL, repoURL, imgURL, iframe, description, date, language, languagedetail)
    print(new_portfolio_item)
    db.session.add(new_portfolio_item)
    db.session.commit()

    return jsonify(portfolio_schema.dump(new_portfolio_item))

@app.route('/portfolio/add/many', methods=["POST"])
def add_many_portfolioItems():
    if request.content_type != "application/json":
        return jsonify("Error: Your data must be sent as JSON")
    
    data = request.get_json()
    portfolioItems = data.get('portfolioItems')
    print(portfolioItems)
    new_portfolioItems = []

    for portfolioItem in portfolioItems:
        title = portfolioItem.get('title')
        category = portfolioItem.get('category')
        projectURL = portfolioItem.get('projectURL')
        repoURL = portfolioItem.get('repoURL')
        imgURL = portfolioItem.get('imgURL')
        iframe = portfolioItem.get('iframe')
        description = portfolioItem.get('description')
        date = portfolioItem.get('date')
        language = portfolioItem.get('language')
        languagedetail = portfolioItem.get('languagedetail')

        existing_portfolioItem_check = db.session.query(PortfolioItem).filter(PortfolioItem.title == title).first()
        if existing_portfolioItem_check is None:
            new_record = PortfolioItem(title, category, projectURL, repoURL, imgURL, iframe, description, date, language, languagedetail)
            print(new_record)
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
    iframe = data.get('iframe')
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
    if iframe !=None:
        portfolio_item_to_update.iframe = iframe
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

if __name__ == "__main__":
    app.run(debug=True)