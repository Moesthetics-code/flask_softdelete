from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from flask import current_app
import logging

# Initialize SQLAlchemy instance
db = SQLAlchemy()

class SoftDeleteMixin:
    """
    Mixin class for adding soft delete functionality to SQLAlchemy models.
    Provides methods to mark records as deleted, restore them, and permanently delete records.
    """

    # Define the columns needed for soft delete functionality
    deleted_at = db.Column(db.DateTime, nullable=True)  # Timestamp when the record was soft-deleted
    deleted_by = db.Column(db.Integer, nullable=True)  # Optional: ID of the user who soft-deleted the record
    restored_by = db.Column(db.Integer, nullable=True)  # Optional: ID of the user who restored the record

    def soft_delete(self, user_id=None):
        """
        Mark the current record as soft-deleted by setting the `deleted_at` timestamp
        and optionally the ID of the user performing the deletion.

        Parameters:
        - user_id (int, optional): The ID of the user performing the soft delete.
        """
        try:
            self.deleted_at = datetime.now(timezone.utc)  # Set the deletion timestamp
            if user_id:
                self.deleted_by = user_id  # Record the ID of the user who performed the deletion

            db.session.flush()  # Flush changes to the database without committing
            current_app.logger.info(f"Record soft-deleted by user {user_id} at {self.deleted_at}")
        except Exception as e:
            current_app.logger.error(f"Error soft-deleting record: {str(e)}")
            db.session.rollback()  # Rollback the transaction in case of error

    def restore(self, user_id=None):
        """
        Restore a soft-deleted record by resetting the `deleted_at` field to None
        and optionally setting the ID of the user who restored it.

        Parameters:
        - user_id (int, optional): The ID of the user performing the restoration.
        """
        try:
            self.deleted_at = None  # Clear the deletion timestamp
            self.deleted_by = None  # Clear the user who deleted
            if user_id:
                self.restored_by = user_id  # Record the user performing the restoration

            db.session.commit()  # Commit the changes to the database
            current_app.logger.info(f"Record restored by user {user_id}")
        except Exception as e:
            current_app.logger.error(f"Error restoring record: {str(e)}")
            db.session.rollback()

    @classmethod
    def get_active(cls):
        """
        Retrieve all records that have not been soft-deleted.

        Returns:
        - list: A list of active (non-soft-deleted) records.
        """
        try:
            active_records = cls.query.filter_by(deleted_at=None).all()
            current_app.logger.info(f"Retrieved {len(active_records)} active records")
            return active_records
        except Exception as e:
            current_app.logger.error(f"Error retrieving active records: {str(e)}")
            return []

    @classmethod
    def get_deleted(cls):
        """
        Retrieve all records that have been soft-deleted.

        Returns:
        - list: A list of soft-deleted records.
        """
        try:
            deleted_records = cls.query.filter(cls.deleted_at.isnot(None)).all()
            current_app.logger.info(f"Retrieved {len(deleted_records)} soft-deleted records")
            return deleted_records
        except Exception as e:
            current_app.logger.error(f"Error retrieving deleted records: {str(e)}")
            return []

    def force_delete(self):
        """
        Permanently delete the current record from the database.
        """
        try:
            db.session.expunge(self)  # Remove the object from the current session
            db.session.delete(self)  # Mark the object for deletion
            db.session.commit()  # Commit the deletion
            current_app.logger.info("Record permanently deleted")
        except Exception as e:
            current_app.logger.error(f"Error force-deleting record: {str(e)}")
            db.session.rollback()

    @classmethod
    def force_delete_all_deleted(cls):
        """
        Permanently delete all soft-deleted records from the database.
        """
        try:
            deleted_records = cls.query.filter(cls.deleted_at.isnot(None)).all()
            for record in deleted_records:
                record.force_delete()  # Call the `force_delete` method for each record
            current_app.logger.info(f"Permanently deleted {len(deleted_records)} soft-deleted records")
        except Exception as e:
            current_app.logger.error(f"Error force-deleting all deleted records: {str(e)}")
            db.session.rollback()

    @classmethod
    def restore_all(cls):
        """
        Restore all soft-deleted records by resetting their `deleted_at` field to None.
        """
        try:
            deleted_records = cls.query.filter(cls.deleted_at.isnot(None)).all()
            for record in deleted_records:
                record.deleted_at = None
                record.deleted_by = None  # Clear the user who deleted

            db.session.commit()  # Commit the changes to the database
            current_app.logger.info(f"Restored {len(deleted_records)} soft-deleted records")
        except Exception as e:
            current_app.logger.error(f"Error restoring all soft-deleted records: {str(e)}")
            db.session.rollback()
