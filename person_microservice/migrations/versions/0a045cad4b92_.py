"""empty message

Revision ID: 0a045cad4b92
Revises: 487bd19c1edf
Create Date: 2022-04-17 18:17:57.042953

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
from models.booking.workday import Appointment

# revision identifiers, used by Alembic.
revision = "0a045cad4b92"
down_revision = "487bd19c1edf"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "appointment",
        sa.Column(
            "status",
            sqlalchemy_utils.types.choice.ChoiceType(Appointment.STATUS_TYPES),
            nullable=True,
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("appointment", "status")
    # ### end Alembic commands ###
