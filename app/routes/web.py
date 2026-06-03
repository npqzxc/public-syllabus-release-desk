from __future__ import annotations

from flask import Blueprint, g, redirect, render_template, request, session, url_for

from ..auth import authenticate_user, login_user, logout_user, require_login
from ..services.contract_service import add_note, contract_form_options, create_contract, get_contract_detail, update_status
from ..services.dashboard_service import build_dashboard
from ..services.vendor_service import get_vendor_detail, list_vendors, owner_options

web_bp = Blueprint("web", __name__)


@web_bp.get("/login")
def login_view():
    return render_template("login.html", page_id="login", page_payload={}, error=None)


@web_bp.post("/login")
def login_submit():
    user = authenticate_user(g.db, request.form.get("username", "").strip(), request.form.get("password", ""))
    if user is None:
        return render_template("login.html", page_id="login", page_payload={}, error="用户名或密码错误。"), 401
    login_user(user)
    destination = session.pop("after_login", url_for("web.dashboard"))
    return redirect(destination)


@web_bp.post("/logout")
@require_login
def logout_submit():
    logout_user()
    return redirect(url_for("web.login_view"))


@web_bp.get("/")
@require_login
def dashboard():
    payload = build_dashboard(g.db)
    return render_template("dashboard.html", page_id="dashboard", page_payload=payload, dashboard=payload)


@web_bp.get("/vendors")
@require_login
def vendors():
    filters = {key: value for key, value in request.args.items() if value.strip()}
    payload = list_vendors(g.db, filters)
    return render_template(
        "vendors.html",
        page_id="vendors",
        page_payload=payload,
        filters=filters,
        vendors=payload["items"],
        owners=owner_options(g.db),
    )


@web_bp.get("/vendors/<code>")
@require_login
def vendor_detail(code: str):
    vendor = get_vendor_detail(g.db, code)
    if vendor is None:
        return render_template("vendor_detail.html", page_id="vendor-detail", page_payload={}, vendor=None), 404
    return render_template("vendor_detail.html", page_id="vendor-detail", page_payload=vendor, vendor=vendor)


@web_bp.get("/contracts/new")
@require_login
def contract_new():
    options = contract_form_options(g.db)
    return render_template("new_contract.html", page_id="new-contract", page_payload=options, options=options, error=None)


@web_bp.post("/contracts")
@require_login
def contract_create():
    options = contract_form_options(g.db)
    try:
        contract_id = create_contract(g.db, request.form)
    except ValueError as exc:
        return render_template(
            "new_contract.html",
            page_id="new-contract",
            page_payload=options,
            options=options,
            error=str(exc),
            form=request.form,
        ), 400
    return redirect(url_for("web.contract_detail", contract_id=contract_id))


@web_bp.get("/contracts/<int:contract_id>")
@require_login
def contract_detail(contract_id: int):
    contract = get_contract_detail(g.db, contract_id)
    if contract is None:
        return render_template("contract_detail.html", page_id="contract-detail", page_payload={}, contract=None), 404
    return render_template("contract_detail.html", page_id="contract-detail", page_payload=contract, contract=contract, error=None)


@web_bp.post("/contracts/<int:contract_id>/notes")
@require_login
def contract_add_note(contract_id: int):
    try:
        add_note(g.db, contract_id, g.current_user.id, request.form.get("note_type", "general"), request.form.get("body", ""))
    except ValueError as exc:
        contract = get_contract_detail(g.db, contract_id)
        return render_template("contract_detail.html", page_id="contract-detail", page_payload=contract, contract=contract, error=str(exc)), 400
    return redirect(url_for("web.contract_detail", contract_id=contract_id))


@web_bp.post("/contracts/<int:contract_id>/status")
@require_login
def contract_update_status(contract_id: int):
    try:
        update_status(g.db, contract_id, request.form.get("status", ""))
    except ValueError as exc:
        contract = get_contract_detail(g.db, contract_id)
        return render_template("contract_detail.html", page_id="contract-detail", page_payload=contract, contract=contract, error=str(exc)), 400
    return redirect(url_for("web.contract_detail", contract_id=contract_id))
