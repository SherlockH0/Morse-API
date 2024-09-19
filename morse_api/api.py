from flask import Blueprint, jsonify, request

blueprint = Blueprint("api", __name__)


@blueprint.route("/", methods=["GET"])
def home():
    return "hi"
