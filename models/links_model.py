class LinkItem(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    title = db.Column(db.String, nullable = False, unique = True)
    url = db.Column(db.String)
    logo_url = db.Column(db.String)
    details = db.Column(db.String)

    def __init__(self, title, url, logo_url, details):
        self.title=title
        self.url=url
        self.logo_url=logo_url
        self.details=details

class LinkSchema(ma.Schema):
    class Meta:
        fields = ("id", "email", "password")

link_schema = LinkSchema
all_link_schema = LinkSchema(many=True)
