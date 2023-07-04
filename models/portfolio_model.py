class PortfolioItem(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    title = db.Column(db.String, nullable = False, unique = True)
    category = db.Column(db.String, nullable = False)
    projectURL = db.Column(db.String)
    repoURL = db.Column(db.String)
    imgURL = db.Column(db.String)
    description = db.Column(db.String)
    date = db.Column(db.String)

    def __init__(self, title, category, projectURL, repoURL, imgURL, description, date):
        self.title = title
        self.category = category
        self.projectURL = projectURL
        self.repoURL = repoURL
        self.imgURL = imgURL
        self.description = description
        self.date = date


class PortfolioSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'category', 'projectURL', 'repoURL', 'imgURL', 'description', 'date', 'perPage')

portfolio_schema = PortfolioSchema()
all_portfolio_schema = PortfolioSchema(many=True)