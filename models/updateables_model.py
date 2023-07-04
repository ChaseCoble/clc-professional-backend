class GeneralUpdate(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    contact_email = db.Column(db.String, nullable = False)
    phone = db.Column(db.String, nullable = False)
    bioBlurb = db.Column(db.String, nullable = False)
    biography = db.Column(db.String, nullable = False)
    logo = db.Column(db.String, nullable = False)
    homeImg = db.Column(db.String, nullable = False)
    aboutImg = db.Column(db.String, nullable = False)

    def __init__(self, contact_email, phone, bioBlurb, biography, logo, homeImg, aboutImg):
        self.contact_email = contact_email
        self.phone = phone
        self.bioBlurb = bioBlurb
        self.biography = biography
        self.logo = logo
        self.homeImg = homeImg
        self.aboutImg = aboutImg

class GeneralUpdateSchema(ma.Schema):
    class Meta:
        fields = ('id', 'contact_email', 'phone', 'bioBlurb', 'biography', 'logo', 'homeImg', 'aboutImg')

generalupdate_schema = GeneralUpdateSchema()
all_generalupdate_schema = GeneralUpdateSchema(many=True)