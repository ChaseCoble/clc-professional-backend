from flask import Blueprint
from .routes.links import link_blueprint
from .routes.videos import video_blueprint

master_blueprint = Blueprint('master', __name__)

master_blueprint.register_blueprint(link_blueprint)
master_blueprint.register_blueprint(video_blueprint)
