"""
Blueprint for Firewall Rule API endpoints.
"""

from flask import Blueprint, jsonify, request

from app.db import get_db
from app.services import rule as rule_service

bp = Blueprint("rules", __name__, url_prefix="/api/rules")


@bp.route("/policy/<int:policy_id>", methods=["POST"])
def add_rule(policy_id: int):
    """
    Add a new rule to a policy
    ---
    tags:
      - Rules
    parameters:
      - name: policy_id
        in: path
        required: true
        type: integer
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/definitions/RuleIn'
    responses:
      201:
        description: Rule created
        schema:
          $ref: '#/definitions/RuleOut'
      404:
        description: Policy not found
    """
    db = get_db()
    body = request.get_json()
    try:
        rule = rule_service.add_rule(
            db,
            policy_id=policy_id,
            action=body["action"],
            src=body.get("src"),
            dst=body.get("dst"),
            protocol=body.get("protocol"),
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    return jsonify(rule.dict()), 201


@bp.route("/policy/<int:policy_id>", methods=["GET"])
def list_rules(policy_id: int):
    """
    List all rules for a policy
    ---
    tags:
      - Rules
    parameters:
      - name: policy_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: List of rules
        schema:
          type: array
          items:
            $ref: '#/definitions/RuleOut'
      404:
        description: Policy not found
    """
    db = get_db()
    try:
        rules = rule_service.list_rules(db, policy_id)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    return jsonify([r.dict() for r in rules]), 200


@bp.route("/<int:rule_id>", methods=["DELETE"])
def delete_rule(rule_id: int):
    """
    Delete a rule
    ---
    tags:
      - Rules
    parameters:
      - name: rule_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Rule deleted
      404:
        description: Rule not found
    """
    db = get_db()
    deleted = rule_service.delete_rule(db, rule_id)
    if not deleted:
        return jsonify({"error": "not found"}), 404
    return jsonify({"deleted": rule_id}), 200
