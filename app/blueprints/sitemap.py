
from flask import Blueprint, jsonify, current_app, url_for

blueprint = Blueprint('sitemap', __name__)

def has_no_empty_params(rule):
    "Check that there are no empty parameters for a rule"
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

@blueprint.route("/sitemap")
def site_map():
    "Generate a dynamic site map for the app"
    links = []

    # Filter out rules we can't navigate to in a browser
    # and rules that require parameters
    for rule in current_app.url_map.iter_rules():
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))

    return jsonify(links)

