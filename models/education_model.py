class EducationItem(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, nullable = False)
    merit = db.Column(db.String, nullable = False)
    start_date = db.Column(db.String, nullable = False)
    end_date = db.Column(db.String)
    details = db.Column(db.String, nullable = False)

    def __init__(self, title, merit, start_date, end_date, details):
        self.title = title
        self.merit = merit
        self.start_date = start_date
        self.end_date = end_date
        self.details = details

class EducationSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'merit', 'start_date', 'end_date', 'details')

education_schema = EducationSchema()
all_education_schema = EducationSchema(many=True)