"""hui

Revision ID: dba6f8e4d20c
Revises: 
Create Date: 2024-05-15 22:01:42.960229

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "dba6f8e4d20c"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "chats",
        sa.Column("name", sa.String(length=32), nullable=False),
        sa.Column("chat_picture", sa.LargeBinary(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "users",
        sa.Column("profile_picture", sa.LargeBinary(), nullable=True),
        sa.Column("username", sa.String(length=32), nullable=False),
        sa.Column("first_name", sa.String(length=32), server_default="", nullable=False),
        sa.Column("last_name", sa.String(length=32), server_default="", nullable=False),
        sa.Column("password_hash", sa.LargeBinary(), server_default="", nullable=False),
        sa.Column("public_key", sa.String(), server_default="", nullable=False),
        sa.Column("enc_private_key", sa.String(), server_default="", nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.create_table(
        "messages",
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column("body", sa.Text(), server_default="", nullable=False),
        sa.Column("sender_user_id", sa.Integer(), nullable=False),
        sa.Column("chat_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["chat_id"],
            ["chats.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user_chat_association",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("chat_id", sa.Integer(), nullable=False),
        sa.Column("password", sa.String(), server_default="", nullable=False),
        sa.ForeignKeyConstraint(
            ["chat_id"],
            ["chats.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user_chat_association")
    op.drop_table("messages")
    op.drop_table("users")
    op.drop_table("chats")
    # ### end Alembic commands ###
