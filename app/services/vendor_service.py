from __future__ import annotations

from sqlalchemy import func, or_
from sqlalchemy.orm import joinedload

from ..models import Contract, User, Vendor


def owner_options(db_session) -> list[dict]:
    owners = db_session.query(User).order_by(User.display_name.asc()).all()
    return [{"id": owner.id, "username": owner.username, "display_name": owner.display_name} for owner in owners]


def list_vendors(db_session, filters: dict[str, str]) -> dict:
    query = db_session.query(Vendor).options(joinedload(Vendor.owner), joinedload(Vendor.contracts))
    if filters.get("status"):
        query = query.filter(Vendor.status == filters["status"])
    if filters.get("category"):
        query = query.filter(Vendor.category == filters["category"])
    if filters.get("owner"):
        query = query.join(Vendor.owner).filter(User.username == filters["owner"])
    if filters.get("query"):
        token = f"%{filters['query'].lower()}%"
        query = query.filter(
            or_(
                func.lower(Vendor.code).like(token),
                func.lower(Vendor.name).like(token),
                func.lower(Vendor.summary).like(token),
            )
        )

    vendors = query.order_by(Vendor.renewal_score.asc(), Vendor.name.asc()).all()
    return {
        "filters": filters,
        "items": [
            {
                "code": vendor.code,
                "name": vendor.name,
                "category": vendor.category,
                "status": vendor.status,
                "owner_name": vendor.owner.display_name,
                "owner_username": vendor.owner.username,
                "renewal_score": vendor.renewal_score,
                "contract_count": len(vendor.contracts),
            }
            for vendor in vendors
        ],
    }


def get_vendor_detail(db_session, code: str):
    vendor = (
        db_session.query(Vendor)
        .options(
            joinedload(Vendor.owner),
            joinedload(Vendor.contracts).joinedload(Contract.review_notes),
            joinedload(Vendor.contracts).joinedload(Contract.risk_flags),
        )
        .filter(Vendor.code == code.upper())
        .one_or_none()
    )
    if vendor is None:
        return None
    return {
        "code": vendor.code,
        "name": vendor.name,
        "category": vendor.category,
        "status": vendor.status,
        "summary": vendor.summary,
        "owner_name": vendor.owner.display_name,
        "renewal_score": vendor.renewal_score,
        "contracts": [
            {
                "id": contract.id,
                "title": contract.title,
                "status": contract.status,
                "renewal_date": contract.renewal_date.isoformat(),
                "annual_spend": float(contract.annual_spend),
                "risk_count": len([risk for risk in contract.risk_flags if not risk.is_resolved]),
                "note_count": len(contract.review_notes),
            }
            for contract in sorted(vendor.contracts, key=lambda item: item.renewal_date)
        ],
    }
