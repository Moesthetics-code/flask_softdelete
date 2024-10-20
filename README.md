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
