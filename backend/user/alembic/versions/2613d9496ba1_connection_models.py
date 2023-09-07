"""Connection models

Revision ID: 2613d9496ba1
Revises: 
Create Date: 2023-09-02 22:46:06.631670

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "2613d9496ba1"
down_revision = None
branch_labels = None
depends_on = None

# Creating ENUM types
gender_enum = postgresql.ENUM(
    "Male",
    "Female",
    "Non-Binary",
    "Transgender",
    "Other",
    "Prefer Not To Say",
    name="gender",
    metadata=sa.MetaData(),
)
connection_status_enum = postgresql.ENUM(
    "Pending", "Accepted", "Blocked", name="connectionstatus", metadata=sa.MetaData()
)


def upgrade() -> None:
    # Create the enum types
    conn = op.get_bind()
    gender_enum.create(conn)
    connection_status_enum.create(conn)

    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "userprofile",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("first_name", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("last_name", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("date_of_birth", sa.DateTime(), nullable=True),
        sa.Column("gender", gender_enum, nullable=True),
        sa.Column("interested_in_gender", gender_enum, nullable=True),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_userprofile_user_id"), "userprofile", ["user_id"], unique=True
    )
    op.create_table(
        "connection",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_profile1_id", sa.Integer(), nullable=True),
        sa.Column("user_profile2_id", sa.Integer(), nullable=True),
        sa.Column("status", connection_status_enum, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_profile1_id"],
            ["userprofile.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_profile2_id"],
            ["userprofile.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_connection_user_profile1_id"),
        "connection",
        ["user_profile1_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_connection_user_profile2_id"),
        "connection",
        ["user_profile2_id"],
        unique=False,
    )
    op.create_table(
        "profilephoto",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_profile_id", sa.Integer(), nullable=True),
        sa.Column("url", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("caption", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("is_main", sa.Boolean(), nullable=False),
        sa.Column("uploaded_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_profile_id"],
            ["userprofile.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_profilephoto_user_profile_id"),
        "profilephoto",
        ["user_profile_id"],
        unique=False,
    )
    op.create_table(
        "userprofiledetails",
        sa.Column("user_profile_id", sa.Integer(), nullable=False),
        sa.Column("bio", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("job_title", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("company", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("school", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("hobbies", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("favorite_music", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("favorite_movies", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("favorite_books", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_profile_id"],
            ["userprofile.id"],
        ),
        sa.PrimaryKeyConstraint("user_profile_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("userprofiledetails")
    op.drop_index(op.f("ix_profilephoto_user_profile_id"), table_name="profilephoto")
    op.drop_table("profilephoto")
    op.drop_index(op.f("ix_connection_user_profile2_id"), table_name="connection")
    op.drop_index(op.f("ix_connection_user_profile1_id"), table_name="connection")
    op.drop_table("connection")
    op.drop_index(op.f("ix_userprofile_user_id"), table_name="userprofile")
    op.drop_table("userprofile")

    # Drop the enum types
    conn = op.get_bind()
    gender_enum.drop(conn)
    connection_status_enum.drop(conn)

    # ### end Alembic commands ###
