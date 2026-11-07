"""baseline

Revision ID: 7d3c298b811b
Revises:
Create Date: 2026-11-05 18:11:43.675062

"""

from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "7d3c298b811b"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
