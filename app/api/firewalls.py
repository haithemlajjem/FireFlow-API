"""
Blueprint for Firewall API endpoints.
"""

from flask import Blueprint, jsonify, request

from app.db import get_db
from app.services import firewall as firewall_service

bp = Blueprint("firewalls", __name__, url_prefix="/api/firewalls")


# Routes
@bp.route("/", methods=["POST"])
def create_firewall():
    """
    Create a new firewall
    ---
    tags:
      - Firewalls
    parameters:
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/definitions/FirewallIn'
    responses:
      201:
        description: Firewall created
        schema:
          $ref: '#/definitions/FirewallOut'
    """
    db = get_db()
    body = request.get_json()
    try:
        fw = firewall_service.create_firewall(db, body["name"], body.get("description"))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify(fw.dict()), 201


@bp.route("/", methods=["GET"])
def list_firewalls():
    """
    List all firewalls
    ---
    tags:
      - Firewalls
    responses:
      200:
        description: List of firewalls
        schema:
          type: array
          items:
            $ref: '#/definitions/FirewallOut'
    """
    db = get_db()
    fws = firewall_service.list_firewalls(db)
    return jsonify([fw.dict() for fw in fws]), 200


@bp.route("/<int:fw_id>", methods=["GET"])
def get_firewall(fw_id: int):
    """
    Get a firewall by ID
    ---
    tags:
      - Firewalls
    parameters:
      - name: fw_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Firewall found
        schema:
          $ref: '#/definitions/FirewallOut'
      404:
        description: Firewall not found
    """
    db = get_db()
    fw = firewall_service.get_firewall(db, fw_id)
    if not fw:
        return jsonify({"error": "not found"}), 404
    return jsonify(fw.dict()), 200


@bp.route("/<int:fw_id>", methods=["PUT"])
def update_firewall(fw_id: int):
    """
    Update a firewall
    ---
    tags:
      - Firewalls
    parameters:
      - name: fw_id
        in: path
        required: true
        type: integer
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/definitions/FirewallIn'
    responses:
      200:
        description: Firewall updated
        schema:
          $ref: '#/definitions/FirewallOut'
      404:
        description: Firewall not found
    """
    db = get_db()
    body = request.get_json()
    fw = firewall_service.update_firewall(
        db, fw_id, body["name"], body.get("description")
    )
    if not fw:
        return jsonify({"error": "not found"}), 404
    return jsonify(fw.dict()), 200


@bp.route("/<int:fw_id>", methods=["DELETE"])
def delete_firewall(fw_id: int):
    """
    Delete a firewall
    ---
    tags:
      - Firewalls
    parameters:
      - name: fw_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Firewall deleted
      404:
        description: Firewall not found
    """
    db = get_db()
    deleted = firewall_service.delete_firewall(db, fw_id)
    if not deleted:
        return jsonify({"error": "not found"}), 404
    return jsonify({"deleted": fw_id}), 200
