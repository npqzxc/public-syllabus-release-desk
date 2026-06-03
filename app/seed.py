from __future__ import annotations

from datetime import date, datetime

from .auth import hash_password
from .db import session_scope
from .models import Contract, ReviewNote, RiskFlag, User, Vendor


def ensure_seed_data() -> None:
    with session_scope() as session:
        if session.query(User).count() > 0:
            return

        users = [
            User(username="cora", display_name="Ivy Zhao", role="procurement_lead", password_hash=hash_password("course123")),
            User(username="marco", display_name="Marco Reyes", role="legal_partner", password_hash=hash_password("course123")),
            User(username="nina", display_name="Nina Patel", role="platform_manager", password_hash=hash_password("course123")),
            User(username="sofia", display_name="Sofia Kim", role="security_reviewer", password_hash=hash_password("course123")),
        ]
        session.add_all(users)
        session.flush()

        vendors = [
            Vendor(code="AURORA", name="Aurora Observability", category="infra", status="active", summary="核心观测平台，承担告警、追踪和审计查询能力。", owner_id=users[2].id, renewal_score=92),
            Vendor(code="ORBIT", name="Orbit CRM Sync", category="sales_ops", status="review", summary="负责销售线索同步和内容流程回流，最近被要求补齐数据保留条款。", owner_id=users[0].id, renewal_score=71),
            Vendor(code="LATTICE", name="Lattice Verify", category="security", status="risk", summary="为外包人员和课程提供身份校验，存在子处理方披露不充分问题。", owner_id=users[3].id, renewal_score=48),
            Vendor(code="EMBER", name="Ember Workspace", category="productivity", status="active", summary="内部文档和流程编排工具，续约窗口临近。", owner_id=users[1].id, renewal_score=83),
        ]
        session.add_all(vendors)
        session.flush()

        contracts = [
            Contract(vendor_id=vendors[0].id, title="Global Monitoring Enterprise 2026", status="active", annual_spend=185000, renewal_date=date(2026, 7, 12), auto_renew=True, sla_level="gold", procurement_stage="approved"),
            Contract(vendor_id=vendors[0].id, title="Log Archive Addendum", status="review", annual_spend=46000, renewal_date=date(2026, 6, 18), auto_renew=False, sla_level="silver", procurement_stage="legal_review"),
            Contract(vendor_id=vendors[1].id, title="CRM Sync Master Agreement", status="review", annual_spend=92000, renewal_date=date(2026, 8, 1), auto_renew=False, sla_level="silver", procurement_stage="security_review"),
            Contract(vendor_id=vendors[2].id, title="Identity Verification Expansion", status="risk", annual_spend=61000, renewal_date=date(2026, 6, 5), auto_renew=False, sla_level="gold", procurement_stage="risk_assessment"),
            Contract(vendor_id=vendors[3].id, title="Workspace Renewal 2026", status="draft", annual_spend=37000, renewal_date=date(2026, 5, 30), auto_renew=True, sla_level="bronze", procurement_stage="owner_review"),
        ]
        session.add_all(contracts)
        session.flush()

        notes = [
            ReviewNote(contract_id=contracts[0].id, author_id=users[2].id, note_type="operations", body="平台侧希望把追踪 retention 从 14 天提到 30 天，再评估加购成本。", created_at=datetime(2026, 5, 20, 9, 30)),
            ReviewNote(contract_id=contracts[1].id, author_id=users[1].id, note_type="legal", body="附加条款里缺少日志导出 SLA，法务要求补一版 redline。", created_at=datetime(2026, 5, 21, 14, 0)),
            ReviewNote(contract_id=contracts[2].id, author_id=users[0].id, note_type="business", body="销售运营要求六月中旬前完成签署，否则会影响季度回流报表。", created_at=datetime(2026, 5, 22, 11, 15)),
            ReviewNote(contract_id=contracts[3].id, author_id=users[3].id, note_type="security", body="课程尚未明确列出二级分包商名单，当前维持高风险状态。", created_at=datetime(2026, 5, 23, 16, 45)),
        ]
        session.add_all(notes)

        risks = [
            RiskFlag(contract_id=contracts[1].id, severity="medium", title="日志导出 SLA 未定义", description="附加条款没有约定日志导出时延和失败补偿。", is_resolved=False, created_at=datetime(2026, 5, 21, 13, 45)),
            RiskFlag(contract_id=contracts[2].id, severity="high", title="数据保留条款不完整", description="CRM 同步服务未明确删除请求处理时效。", is_resolved=False, created_at=datetime(2026, 5, 22, 9, 0)),
            RiskFlag(contract_id=contracts[3].id, severity="critical", title="子处理方披露不足", description="身份校验课程尚未交付最新分包清单。", is_resolved=False, created_at=datetime(2026, 5, 23, 16, 30)),
            RiskFlag(contract_id=contracts[4].id, severity="low", title="续约提醒时间过晚", description="当前只有自动续约前两天提醒，容易错过窗口。", is_resolved=False, created_at=datetime(2026, 5, 24, 10, 0)),
        ]
        session.add_all(risks)
