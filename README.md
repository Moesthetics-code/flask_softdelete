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

```bash
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_softdelete import SoftDeleteMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
db = SQLAlchemy(app)
```

## Usage

```bash
class SampleModel(db.Model, SoftDeleteMixin):
    __tablename__ = 'sample_model'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
```

## Record Management Methods

Flask-Softdelete provides methods for managing soft delete functionality:

soft_delete(): Marks the record as deleted, but keeps it in the database.
restore(): Restores a soft-deleted record, making it active again.
force_delete(): Permanently removes the record from the database, which cannot be undone.

## Examples

# Create a new record

```bash
sample = SampleModel(name="Example")
db.session.add(sample)
db.session.commit()

# Soft delete the record
sample.soft_delete()

# Restore the record
sample.restore()

# Permanently delete the record
sample.force_delete()
```

## Logging

```bash
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

This project is licensed under the MIT License. See the LICENSE file for more details.


### Changements Apportés :
1. **Installation** : Ajout de détails sur l'installation de Flask et Flask-SQLAlchemy.
2. **Configuration** : Précisions sur l'URI de la base de données.
3. **Usage** : Clarifications sur l'héritage de modèle et les méthodes de gestion.
4. **Exemples** : Exemple d'utilisation de chaque méthode.
5. **Logging** : Explication de la configuration du logging.
6. **Contributing** : Ajout d'informations sur la manière de contribuer et de signaler des problèmes.

Ces ajouts rendent chaque section plus informative et permettent aux utilisateurs de mieux comprendre comment utiliser votre module `Flask-Softdelete`.


