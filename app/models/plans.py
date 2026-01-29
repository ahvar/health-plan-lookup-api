from app import db
import sqlalchemy as sa
import sqlalchemy.orm as so


class RateArea(db.Model):
    __tablename__ = "rate_areas"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    state_abbreviation: so.Mapped[str] = so.mapped_column(
        sa.String(2),
        sa.ForeignKey("states.abbreviation", ondelete="CASCADE"),
        nullable=False,
    )
    area_number: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)

    state: so.Mapped["State"] = so.relationship(back_populates="rate_areas")
    zip_codes: so.WriteOnlyMapped["ZipCode"] = so.relationship(
        back_populates="rate_area", cascade="all, delete-orphan"
    )
    plans: so.WriteOnlyMapped["Plan"] = so.relationship(
        back_populates="rate_area", cascade="all, delete-orphan"
    )

    __table_args__ = (
        sa.UniqueConstraint(
            "state_abbreviation", "area_number", name="uq_rate_area_state_number"
        ),
        sa.Index("idx_rate_areas_state", "state_abbreviation"),
        sa.Index("idx_rate_areas_number", "area_number"),
    )


class Plan(db.Model):
    __tablename__ = "plans"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    plan_id: so.Mapped[str] = so.mapped_column(sa.String(20), nullable=False, unique=True)
    state_abbreviation: so.Mapped[str] = so.mapped_column(
        sa.String(2),
        sa.ForeignKey("states.abbreviation", ondelete="CASCADE"),
        nullable=False,
    )
    metal_level: so.Mapped[str] = so.mapped_column(sa.String(20), nullable=False)
    rate: so.Mapped[float] = so.mapped_column(sa.Numeric(10, 2), nullable=False)
    rate_area_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("rate_areas.id", ondelete="CASCADE"), nullable=False
    )

    state: so.Mapped["State"] = so.relationship(back_populates="plans")
    rate_area: so.Mapped["RateArea"] = so.relationship(back_populates="plans")

    __table_args__ = (
        sa.Index("idx_plans_plan_id", "plan_id"),
        sa.Index("idx_plans_state", "state_abbreviation"),
        sa.Index("idx_plans_metal", "metal_level"),
        sa.Index("idx_plans_rate_area", "rate_area_id"),
    )


class ZipCode(db.Model):
    __tablename__ = "zip_codes"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    zipcode: so.Mapped[str] = so.mapped_column(sa.String(5), nullable=False)
    state_abbreviation: so.Mapped[str] = so.mapped_column(
        sa.String(2),
        sa.ForeignKey("states.abbreviation", ondelete="CASCADE"),
        nullable=False,
    )
    county_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("counties.id", ondelete="CASCADE"), nullable=False
    )
    rate_area_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("rate_areas.id", ondelete="CASCADE"), nullable=False
    )

    state: so.Mapped["State"] = so.relationship(back_populates="zip_codes")
    county: so.Mapped["County"] = so.relationship(back_populates="zip_codes")
    rate_area: so.Mapped["RateArea"] = so.relationship(back_populates="zip_codes")
    __table_args__ = (
        sa.UniqueConstraint(
            "zipcode",
            "state_abbreviation",
            "county_id",
            name="uq_zipcode_state_county",
        ),
        sa.Index("idx_zip_codes_zip", "zipcode"),
        sa.Index("idx_zip_codes_state", "state_abbreviation"),
        sa.Index("idx_zip_codes_county", "county_id"),
        sa.Index("idx_zip_codes_rate_area", "rate_area_id"),
    )


class SlcspRequest(db.Model):
    __tablename__ = "slcsp_requests"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    zipcode: so.Mapped[str] = so.mapped_column(sa.String(5), nullable=False)

    __table_args__ = (sa.Index("idx_slcsp_zip", "zipcode"),)
