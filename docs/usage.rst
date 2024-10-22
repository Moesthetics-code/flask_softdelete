Usage
=====

Base models
===========

.. code-block:: python

    from flask_softdelete import SoftDeleteMixin
    from flask_sqlalchemy import SQLAlchemy

    db = SQLAlchemy()

    class SampleModel(db.Model, SoftDeleteMixin):
        __tablename__ = 'sample_model'

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(50))


Record Management Methods
=========================

Flask-Softdelete provides the following methods for managing soft delete functionality:

soft_delete(user_id=None): Marks the record as deleted by setting a deleted_at timestamp. You can also specify the ID of the user who performed the deletion.

restore(user_id=None): Restores a soft-deleted record by resetting deleted_at. You can also specify the ID of the user who performed the restoration.

force_delete(): Permanently removes the record from the database, an action that cannot be undone.

get_active(): Retrieves all records that are not soft-deleted.

get_deleted(): Retrieves only the records that have been soft-deleted.

force_delete_all_deleted(): Permanently deletes all records that have been soft-deleted.

restore_all(): Restores all soft-deleted records.