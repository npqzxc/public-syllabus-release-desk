from __future__ import annotations

from datetime import date

from sqlalchemy import func

from ..models import Contract, RiskFlag, Vendor


def build_dashboard(db_session) -> dict:
    vendor_total = db_session.query(func.count(Vendor.id)).scalar() or 0
    active_contracts = db_session.query(func.count(Contract.id)).filter(Contract.status == "active").scalar() or 0
    open_risks = db_session.query(func.count(RiskFlag.id)).filter(RiskFlag.is_resolved.is_(False)).scalar() or 0
    annual_spend = db_session.query(func.coalesce(func.sum(Contract.annual_spend), 0)).scalar() or 0

    upcoming_contracts = (
        db_session.query(Contract)
        .join(Contract.vendor)
        .order_by(Contract.renewal_date.asc())
        .limit(6)
        .all()
    )
    risky_contracts = (
        db_session.query(RiskFlag)
        .join(RiskFlag.contract)
        .join(Contract.vendor)
        .filter(RiskFlag.is_resolved.is_(False))
        .order_by(RiskFlag.created_at.desc())
        .limit(5)
        .all()
    )

    return {
        "vendor_total": vendor_total,
        "active_contracts": active_contracts,
        "open_risks": open_risks,
        "annual_spend": float(annual_spend),
        "today": date.today().isoformat(),
        "upcoming_contracts": [
            {
                "id": contract.id,
                "vendor_code": contract.vendor.code,
                "vendor_name": contract.vendor.name,
                "title": contract.title,
                "renewal_date": contract.renewal_date.isoformat(),
                "status": contract.status,
            }
            for contract in upcoming_contracts
        ],
        "risky_contracts": [
            {
                "contract_id": risk.contract.id,
                "vendor_code": risk.contract.vendor.code,
                "severity": risk.severity,
                "title": risk.title,
                "created_at": risk.created_at.isoformat(timespec="minutes"),
            }
            for risk in risky_contracts
        ],
    }
