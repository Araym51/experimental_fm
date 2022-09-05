from datetime import date

from framework.template_render import render_template
from patterns.creating_patterns import Engine, Logger, MapperRegistry
from patterns.sructure_patterns import Routes, Debug
from patterns.behavior_patterns import TemplateView, CreateView, \
    BaseSerializer, ListView, EmailNotify, SmsNotify
from patterns.architectural_system_pattern import UnitOfWork


# получаем "движок" из порождающих паттернов
site = Engine()
# инициализация простого логгера
logger = Logger('main')
# оповещения:
email_notifier = EmailNotify()
sms_notify = SmsNotify()
# База данных:
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)
# пути приложения. С помощью декоратора @Routes все пути будут складываться сюда
routes = {}


# views
# главная страница
@Routes(routes=routes, url='/')
class IndexView(ListView):
    template_name = 'index.html'


# страница "О нас"
@Routes(routes=routes, url='/about/')
class AboutView(ListView):
    template_name = 'about.html'


# страница с контактами
@Routes(routes=routes, url='/contact_us/')
class ContactView(ListView):
    template_name = 'contact_us.html'


# страница с расписанием
@Routes(routes=routes, url='/programs/')
class StudyProgramsView(TemplateView):
    template_name = 'study_programs.html'

    def get_context_data(self):
        return {'objects_list': date.today()}


# страница с курсами
@Routes(routes=routes, url='/courses/')
class CoursesListView:
    @Debug(name='CoursesList')
    def __call__(self, request):
        logger.log('Course list')
        try:
            category = site.find_category_id(int(request['request_params']['id']))
            return '200 OK', render_template('course_list.html', objects_list=category.courses,
                                                              name=category.name, id=category.id)
        except KeyError:
            return '200 OK', render_template('404_cat_course.html')


# страница создания курса
@Routes(routes=routes, url='/create-course/')
class CreateCourse:
    category_id = -1

    @Debug(name='CreateCourse')
    def __call__(self, request):
        if request['method'] == 'POST':  # обработка POST запроса
            data = request['data']
            name = data['name']
            name = site.decode_value(name)
            category = None
            if self.category_id != -1:
                category = site.find_category_id(int(self.category_id))
                course = site.create_course('record', name, category)
                site.courses.append(course)
            return '200 OK', render_template('course_list.html',
                                             objects_list=category.courses, name=category.name, id=category.id)
        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_id(int(self.category_id))
                return '200 OK', render_template('create_course.html', name=category.name, id=category.id)
            except KeyError:
                return '200 OK', render_template('404_cat_course.html')


# контроллер списка категорий
@Routes(routes=routes, url='/categories/')
class CategoryList(ListView):
    template_name = 'category_list.html'

    def get_context_data(self):
        return {'objects_list': site.categories}
    # @Debug(name='CategoryList')
    # def __call__(self, request):
    #     return '200 OK', render_template('category_list.html', objects_list=site.categories)


# страница создания курса
@Routes(routes=routes, url='/create-category/')
class CreateCategory:
    @Debug(name='CreateCategory')
    def __call__(self, request):

        if request['method'] == 'POST':
            # метод пост
            print(request)
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_id(int(category_id))
            new_category = site.create_category(name, category)
            site.categories.append(new_category)
            return '200 OK', render_template('category_list.html', objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render_template('create_category.html', categories=categories)


# копирование курса
@Routes(routes=routes, url='/copy-course/') # todo проверить работоспособность
class CopyCourse:
    @Debug(name='CopyCourse')
    def __call__(self, request):
        request_params = request['request_params']
        try:
            name = request_params['name']
            old_course = site.get_course(name)
            if old_course:
                new_name = f'copy_{name}'
                new_course = old_course.clone()
                new_course.name = new_name
                site.courses.append(new_course)
            return '200 OK', render_template('course_list.html', objects_list=site.courses)
        except KeyError:
            return '200 OK', render_template('404_cat_course.html')


@Routes(routes=routes, url='/students-list/')
class StudentsListView(ListView):
    template_name = 'students_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('student')
        return mapper.all()


@Routes(routes=routes, url='/create-student/')
class StudentCreateView(CreateView):
    template_name = 'create_student.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_object = site.create_user('student', name)
        site.students.append(new_object)
        new_object.mark_new()
        UnitOfWork.get_current().commit()


@Routes(routes=routes, url='/add-student/')
class AddStudentByCourseCreateView(CreateView):
    template_name = 'add_student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = site.get_course(course_name)
        student_name = data['student_name']
        student_name = site.decode_value(student_name)
        student = site.get_student(student_name)
        course.add_student(student)


@Routes(routes=routes, url='/api/')
class CourseApi:
    @Debug(name='Api')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.courses).save()
