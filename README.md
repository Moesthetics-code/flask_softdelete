# Flask-Softdelete

Flask-SoftDelete is a simple extension for Flask applications that adds soft delete functionality to Flask-SQLAlchemy models. Instead of permanently deleting records, soft deleting allows you to mark records as "deleted" without actually removing them from the database. This is useful for keeping a history of deleted records or allowing for easy restoration.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Base Model](#base-model)
  - [Record Management Methods](#record-management-methods)
- [Examples](#examples)
- [Logging](#logging)
- [Contributing](#contributing)
- [License](#license)

## Installation

To install Flask-Softdelete, use pip:

```bash
pip install Flask-Softdelete
```

## Configuration

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_softdelete import SoftDeleteMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
db = SQLAlchemy(app)
```

## Usage

## Base Model

```python
class SampleModel(db.Model, SoftDeleteMixin):
    __tablename__ = 'sample_model'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
```

## Record Management Methods

Flask-Softdelete provides the following methods for managing soft delete functionality:

soft_delete(user_id=None): Marks the record as deleted by setting a deleted_at timestamp. You can also specify the ID of the user who performed the deletion.

restore(user_id=None): Restores a soft-deleted record by resetting deleted_at. You can also specify the ID of the user who performed the restoration.

force_delete(): Permanently removes the record from the database, an action that cannot be undone.

get_active(): Retrieves all records that are not soft-deleted.

get_deleted(): Retrieves only the records that have been soft-deleted.

force_delete_all_deleted(): Permanently deletes all records that have been soft-deleted.

restore_all(): Restores all soft-deleted records.

## Examples

# Create a new record

```python
sample = SampleModel(name="Example")
db.session.add(sample)
db.session.commit()
```

# Soft delete the record

```python
sample.soft_delete(user_id=1)
```

# Restore the record

```python
sample.restore(user_id=1)
```

# Permanently delete the record

```python
sample.force_delete()
```

# Retrieve All Active Records

```python
active_records = SampleModel.get_active()
```

# Retrieve All Deleted Records

```python
deleted_records = SampleModel.get_deleted()
```

# Permanently Delete All Deleted Records

```python
SampleModel.force_delete_all_deleted()
```

# Restore All Deleted Records

```python
SampleModel.restore_all()
```

## Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log soft delete action
logger.info(f"Soft deleted record with ID: {sample.id}")
```

## Contributing

If you would like to contribute to Flask-Softdelete, please fork the repository and submit a pull request. You can find the repository on GitHub.

## Reporting Issues

If you encounter any issues, please report them in the Issues section of the GitHub repository. This helps improve the package and assists others who might face similar issues.

## License

MIT License

Copyright (c) 2024 Mohamed Ndiaye

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

1. The above copyright notice and this permission notice shall be included in
   all copies or substantial portions of the Software.

2. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
   SOFTWARE.

```vbnet
This README provides a comprehensive overview of the Flask-SoftDelete module, including its installation, configuration, usage, methods, and examples. Let me know if you need any further adjustments or additions!
```
