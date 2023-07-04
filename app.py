from flask import Flask, request, jsonify
from flask_cors import CORS
from imports import db, ma, bcrypt
import os

app = Flask(__name__)
init_Posted = False
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, 'app.sqlite')
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://wwiwrddrdlsunr:ba77b924a207da45ea99849dd3096ffbe4805dfd8c1f5fa41993d933fec780ae@ec2-54-234-13-16.compute-1.amazonaws.com:5432/d83nvvhb3an956"

db.init_app(app)
ma.init_app(app)
bcrypt.init_app(app)
CORS(app)



@app.route('/portfolio', methods=["GET"])
def get_portfolio_items():
    portfolioItems = db.session.query(PortfolioItem).all()
    return jsonify(all_portfolio_schema.dump(portfolioItems))

@app.route("/portfolio", methods=["POST"])
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
  
    new_portfolio_item = PortfolioItem(title, category, projectURL, repoURL, imgURL, description, date)
    db.session.add(new_portfolio_item)
    db.session.commit()

    return jsonify(portfolio_schema.dump(new_portfolio_item))
    
@app.route('/portfolio/batch', methods=["POST"])

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

        existing_portfolioItem_check = db.session.query(PortfolioItem).filter(PortfolioItem.title == title).first()
        if existing_portfolioItem_check is None:
            new_record = PortfolioItem(title, category, projectURL, repoURL, imgURL, description, date)
            db.session.add(new_record)
            db.session.commit()
            new_portfolioItems.append(portfolio_schema.dump(new_record))

    return jsonify(all_portfolio_schema.dump(new_portfolioItems))

@app.route('/portfolio/<id>', methods=["GET"])
def get_portfolio_item(id):
    portfolioItem = db.session.query(PortfolioItem).filter_by(id=id).first()
    return jsonify(portfolio_schema.dump(portfolioItem))

@app.route('/portfolio/<id>', methods=["PUT"])
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

    db.session.commit()

    return jsonify(portfolio_schema.dump(portfolio_item_to_update))

@app.route('/portfolio/<id>', methods=["DELETE"])
def delete_portfolio_item(id):
    delete_portfolio_item = db.session.query(PortfolioItem).filter(PortfolioItem.id == id).first()
    db.session.delete(delete_portfolio_item)

    db.session.commit()

    return jsonify(f"{delete_portfolio_item.title} has been deleted!")

@app.route('/blog', methods = ["GET"])
def get_all_blog_items():
    blogItems = db.session.query(BlogItem).all()
    return jsonify(all_blog_schema.dump(blogItems))

@app.route('/blog', methods = ["POST"])
def add_blog_item():
    if not request.is_json:
        return jsonify("Request body is not JSON")
    
    data = request.get_json()
    title = data.get('title')
    date = data.get('date')
    content = data.get('content')
    flavorImgURL = data.get('flavorImgURL')
    refURL = data.get('refURL')

    new_blog_item = BlogItem(title, date, content, flavorImgURL, refURL)
    db.session.add(new_blog_item)
    db.session.commit()

    return jsonify(blog_schema.dump(new_blog_item))

@app.route('/blog/batch', methods=["POST"])
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
        flavorImgURL = blogItem.get('flavorImgURL')
        refURL = blogItem.get('refURL')

        existing_blogItem_check = db.session.query(PortfolioItem).filter(PortfolioItem.title == title).first()
        if existing_blogItem_check is None:
            new_record = BlogItem(title, date, content, flavorImgURL, refURL)
            db.session.add(new_record)
            db.session.commit()
            new_blogItems.append(all_blog_schema.dump(new_record))

    return jsonify(all_portfolio_schema.dump(new_blogItems))

@app.route('/blog/<id>', methods = ["GET"])
def get_blog_item(id):
    blogItem = db.session.query(BlogItem).filter(BlogItem.id == id).first()
    return jsonify(blog_schema.dump(blogItem))




@app.route('/blog/<id>', methods = ["PUT"])
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

@app.route('/blog/<id>', methods=["DELETE"])
def delete_blog_item(id):
    delete_blog_item = db.session.query(BlogItem).filter(BlogItem.id == id).first()
    db.session.delete(delete_blog_item) 
    db.session.commit()
    return jsonify(f"{delete_blog_item} has been deleted")

@app.route('/ed', methods = ["GET"])
def get_ed_items():
    edItems = db.session.query().all()
    return jsonify(all_education_schema.dump(edItems))

@app.route('/ed', methods = ["POST"])
def add_ed_item():
    if not request.is_json:
        return jsonify("Request body is not JSON")
    
    data = request.get_json()
    title = data.get('title')
    merit = data.get('merit')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    details = data.get('details')

    new_ed_item = EducationItem(title, merit, start_date, end_date, details)
    db.session.add(new_ed_item)
    db.session.commit()

