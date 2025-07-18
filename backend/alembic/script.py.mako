"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    """
    Upgrade the database schema.
    
    This function contains the forward migration logic.
    """
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    """
    Downgrade the database schema.
    
    This function contains the backward migration logic.
    WARNING: Downgrading may result in data loss.
    """
    ${downgrades if downgrades else "pass"}