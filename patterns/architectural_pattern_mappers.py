import sqlite3
from creating_patterns import Student


class StudentMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'student'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            student = Student(name)
            student.id = id
            result.append(student)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, name FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Student(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, object):
        statement = f"INSERT INTO {self.tablename} (name) VALUES (?)"
        self.cursor.execute(statement, (object.name,))
        try:
            self.connection.commit()
        except Exception as error:
            raise DbCommitException(error.args)

    def update(self, object):
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"
        self.cursor.execute(statement, (object.name, object.id))
        try:
            self.connection.commit()
        except Exception as error:
            raise DbUpdateException(error.args)

    def delete(self, object):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (object.id),)
        try:
            self.connection.commit()
        except Exception as error:
            raise DbDeleteExeption(error.args)


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'data base commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'data base update error: {message}')


class DbDeleteExeption(Exception):
    def __init__(self, message):
        super().__init__(f'data base delete error: {message}')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')
