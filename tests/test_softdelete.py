"""
This module demonstrates the usage of Flask, SQLAlchemy, and the SoftDeleteMixin for managing soft-deleted records in a database. 
It includes a sample model, test configurations, and multiple test cases for validating soft deletion, restoration, and permanent deletion of records.
"""

import pytest
from flask import Flask
import logging
from flask_sqlalchemy import SQLAlchemy
from flask_softdelete.softdelete import SoftDeleteMixin

# Create a global SQLAlchemy instance
db = SQLAlchemy()

@pytest.fixture
def app():
    """
    Pytest fixture to set up a Flask application for testing purposes.
    - Configures an in-memory SQLite database for isolation during tests.
    - Initializes the global SQLAlchemy instance with the application.
    - Ensures database tables are created and dropped around the test's execution.

    Yields:
        Flask app instance: Configured Flask application for testing.
    """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory SQLite database
    app.config['TESTING'] = True

    db.init_app(app)  # Initialize the db with the app

    with app.app_context():
        db.create_all()
        yield app  # Yield only the app
        db.drop_all()

@pytest.fixture
def client(app):
    """
    Pytest fixture to set up a test client for the Flask application.

    Args:
        app (Flask): The test Flask application.

    Returns:
        Flask test client: Provides testing capabilities like sending requests.
    """
    return app.test_client()

class SampleModel(db.Model, SoftDeleteMixin):
    """
    A sample database model that demonstrates the integration of SQLAlchemy 
    with soft deletion functionality via SoftDeleteMixin.

    Attributes:
        id (int): Primary key of the record.
        deleted_at (datetime): Timestamp when the record was soft deleted.
        deleted_by (int): ID of the user who performed the soft delete.
    """
    __tablename__ = 'samples'
    id = db.Column(db.Integer, primary_key=True)
    deleted_at = db.Column(db.DateTime, nullable=True)
    deleted_by = db.Column(db.Integer, nullable=True)  # Optional: ID of the user who deleted
    
    def force_delete(self):
        """
        Permanently deletes the record from the database.

        Raises:
            Exception: If an error occurs during the delete operation.
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e  # Rethrow to allow pytest to capture it

def test_soft_delete(client):
    """
    Test case for verifying the soft deletion of a record.

    - Creates a SampleModel instance.
    - Soft deletes the instance and verifies the 'deleted_at' and 'deleted_by' fields.
    """
    sample = SampleModel()
    db.session.add(sample)
    db.session.commit()

    sample.soft_delete(user_id=1)
    assert sample.deleted_at is not None
    assert sample.deleted_by == 1

def test_restore(client):
    """
    Test case for verifying the restoration of a soft-deleted record.

    - Soft deletes a SampleModel instance.
    - Restores the instance and verifies the 'deleted_at' and 'deleted_by' fields are reset.
    """
    sample = SampleModel()
    db.session.add(sample)
    db.session.commit()
    sample.soft_delete(user_id=1)

    sample.restore(user_id=1)
    assert sample.deleted_at is None
    assert sample.deleted_by is None

def test_get_active(client):
    """
    Test case for retrieving only active (non-deleted) records.

    - Creates two SampleModel instances.
    - Soft deletes one instance.
    - Ensures only the non-deleted instance is retrieved as active.
    """
    sample1 = SampleModel()
    sample2 = SampleModel()
    db.session.add(sample1)
    db.session.add(sample2)
    db.session.commit()

    sample1.soft_delete(user_id=1)

    active_records = SampleModel.get_active()
    assert len(active_records) == 1
    assert active_records[0].id == sample2.id

def test_get_deleted(client):
    """
    Test case for retrieving only soft-deleted records.

    - Creates and soft deletes a SampleModel instance.
    - Ensures the soft-deleted instance is retrieved.
    """
    sample = SampleModel()
    db.session.add(sample)
    db.session.commit()
    sample.soft_delete(user_id=1)

    deleted_records = SampleModel.get_deleted()
    assert len(deleted_records) == 1
    assert deleted_records[0].id == sample.id

def test_force_delete(client):
    """
    Test case for verifying permanent deletion of a soft-deleted record.

    - Soft deletes a SampleModel instance.
    - Permanently deletes the instance and ensures it no longer exists in the database.
    """
    sample = SampleModel()
    db.session.add(sample)
    db.session.commit()
    sample.soft_delete(user_id=1)

    sample.force_delete()
    assert SampleModel.query.count() == 0

def test_force_delete_all_deleted(client):
    """
    Test case for permanently deleting all soft-deleted records.

    - Creates and soft deletes two SampleModel instances.
    - Permanently deletes all soft-deleted instances and verifies no records remain.
    """
    sample1 = SampleModel()
    sample2 = SampleModel()
    db.session.add(sample1)
    db.session.add(sample2)
    db.session.commit()

    sample1.soft_delete(user_id=1)
    sample2.soft_delete(user_id=2)

    logging.info("Before force deletion, count is: %d", SampleModel.query.count())

    SampleModel.force_delete_all_deleted()

    count = SampleModel.query.count()
    logging.info("After force deletion, count is: %d", count)

    assert count == 0

def test_restore_all(client):
    """
    Test case for restoring all soft-deleted records.

    - Creates and soft deletes two SampleModel instances.
    - Restores all soft-deleted instances and verifies their 'deleted_at' fields are reset.
    """
    sample1 = SampleModel()
    sample2 = SampleModel()
    db.session.add(sample1)
    db.session.add(sample2)
    db.session.commit()
    sample1.soft_delete(user_id=1)
    sample2.soft_delete(user_id=2)

    SampleModel.restore_all()
    assert sample1.deleted_at is None
    assert sample2.deleted_at is None
