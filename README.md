# Databases autotest compare project

Wargaming internship task

Tools and instruments used in project:
- pytest
- peewee

_task.txt_ contents the task text

## To start tests

Install required packages
```sh
pip install -r \path\to\requirements.txt
```
To create initial database run db_model.py
```sh
python .\models\db_model.py
```
Start tests
```sh
pytest -v .\tests\test_compare_dbs.py
```