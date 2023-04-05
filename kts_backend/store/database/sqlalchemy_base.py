"""
This module defines a base class for declarative models in SQLAlchemy.

Usage:
- Import this module to access the base class for creating model classes.
- Inherit from `db` when defining a model class.
"""

from sqlalchemy.orm import declarative_base

# Create a base class for declarative models
db = declarative_base()
