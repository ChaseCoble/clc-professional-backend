from ..models.videos_model import VideoItem, video_schema, all_video_schema


video_blueprint = Blueprint('video', __name__)

@video_blueprint.route('/video', methods = ["GET"])
def get_video_item():
    videoItems = db.session.query(VideoItem).all
    return jsonify(all_video_schema.dump(videoItems))

@video_blueprint.route('/video', methods=["POST"])
def add_video_item():
    if not request.is_json:
        return jsonify("Request body is not JSON")

    data = request.get_json()
    title = data.get("title")
    subtitle = data.get("subtitle")
    source = data.get("source")
    url = data.get("url")
    details = data.get("details")

    new_video_item = VideoItem(title, subtitle, source, url, details)
    db.session.add(new_video_item)
    db.session.commit()

    return jsonify(video_schema.dump(new_video_item))

@video_blueprint.route('/video/batch', methods = ["POST"])
def add_many_video_items():
    if request.content_type != "application/json":
        return jsonify("Error: Your data must be sent as JSON")
    
    data = request.get_json()
    videoItems = data.get('videoItems')

    new_videoItems = []

    for videoItem in videoItems:
        title = videoItem.get('title')
        subtitle = videoItem.get('subtitle')
        url = videoItem.get('url')
        source = videoItem.get('source')
        details = videoItem.get('details')
        new_record = VideoItem(title, subtitle, url, source, details)
        db.session.add(new_record)
        db.session.commit()
        new_videoItems.append(video_schema.dump(new_record))

    return jsonify(all_video_schema.dump(new_videoItems))

@video_blueprint.route('/video/<id>', methods = ["GET"])
def get_video_item(id):
    videoItem = db.session.query(VideoItem).filter_by(id=id).first()
    return jsonify(video_schema.dump(videoItem))

@video_blueprint.route('/video/<id>', methods = ["PUT"])
def update_video_item(id):
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be sent as JSON')
    
    data = request.get_json()
    title = data.get('title')
    subtitle = data.get('subtitle')
    url = data.get('url')
    source = data.get('source')
    details = data.get('details')

    video_item_to_update = db.session.query(VideoItem).filter(VideoItem.id == id).first()

    if title != None:
        video_item_to_update.title = title
    if subtitle != None:
        video_item_to_update.subtitle = subtitle
    if url != None:
        video_item_to_update.url = url
    if source != None:
        video_item_to_update.source = source
    if details != None:
        video_item_to_update.details = details

    db.session.commit()

    return jsonify(video_schema.dump(video_item_to_update))

@video_blueprint.route('/video/<id>', methods = ["DELETE"])
def delete_video_item(id):
    delete_portfolio_item = db.session.query(VideoItem).filter(VideoItem.id == id).first()
    db.session.delete(delete_portfolio_item)

    db.session.commit()

    return jsonify(f"{delete_portfolio_item.title} has been deleted")

