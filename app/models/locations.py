from app import db
import sqlalchemy as sa
import sqlalchemy.orm as so


class Permission:
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship("User", backref="role", lazy="dynamic")

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            "User": [Permission.WRITE],
            "AnonymousUser": [],
            "Moderator": [Permission.WRITE, Permission.MODERATE],
            "Administrator": [Permission.WRITE, Permission.MODERATE, Permission.ADMIN],
        }
        default_role = "AnonymousUser"
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = role.name == default_role
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return "<Role %r>" % self.name


class State(db.Model):
    __tablename__ = "states"
    abbreviation: so.Mapped[str] = so.mapped_column(sa.String(2), primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(50), nullable=False, unique=True)
    counties: so.WriteOnlyMapped["County"] = so.relationship(
        back_populates="state", cascade="all, delete-orphan"
    )
    rate_areas: so.WriteOnlyMapped["RateArea"] = so.relationship(
        back_populates="state", cascade="all, delete-orphan"
    )
    plans: so.WriteOnlyMapped["Plan"] = so.relationship(
        back_populates="state", cascade="all, delete-orphan"
    )
    zip_codes: so.WriteOnlyMapped["ZipCode"] = so.relationship(
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
    zip_codes: so.WriteOnlyMapped["ZipCode"] = so.relationship(
        back_populates="county", cascade="all, delete-orphan"
    )

    __table_args__ = (
        sa.UniqueConstraint("code", "state_abbreviation", name="uq_county_code_state"),
        sa.UniqueConstraint("name", "state_abbreviation", name="uq_county_name_state"),
        sa.Index("idx_counties_code", "code"),
        sa.Index("idx_counties_name", "name"),
        sa.Index("idx_counties_state", "state_abbreviation"),
    )
