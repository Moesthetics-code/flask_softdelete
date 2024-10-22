Examples
========

Create new record
=================

.. code-block:: python

    sample = SampleModel(name="Example")
    db.session.add(sample)
    db.session.commit()


Soft delete the record
======================

.. code-block:: python

    sample.soft_delete(user_id=1)


Restore the record
==================

.. code-block:: python

    sample.restore(user_id=1)


Permanently delete the record
=============================

.. code-block:: python

    sample.force_delete()


Retrieve All Active Records
===========================

.. code-block:: python

    active_records = SampleModel.get_active()


Retrieve All Deleted Records
============================

.. code-block:: python

    deleted_records = SampleModel.get_deleted()


Permanently Delete All Deleted Records
======================================

.. code-block:: python

    SampleModel.force_delete_all_deleted()


Restore All Deleted Records
===========================

.. code-block:: python

    SampleModel.restore_all()


Logging
=======

.. code-block:: python

    import logging

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Log soft delete action
    logger.info(f"Soft deleted record with ID: {sample.id}")
