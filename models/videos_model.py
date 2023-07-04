class VideoItem:
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, nullable = False)
    subtitle = db.Column(db.String, nullable = False)
    url = db.Column(db.String, nullable = False)
    source = db.Column(db.String, nullable = False)
    details = db.Column(db.String, nullable = False)

    def __init__(self, title, subtitle, url, source, details):
        self.title = title
        self.subtitle = subtitle
        self.url = url
        self.source = source
        self.details = details

class VideoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'subtitle', 'url', 'source', 'details')

video_schema = VideoSchema()
all_video_schema = VideoSchema(many=True)