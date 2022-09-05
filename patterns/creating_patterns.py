import copy
import quopri
import sqlite3

from .behavior_patterns import Subject, ConsoleWriter
from .architectural_system_pattern import DomainObject


# абстрактный пользователь:
class User:
    def __init__(self, name):
        self.name = name


# абстрактный преподователь
class Teacher(User):
    pass


# абстрактный студент
class Student(User, DomainObject):

    def __init__(self, name):
        self.courses = []
        super().__init__(name)


# фабрика пользователей
class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher
    }

    @classmethod
    def create(cls, type_user, name):
        return cls.types[type_user](name)


# порождающий паттерн прототип - курс
class CoursePrototype:

    def clone(self):
        return copy.deepcopy(self)


# класс Курс
class Course(CoursePrototype, Subject):
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []
        super().__init__()

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student: Student):
        self.students.append(student)
        student.courses.append(self)
        self.notify()


# интерактивный курс
class InteractiveCourse(Course):
    pass


# записанный курс
class RecordCourse(Course):
    pass


# категория
class Category:
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1 # при инициализации класса счетчик id будет увеличиваться
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        # считает количество созданных экземпляров класса
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result


# фабрика курсов
class CourseFactory:
    types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse,
    }

    @classmethod
    def create(cls, type_course, name, category):
        return cls.types[type_course](name, category)


# основной интерфейс проекта
class Engine:
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    # создаем пользователя
    @staticmethod
    def create_user(type_user, name):
        return UserFactory.create(type_user, name)

    # создаем категории
    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    # поиск категорий
    def find_category_id(self, id):
        for category in self.categories:
            if category.id == id:
                return category
        raise Exception(f'Нет категории с id = {id}')

    # создаем курсы
    @staticmethod
    def create_course(type_course, name, category):
        return CourseFactory.create(type_course, name, category)

    # получение определенного курса
    def get_course(self, name):
        for course in self.courses:
            if course.name == name:
                return course
        return None

    def get_student(self, name) -> Student:
        for student in self.students:
            if student.name == name:
                return student

    # статик метод для исправления бага декодирования из ASCII
    @staticmethod
    def decode_value(val):
        val_byte = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = quopri.decodestring(val_byte)
        return val_decode_str.decode('UTF-8')


# порождающий паттерн Синглтон
class SingletonByName(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance['name']
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


# простой логгер
class Logger(metaclass=SingletonByName):
    def __init__(self, name, writer=ConsoleWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        print('log =->', text)
        text = f'log =-> {text}'
        self.writer.write(text)


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

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name) VALUES (?)"
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as error:
            raise DbCommitException(error.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"
        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as error:
            raise DbUpdateException(error.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as error:
            raise DbDeleteException(error.args)


connection = sqlite3.connect('patterns.sqlite')


class MapperRegistry:
    mappers = {
        'student': StudentMapper,
    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Student):
            return StudentMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')

class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')
