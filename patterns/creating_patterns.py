import copy
import quopri


# abstract user:
class User:
    pass


# abstract teacher
class Teacher(User):
    pass


# abstract student
class Student(User):
    pass


# фабрика пользователей
class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher,
    }

    @classmethod
    def create(cls, type_user):
        return cls.types[type_user]()


# порождающий паттерн прототип - курск
class CoursePrototype:

    def clone(self):
        return copy.deepcopy(self)


# класс Курс
class Course(CoursePrototype):
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)


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
    def create_user(type_user):
        return UserFactory.create(type_user)

    # создаем категории
    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    # поиск категорий
    def find_category_id(self, id):
        for category in self.categories:
            print('item', category.id)
            if category.id == id:
                return category
        raise Exception(f'Нет категории с id = {id}')

    # создаем курсы
    @staticmethod
    def create_course(type_course, name, category):
        return CourseFactory.create(type_course, name, category)

    def get_course(self, name):
        for course in self.courses:
            if course.name == name:
                return course
        return None

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


class Logger(metaclass=SingletonByName):
    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print('log =->', text)
