"""initial_schema

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-09-16 12:15:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '001_initial_schema'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # -------------------------------------------------------------------------
    # 1. Table: locations
    # -------------------------------------------------------------------------
    op.create_table(
        'locations',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('administrative_type', sa.String(), nullable=False),
        sa.Column('state_code', sa.String(length=10), nullable=False),
        sa.Column('capital', sa.String(), nullable=True),
        sa.Column('region', sa.String(), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_locations_id'), 'locations', ['id'], unique=False)
    op.create_index(op.f('ix_locations_name'), 'locations', ['name'], unique=False)
    op.create_index(op.f('ix_locations_administrative_type'), 'locations', ['administrative_type'], unique=False)
    op.create_index(op.f('ix_locations_state_code'), 'locations', ['state_code'], unique=False)
    op.create_index(op.f('ix_locations_region'), 'locations', ['region'], unique=False)

    # -------------------------------------------------------------------------
    # 2. Table: disaster_events
    # -------------------------------------------------------------------------
    op.create_table(
        'disaster_events',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('location_id', sa.String(), nullable=False),
        sa.Column('disaster_type', sa.String(), nullable=False),
        sa.Column('severity', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('source', sa.String(), nullable=True),
        sa.Column('source_url', sa.String(), nullable=True),
        sa.Column('is_demo', sa.Boolean(), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('ended_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_disaster_events_location_id'), 'disaster_events', ['location_id'], unique=False)
    op.create_index(op.f('ix_disaster_events_disaster_type'), 'disaster_events', ['disaster_type'], unique=False)
    op.create_index(op.f('ix_disaster_events_severity'), 'disaster_events', ['severity'], unique=False)
    op.create_index(op.f('ix_disaster_events_status'), 'disaster_events', ['status'], unique=False)
    op.create_index(op.f('ix_disaster_events_started_at'), 'disaster_events', ['started_at'], unique=False)

    # -------------------------------------------------------------------------
    # 3. Table: risk_assessments
    # -------------------------------------------------------------------------
    op.create_table(
        'risk_assessments',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('location_id', sa.String(), nullable=False),
        sa.Column('disaster_type', sa.String(), nullable=False),
        sa.Column('risk_score', sa.Integer(), nullable=False),
        sa.Column('risk_level', sa.String(), nullable=False),
        sa.Column('model_version', sa.String(), nullable=True),
        sa.Column('assessment_status', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_risk_assessments_location_id'), 'risk_assessments', ['location_id'], unique=False)

    # -------------------------------------------------------------------------
    # 4. Table: risk_factors
    # -------------------------------------------------------------------------
    op.create_table(
        'risk_factors',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('assessment_id', sa.String(), nullable=False),
        sa.Column('factor_name', sa.String(), nullable=False),
        sa.Column('factor_value', sa.String(), nullable=False),
        sa.Column('importance', sa.String(), nullable=True),
        sa.Column('unit', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['assessment_id'], ['risk_assessments.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_risk_factors_assessment_id'), 'risk_factors', ['assessment_id'], unique=False)

    # -------------------------------------------------------------------------
    # 5. Table: resources
    # -------------------------------------------------------------------------
    op.create_table(
        'resources',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('resource_type', sa.String(), nullable=False),
        sa.Column('category', sa.String(), nullable=True),
        sa.Column('location_id', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('website', sa.String(), nullable=True),
        sa.Column('phone', sa.String(), nullable=True),
        sa.Column('verification_status', sa.String(), nullable=True),
        sa.Column('last_verified', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_resources_name'), 'resources', ['name'], unique=False)
    op.create_index(op.f('ix_resources_resource_type'), 'resources', ['resource_type'], unique=False)
    op.create_index(op.f('ix_resources_category'), 'resources', ['category'], unique=False)
    op.create_index(op.f('ix_resources_location_id'), 'resources', ['location_id'], unique=False)
    op.create_index(op.f('ix_resources_verification_status'), 'resources', ['verification_status'], unique=False)


def downgrade() -> None:
    op.drop_table('resources')
    op.drop_table('risk_factors')
    op.drop_table('risk_assessments')
    op.drop_table('disaster_events')
    op.drop_table('locations')
