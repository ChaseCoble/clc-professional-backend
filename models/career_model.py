class CareerItem(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, nullable = False)
    employer = db.Column(db.String, nullable = False)
    start_job_title = db.Column(db.String, nullable = False)
    end_job_title = db.Column(db.String, nullable = False)
    start_date = db.Column(db.String, nullable = False)
    end_date = db.Column(db.String)
    details = db.Column(db.String, nullable = False)

    def __init__(self, employer, start_job_title, end_job_title, start_date, end_date, details):
        self.employer = employer
        self.start_job_title = start_job_title
        self.end_job_title = end_job_title
        self.start_date = start_date
        self.end_date = end_date
        self.details = details

class CareerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'career', 'start_job_title', 'end_job_title', 'start_date', 'end_date', 'details')

career_schema = CareerSchema()
all_career_schema = CareerSchema(many=True)