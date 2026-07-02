"""Initial schema.

Revision ID: 001
Revises:
Create Date: 2026-07-02
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("telegram_id", sa.BigInteger(), nullable=False),
        sa.Column("username", sa.String(length=255), nullable=True),
        sa.Column("display_name", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_telegram_id"), "users", ["telegram_id"], unique=True)

    op.create_table(
        "user_settings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("key", sa.String(length=100), nullable=False),
        sa.Column("value", sa.String(length=500), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_settings_user_id"), "user_settings", ["user_id"], unique=False)

    op.create_table(
        "training_sessions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("routine_name", sa.String(length=255), nullable=False),
        sa.Column("routine_version", sa.String(length=50), nullable=False),
        sa.Column("day_key", sa.String(length=50), nullable=False),
        sa.Column("warmup_type", sa.String(length=50), nullable=False),
        sa.Column("session_rpe", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_training_sessions_user_id"), "training_sessions", ["user_id"], unique=False)
    op.create_index(op.f("ix_training_sessions_status"), "training_sessions", ["status"], unique=False)

    op.create_table(
        "exercise_logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("session_id", sa.Integer(), nullable=False),
        sa.Column("exercise_key", sa.String(length=100), nullable=False),
        sa.Column("exercise_name", sa.String(length=255), nullable=False),
        sa.Column("order_index", sa.Integer(), nullable=False),
        sa.Column("sets_planned", sa.Integer(), nullable=False),
        sa.Column("reps_planned", sa.String(length=50), nullable=False),
        sa.Column("suggested_weight_kg", sa.Float(), nullable=True),
        sa.Column("weight_kg", sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(["session_id"], ["training_sessions.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_exercise_logs_session_id"), "exercise_logs", ["session_id"], unique=False)
    op.create_index(op.f("ix_exercise_logs_exercise_key"), "exercise_logs", ["exercise_key"], unique=False)

    op.create_table(
        "progression_tracking",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("exercise_key", sa.String(), nullable=False),
        sa.Column("week_start", sa.Date(), nullable=False),
        sa.Column("avg_session_rpe", sa.Float(), nullable=True),
        sa.Column("current_weight_kg", sa.Float(), nullable=False),
        sa.Column("weeks_at_current_weight", sa.Integer(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_progression_tracking_user_id"), "progression_tracking", ["user_id"], unique=False)
    op.create_index(op.f("ix_progression_tracking_exercise_key"), "progression_tracking", ["exercise_key"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_progression_tracking_exercise_key"), table_name="progression_tracking")
    op.drop_index(op.f("ix_progression_tracking_user_id"), table_name="progression_tracking")
    op.drop_table("progression_tracking")
    op.drop_index(op.f("ix_exercise_logs_exercise_key"), table_name="exercise_logs")
    op.drop_index(op.f("ix_exercise_logs_session_id"), table_name="exercise_logs")
    op.drop_table("exercise_logs")
    op.drop_index(op.f("ix_training_sessions_status"), table_name="training_sessions")
    op.drop_index(op.f("ix_training_sessions_user_id"), table_name="training_sessions")
    op.drop_table("training_sessions")
    op.drop_index(op.f("ix_user_settings_user_id"), table_name="user_settings")
    op.drop_table("user_settings")
    op.drop_index(op.f("ix_users_telegram_id"), table_name="users")
    op.drop_table("users")
