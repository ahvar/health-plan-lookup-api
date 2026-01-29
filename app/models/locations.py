from app import db
import sqlalchemy as sa
import sqlalchemy.orm as so
from datetime import datetime


class State(db.Model):
    __tablename__ = "states"
    abbreviation: so.Mapped[str] = so.mapped_column(sa.String(2), primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(50), nullable=False, unique=True)
    counties: so.WriteOnlyMapped["County"] = so.relationship(
        back_populates="state", cascade="all, delete-orphan"
    )

    __table_args__ = sa.Index("idx_states_name", "name")


class County(db.Model):
    __tablename__ = "counties"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    code: so.Mapped[str] = so.mapped_column(sa.String(5), nullable=False, unique=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(120), unique=True, nullable=False)
    state_abbreviation: so.Mapped[str] = so.mapped_column(
        sa.String(2),
        sa.ForeignKey("states.abbreviation", ondelete="CASCADE"),
        nullable=False,
    )

    state: so.Mapped["State"] = so.relationship(back_populates="counties")

    __table_args__ = (
        sa.UniqueConstraint("code", "state_abbreviation", name="uq_county_code_state"),
        sa.UniqueConstraint("name", "state_abbreviation", name="uq_county_name_state"),
        sa.Index("idx_counties_code", "code"),
        sa.Index("idx_counties_name", "name"),
        sa.Index("idx_counties_state", "state_abbreviations"),
    )
