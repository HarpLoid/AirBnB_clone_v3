#!/usr/bin/python3
"""
Module - index
Index for API
"""
from api.v1.views import app_views


@app_views.route("/status", strict_slashes=False)
def api_status():
    return {"status": "OK"}
