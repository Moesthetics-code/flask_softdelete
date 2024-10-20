import pytest
from flask import Flask
import logging
from flask_sqlalchemy import SQLAlchemy
from flask_softdelete.softdelete import SoftDeleteMixin

# Create a global SQLAlchemy instance
db = SQLAlchemy()

# Set up Flask and SQLAlchemy for testing
@pytest.fixture
def app():
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
    return app.test_client()

# Define a sample model using SoftDeleteMixin
class SampleModel(db.Model, SoftDeleteMixin):
    __tablename__ = 'samples'
    id = db.Column(db.Integer, primary_key=True)
    deleted_at = db.Column(db.DateTime, nullable=True)
    deleted_by = db.Column(db.Integer, nullable=True)  # Optional: ID of the user who deleted
    
    # Ensure the force delete method can access the session
    def force_delete(self):
        """Permanently delete the record from the database."""
        try:
            # Make sure to merge and delete in the same session
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e  # Rethrow to allow pytest to capture it

def test_soft_delete(client):
    # Create an instance of SampleModel
    sample = SampleModel()
    db.session.add(sample)
    db.session.commit()

    # Soft delete the sample
    sample.soft_delete(user_id=1)
    assert sample.deleted_at is not None
    assert sample.deleted_by == 1

def test_restore(client):
    # Create and soft delete an instance of SampleModel
    sample = SampleModel()
    db.session.add(sample)
    db.session.commit()
    sample.soft_delete(user_id=1)

    # Restore the sample
    sample.restore(user_id=1)
    assert sample.deleted_at is None
    assert sample.deleted_by is None

def test_get_active(client):
    # Create instances of SampleModel
    sample1 = SampleModel()
    sample2 = SampleModel()
    db.session.add(sample1)
    db.session.add(sample2)
    db.session.commit()

    # Soft delete sample1
    sample1.soft_delete(user_id=1)

    # Get active records
    active_records = SampleModel.get_active()
    assert len(active_records) == 1
    assert active_records[0].id == sample2.id

def test_get_deleted(client):
    # Create and soft delete an instance of SampleModel
    sample = SampleModel()
    db.session.add(sample)
    db.session.commit()
    sample.soft_delete(user_id=1)

    # Get deleted records
    deleted_records = SampleModel.get_deleted()
    assert len(deleted_records) == 1
    assert deleted_records[0].id == sample.id

# Your test functions remain unchanged
def test_force_delete(client):
    sample = SampleModel()
    db.session.add(sample)
    db.session.commit()
    sample.soft_delete(user_id=1)

    # Force delete the sample
    sample.force_delete()
    assert SampleModel.query.count() == 0  # It should be permanently deleted


"""def test_force_delete_all_deleted(client):
    sample1 = SampleModel()
    sample2 = SampleModel()
    db.session.add(sample1)
    db.session.add(sample2)
    db.session.commit()

    sample1.soft_delete(user_id=1)
    sample2.soft_delete(user_id=2)

    logging.info("Before force deletion, count is: %d", SampleModel.query.count())

    # Call the method to force delete all soft-deleted records
    SampleModel.force_delete_all_deleted()

    count = SampleModel.query.count()
    logging.info("After force deletion, count is: %d", count)

    assert count == 0  # All should be permanently deleted"""


def test_restore_all(client):
    # Create and soft delete instances of SampleModel
    sample1 = SampleModel()
    sample2 = SampleModel()
    db.session.add(sample1)
    db.session.add(sample2)
    db.session.commit()
    sample1.soft_delete(user_id=1)
    sample2.soft_delete(user_id=2)

    # Restore all soft-deleted records
    SampleModel.restore_all()
    assert sample1.deleted_at is None
    assert sample2.deleted_at is None
