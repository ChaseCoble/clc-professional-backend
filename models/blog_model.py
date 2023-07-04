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