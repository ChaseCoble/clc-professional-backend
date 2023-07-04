from ..models.links_model import LinkItem, link_schema, all_link_schema


link_blueprint = Blueprint('link', __name__)

@link_blueprint.route('/link', methods = ["GET"])
def get_link_item():
    linkItems = db.session.query(LinkItem).all()
    return jsonify(all_link_schema.dump(linkItems))

@link_blueprint.route('/link', methods = ["POST"])
def add_link_item():
    if not request.is_json:
        return jsonify("Request body is not JSON")
    
    data = request.get_json()
    title = data.get('title')
    url = data.get('url')
    logo_url = data.get('logo_url')
    details = data.get('details')

    new_link_item = LinkItem(title, url, logo_url, details)
    db.session.add(new_link_item)
    db.session.commit()

@link_blueprint.route('/link/batch', methods=["POST"])
def add_many_linkItems():
    if request.content_type != "application/json":
        return jsonify("Error: Your data must be sent as JSON")
    
    data = request.get_json()
    linkItems = data.get('linkItems')

    new_linkItems = []

    for linkItem in linkItems:
        title = linkItem.get('title')
        url = linkItem.get('url')
        logo_url = linkItem.get('logo_url')
        details = linkItem.get('details')
        new_record = LinkItem(title, url, logo_url, details)
        db.session.add(new_record)
        db.session.commit()
        new_linkItems.append(link_schema.dump(new_record))

    return jsonify(all_link_schema.dump(new_linkItems))

@link_blueprint.route('/link/<id>', methods=["GET"])
def get_link_item(id):
    linkItem = db.session.query(LinkItem).filter(LinkItem.id == id).first()
    return jsonify(link_schema.dump(linkItem))

@link_blueprint.route('/link/<id>', methods = ["PUT"])
def update_link_item(id):
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be sent as JSON')
    
    data = request.get_json()
    title = data.get('title')
    url = data.get('url')
    logo_url = data.get('logo_url')
    details = data.get('details')

    link_item_to_update = db.session.query(LinkItem).filter(LinkItem.id == id).first()

    if title != None:
        link_item_to_update.title = title
    if url != None:
        link_item_to_update.url = url
    if logo_url != None:
        link_item_to_update.logo_url = logo_url
    if details != None:
        link_item_to_update.details = details

    db.session.commit()

    return jsonify(link_schema.dump(link_item_to_update))

@link_blueprint.route('/link/<id>', methods = ["DELETE"])
def delete_link_item(id):
    delete_link_item = db.session.query(LinkItem).filter(LinkItem.id == id).first()
    db.session.delete(delete_link_item) 
    db.session.commit()
    return jsonify(f"{delete_link_item} has been deleted")


