from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from flask import current_app

db = SQLAlchemy()

class SoftDeleteMixin:
    """Mixin for adding soft delete functionality to SQLAlchemy models."""
    
    deleted_at = db.Column(db.DateTime, nullable=True)
    deleted_by = db.Column(db.Integer, nullable=True)  # Optional: ID of the user who deleted
    restored_by = db.Column(db.Integer, nullable=True)  # Optional: ID of the user who restored

    def soft_delete(self, user_id=None):
        """Mark the record as deleted by setting the deleted_at timestamp."""
        try:
            self.deleted_at = datetime.now(timezone.utc)  # Ensure timezone-aware datetime
            if user_id:
                self.deleted_by = user_id
            
            db.session.commit()
            current_app.logger.info(f"Record soft-deleted by user {user_id} at {self.deleted_at}")
        except Exception as e:
            current_app.logger.error(f"Error soft-deleting record: {str(e)}")
            db.session.rollback()  # Rollback the transaction if an error occurs


    def restore(self, user_id=None):
        """Restore a soft-deleted record by setting deleted_at to None."""
        try:
            self.deleted_at = None
            self.deleted_by = None  # Clear the user who deleted
            if user_id:
                self.restored_by = user_id

            db.session.commit()
            current_app.logger.info(f"Record restored by user {user_id}")
        except Exception as e:
            current_app.logger.error(f"Error restoring record: {str(e)}")
            db.session.rollback()

    @classmethod
    def get_active(cls):
        """Retrieve records that are not soft-deleted."""
        try:
            active_records = cls.query.filter_by(deleted_at=None).all()
            current_app.logger.info(f"Retrieved {len(active_records)} active records")
            return active_records
        except Exception as e:
            current_app.logger.error(f"Error retrieving active records: {str(e)}")
            return []

    @classmethod
    def get_deleted(cls):
        """Retrieve only soft-deleted records."""
        try:
            deleted_records = cls.query.filter(cls.deleted_at.isnot(None)).all()
            current_app.logger.info(f"Retrieved {len(deleted_records)} soft-deleted records")
            return deleted_records
        except Exception as e:
            current_app.logger.error(f"Error retrieving deleted records: {str(e)}")
            return []

    def force_delete(self):
        """Permanently delete the record from the database."""
        try:
            db.session.delete(self)  # Merge to ensure it's in the current session
            db.session.commit()
            current_app.logger.info("Record permanently deleted")
        except Exception as e:
            current_app.logger.error(f"Error force-deleting record: {str(e)}")
            db.session.rollback()

    """@classmethod
    def force_delete_all_deleted(cls):
       Permanently delete all soft-deleted records.
        try:
            deleted_records = cls.query.filter(cls.deleted_at.isnot(None)).all()
            for record in deleted_records:
                db.session.delete(db.session.merge(record))  # Merge to ensure it's in the current session

            db.session.commit()
            current_app.logger.info(f"Permanently deleted {len(deleted_records)} soft-deleted records")
        except Exception as e:
            current_app.logger.error(f"Error force-deleting all deleted records: {str(e)}")
            db.session.rollback()"""


    @classmethod
    def restore_all(cls):
        """Restore all soft-deleted records."""
        try:
            deleted_records = cls.query.filter(cls.deleted_at.isnot(None)).all()
            for record in deleted_records:
                record.deleted_at = None
                record.deleted_by = None

            db.session.commit()
            current_app.logger.info(f"Restored {len(deleted_records)} soft-deleted records")
        except Exception as e:
            current_app.logger.error(f"Error restoring all soft-deleted records: {str(e)}")
            db.session.rollback()