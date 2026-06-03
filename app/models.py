from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    display_name: Mapped[str] = mapped_column(String(120), nullable=False)
    role: Mapped[str] = mapped_column(String(80), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)

    vendors: Mapped[list["Vendor"]] = relationship(back_populates="owner")
    notes: Mapped[list["ReviewNote"]] = relationship(back_populates="author")


class Vendor(Base):
    __tablename__ = "vendors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    category: Mapped[str] = mapped_column(String(80), nullable=False)
    status: Mapped[str] = mapped_column(String(40), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    renewal_score: Mapped[int] = mapped_column(Integer, nullable=False, default=50)

    owner: Mapped[User] = relationship(back_populates="vendors")
    contracts: Mapped[list["Contract"]] = relationship(back_populates="vendor", cascade="all, delete-orphan")


class Contract(Base):
    __tablename__ = "contracts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    vendor_id: Mapped[int] = mapped_column(ForeignKey("vendors.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[str] = mapped_column(String(40), nullable=False)
    annual_spend: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    renewal_date: Mapped[date] = mapped_column(Date, nullable=False)
    auto_renew: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    sla_level: Mapped[str] = mapped_column(String(40), nullable=False)
    procurement_stage: Mapped[str] = mapped_column(String(40), nullable=False, default="review")

    vendor: Mapped[Vendor] = relationship(back_populates="contracts")
    review_notes: Mapped[list["ReviewNote"]] = relationship(back_populates="contract", cascade="all, delete-orphan")
    risk_flags: Mapped[list["RiskFlag"]] = relationship(back_populates="contract", cascade="all, delete-orphan")


class ReviewNote(Base):
    __tablename__ = "review_notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    contract_id: Mapped[int] = mapped_column(ForeignKey("contracts.id"), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    note_type: Mapped[str] = mapped_column(String(40), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    contract: Mapped[Contract] = relationship(back_populates="review_notes")
    author: Mapped[User] = relationship(back_populates="notes")


class RiskFlag(Base):
    __tablename__ = "risk_flags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    contract_id: Mapped[int] = mapped_column(ForeignKey("contracts.id"), nullable=False)
    severity: Mapped[str] = mapped_column(String(40), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    is_resolved: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    contract: Mapped[Contract] = relationship(back_populates="risk_flags")
