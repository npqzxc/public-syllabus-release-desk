from __future__ import annotations

from flask import Blueprint, g, jsonify, request

from ..auth import require_login
from ..services.contract_service import get_contract_detail
from ..services.dashboard_service import build_dashboard
from ..services.vendor_service import get_vendor_detail, list_vendors, owner_options

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.get("/dashboard")
@require_login
def dashboard_api():
    return jsonify(build_dashboard(g.db))


@api_bp.get("/vendors")
@require_login
def vendors_api():
    filters = {key: value for key, value in request.args.items() if value.strip()}
    return jsonify(list_vendors(g.db, filters))


@api_bp.get("/vendors/<code>")
@require_login
def vendor_detail_api(code: str):
    payload = get_vendor_detail(g.db, code)
    if payload is None:
        return jsonify({"error": "not_found"}), 404
    return jsonify(payload)


@api_bp.get("/contracts/<int:contract_id>")
@require_login
def contract_detail_api(contract_id: int):
    payload = get_contract_detail(g.db, contract_id)
    if payload is None:
        return jsonify({"error": "not_found"}), 404
    return jsonify(payload)


@api_bp.get("/owners")
@require_login
def owners_api():
    return jsonify({"items": owner_options(g.db)})
