#!/usr/bin/python3
"""
Module - index
Index for API
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def api_status():
    """
    returns JSON of status
    """
    return jsonify({"status": "OK"})
