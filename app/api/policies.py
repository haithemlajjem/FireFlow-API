"""
Blueprint for Filtering Policy API endpoints.
"""

from flask import Blueprint, jsonify, request

from app.db import get_db
from app.services import policy as policy_service

bp = Blueprint("policies", __name__, url_prefix="/api/policies")


@bp.route("/firewall/<int:fw_id>", methods=["POST"])
def add_policy(fw_id: int):
    """
    Add a new policy to a firewall
    ---
    tags:
      - Policies
    parameters:
      - name: fw_id
        in: path
        required: true
        type: integer
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/definitions/PolicyIn'
    responses:
      201:
        description: Policy created
        schema:
          $ref: '#/definitions/PolicyOut'
      404:
        description: Firewall not found
    """
    db = get_db()
    body = request.get_json()
    try:
        policy = policy_service.add_policy(
            db,
            fw_id=fw_id,
            name=body["name"],
            rules=body.get("rules", []),
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    return jsonify(policy.dict()), 201


@bp.route("/firewall/<int:fw_id>", methods=["GET"])
def list_policies(fw_id: int):
    """
    List all policies for a firewall
    ---
    tags:
      - Policies
    parameters:
      - name: fw_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: List of policies
        schema:
          type: array
          items:
            $ref: '#/definitions/PolicyOut'
      404:
        description: Firewall not found
    """
    db = get_db()
    try:
        policies = policy_service.list_policies(db, fw_id)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    return jsonify([p.dict() for p in policies]), 200


@bp.route("/<int:policy_id>", methods=["DELETE"])
def delete_policy(policy_id: int):
    """
    Delete a policy
    ---
    tags:
      - Policies
    parameters:
      - name: policy_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Policy deleted
      404:
        description: Policy not found
    """
    db = get_db()
    deleted = policy_service.delete_policy(db, policy_id)
    if not deleted:
        return jsonify({"error": "not found"}), 404
    return jsonify({"deleted": policy_id}), 200
