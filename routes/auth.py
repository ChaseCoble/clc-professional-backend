from ..models.user_model import User, user_schema
from ..models.updateables_model import GeneralUpdate, generalupdate_schema, all_generalupdate_schema

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/init', methods = ["POST"])
def initContent():
    global init_Posted

    if init_Posted:
        return 'Only one POST request is allowed.', 400
    
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be sent as JSON')

    data = request.get_json()
    userAcct = data.get('userAcct')
    updateables = data.get('updateables')
    
    def init_user(user):
        email = user['email']
        password = user['password']
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        new_admin = User(email, pw_hash)
        db.session.add(new_admin)
        response = jsonify(user_schema.dump(new_admin))
        return response

    def init_updateables(content):
        contact_email = content['contact_email']
        phone = content['phone']
        bioBlurb = content['bioBlurb']
        biography = content['biography']
        logo = content['logo']
        homeImg = content['homeImg']
        aboutImg = content['aboutImg']
        new_updateables = GeneralUpdate(contact_email, phone, bioBlurb, biography, logo, homeImg, aboutImg)
        db.session.add(new_updateables)
        response_2= jsonify(generalupdate_schema.dump(new_updateables))
        return response_2

    response = init_user(userAcct)
    response_2 = init_updateables(updateables)
    db.session.commit()

    init_Posted = True

    return jsonify(response, response_2)

@auth_blueprint.route('/auth', methods=["POST"])
def verification():
    if request.content_type != "application/json":
        return jsonify("Error improper validation content type")
    
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = db.session.query(User).filter(User.email == email).first()

    if user is None:
        return jsonify("User could not be Verified")
    
    if user.email != "coblexdevelopment@gmail.com":
        return jsonify("User not authorized")
    
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify("User could not be Verified")
    
    return jsonify("Authenticated")