@app.route('/ed/batch', methods=["POST"])
def add_many_edItems():
    if request.content_type != "application/json":
        return jsonify("Error: Your data must be sent as JSON")
    
    data = request.get_json()
    edItems = data.get('edItems')

    new_edItems = []

    for edItem in edItems:
        title = edItem.get('title')
        merit = edItem.get('merit')
        start_date = edItem.get('start_date')
        end_date = edItem.get('end_date')
        details = edItem.get('details')
        new_record = edItem(title, merit, start_date, end_date, details)
        db.session.add(new_record)
        db.session.commit()
        new_edItems.append(all_education_schema.dump(new_record))

    return jsonify(all_education_schema.dump(new_edItems))

@app.route('/ed/<id>', methods=["GET"])
def get_ed_item(id):
    edItem = db.session.query(EducationItem).filter(EducationItem.id == id).first()
    return jsonify(education_schema.dump(edItem))

@app.route('/ed/<id>', methods = ["PUT"])
def update_ed_item(id):
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be sent as JSON')
    
    data = request.get_json()
    title = data.get('title')
    merit = data.get('merit')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    details = data.get('details')

    ed_item_to_update = db.session.query(EducationItem).filter(EducationItem.id == id).first()

    if title != None:
        ed_item_to_update.title = title
    if merit != None:
        ed_item_to_update.merit = merit
    if start_date != None:
        ed_item_to_update.start_date = start_date
    if end_date != None:
        ed_item_to_update.end_date = end_date
    if details != None:
        ed_item_to_update.details = details

    db.session.commit()

    return jsonify(education_schema.dump(ed_item_to_update))

@app.route('/ed/<id>', methods = ["DELETE"])
def delete_ed_item(id):
    delete_ed_item = db.session.query(EducationItem).filter(EducationItem.id == id).first()
    db.session.delete(delete_ed_item) 
    db.session.commit()
    return jsonify(f"{delete_ed_item} has been deleted")

@app.route('/career', methods = ['GET'])
def get_all_career_items():
    careerItems = db.session.query(CareerItem).all()
    return jsonify(all_career_schema.dump(careerItems))  

@app.route('/career', methods = ["POST"])
def add_career_item():
    if not request.is_json:
        return jsonify("Request body is not JSON")
    
    data = request.get_json()
    employer = data.get('employer')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    start_job_title = data.get('start_job_title')
    end_job_title = data.get('end_job_title')
    details = data.get('details')

    new_career_item = CareerItem(employer, start_job_title, end_job_title, start_date, end_date, details)
    db.session.add(new_career_item)
    db.session.commit()

@app.route('/career/batch', methods=["POST"])
def add_many_careerItems():
    if request.content_type != "application/json":
        return jsonify("Error: Your data must be sent as JSON")
    
    data = request.get_json()
    careerItems = data.get('careerItems')

    new_careerItems = []

    for careerItem in careerItems:
        employer = careerItem.get('employer')
        start_date = careerItem.get('start_date')
        end_date = careerItem.get('end_date')
        start_job_title = careerItem.get('start_job_title')
        end_job_title = careerItem.get('end_job_title')
        details = careerItem.get('details')
        new_record = careerItem(employer, start_date, end_date, start_job_title, end_job_title, details)
        db.session.add(new_record)
        db.session.commit()
        new_careerItems.append(all_career_schema.dump(new_record))

    return jsonify(all_career_schema.dump(new_careerItems))

@app.route('/career/<id>', methods=["GET"])
def get_career_item(id):
    careerItem = db.session.query(CareerItem).filter(CareerItem.id == id).first()
    return jsonify(career_schema.dump(careerItem))

@app.route('/career/<id>', methods = ["PUT"])
def update_career_item(id):
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be sent as JSON')
    
    data = request.get_json()
    employer = data.get('employer')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    start_job_title = data.get('start_job_title')
    end_job_title = data.get('end_job_title')
    details = data.get('details')

    career_item_to_update = db.session.query(CareerItem).filter(CareerItem.id == id).first()


    if employer != None:
        career_item_to_update.employer = employer
    if start_date != None:
        career_item_to_update.start_date = start_date
    if end_date != None:
        career_item_to_update.end_date = end_date
    if start_job_title != None:
        career_item_to_update.start_job_title = start_job_title
    if end_job_title != None:
        career_item_to_update.end_job_title = end_job_title
    if details != None:
        career_item_to_update.details = details

    db.session.commit()

    return jsonify(education_schema.dump(career_item_to_update))

@app.route('/career/<id>', methods = ["DELETE"])
def delete_career_item(id):
    delete_career_item = db.session.query(CareerItem).filter(CareerItem.id == id).first()
    db.session.delete(delete_career_item) 
    db.session.commit()
    return jsonify(f"{delete_career_item} has been deleted")



@app.route('/updateables', methods = ["GET"])
def get_updateables():
    updateItems = db.session.query(GeneralUpdate).all()
    return jsonify(all_generalupdate_schema.dump(updateItems))

if __name__ == "__main__":
    app.run(debug=True)