from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import joinedload

from ..models import Contract, ReviewNote, RiskFlag, Vendor

CONTRACT_STATUSES = ("draft", "review", "active", "risk", "closed")
SLA_LEVELS = ("bronze", "silver", "gold")
PROCUREMENT_STAGES = ("owner_review", "legal_review", "security_review", "risk_assessment", "approved")


def contract_form_options(db_session) -> dict:
    vendors = db_session.query(Vendor).order_by(Vendor.name.asc()).all()
    return {
        "vendors": [{"id": vendor.id, "code": vendor.code, "name": vendor.name} for vendor in vendors],
        "statuses": CONTRACT_STATUSES,
        "sla_levels": SLA_LEVELS,
        "procurement_stages": PROCUREMENT_STAGES,
    }


def get_contract_detail(db_session, contract_id: int):
    contract = (
        db_session.query(Contract)
        .options(
            joinedload(Contract.vendor).joinedload(Vendor.owner),
            joinedload(Contract.review_notes).joinedload(ReviewNote.author),
            joinedload(Contract.risk_flags),
        )
        .filter(Contract.id == contract_id)
        .one_or_none()
    )
    if contract is None:
        return None
    return {
        "id": contract.id,
        "title": contract.title,
        "status": contract.status,
        "annual_spend": float(contract.annual_spend),
        "renewal_date": contract.renewal_date.isoformat(),
        "auto_renew": contract.auto_renew,
        "sla_level": contract.sla_level,
        "procurement_stage": contract.procurement_stage,
        "vendor": {
            "code": contract.vendor.code,
            "name": contract.vendor.name,
            "owner_name": contract.vendor.owner.display_name,
        },
        "notes": [
            {
                "id": note.id,
                "note_type": note.note_type,
                "body": note.body,
                "author_name": note.author.display_name,
                "created_at": note.created_at.isoformat(timespec="minutes"),
            }
            for note in sorted(contract.review_notes, key=lambda item: item.created_at, reverse=True)
        ],
        "risks": [
            {
                "id": risk.id,
                "severity": risk.severity,
                "title": risk.title,
                "description": risk.description,
                "is_resolved": risk.is_resolved,
                "created_at": risk.created_at.isoformat(timespec="minutes"),
            }
            for risk in sorted(contract.risk_flags, key=lambda item: item.created_at, reverse=True)
        ],
    }


def create_contract(db_session, form: dict[str, str]) -> int:
    required = ["vendor_id", "title", "status", "annual_spend", "renewal_date", "sla_level", "procurement_stage"]
    if any(not form.get(field, "").strip() for field in required):
        raise ValueError("请填写完整的内容流程信息。")
    if form["status"] not in CONTRACT_STATUSES:
        raise ValueError("内容流程状态不合法。")
    contract = Contract(
        vendor_id=int(form["vendor_id"]),
        title=form["title"].strip(),
        status=form["status"],
        annual_spend=Decimal(form["annual_spend"]),
        renewal_date=datetime.strptime(form["renewal_date"], "%Y-%m-%d").date(),
        auto_renew=form.get("auto_renew") == "on",
        sla_level=form["sla_level"],
        procurement_stage=form["procurement_stage"],
    )
    db_session.add(contract)
    db_session.commit()
    return contract.id


def add_note(db_session, contract_id: int, author_id: int, note_type: str, body: str) -> None:
    if not body.strip():
        raise ValueError("评审记录内容不能为空。")
    note = ReviewNote(contract_id=contract_id, author_id=author_id, note_type=note_type or "general", body=body.strip())
    db_session.add(note)
    db_session.commit()


def update_status(db_session, contract_id: int, new_status: str) -> None:
    if new_status not in CONTRACT_STATUSES:
        raise ValueError("目标状态不合法。")
    contract = db_session.get(Contract, contract_id)
    if contract is None:
        raise ValueError("内容流程不存在。")
    contract.status = new_status
    db_session.commit()


def owner_snapshot(db_session) -> dict:
    return {
        "items": [
            {
                "username": vendor["owner_username"],
                "display_name": vendor["owner_name"],
            }
            for vendor in list_vendors_simple(db_session)
        ]
    }


def list_vendors_simple(db_session) -> list[dict]:
    vendors = db_session.query(Vendor).options(joinedload(Vendor.owner)).all()
    return [
        {
            "owner_username": vendor.owner.username,
            "owner_name": vendor.owner.display_name,
        }
        for vendor in vendors
    ]
