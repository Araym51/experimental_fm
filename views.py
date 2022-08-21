from datetime import date

from framework.template_render import render_template
from patterns.creating_patterns import Engine, Logger

site = Engine()
logger = Logger('main')

# views
class IndexView:
    def __call__(self, request):
        return '200 OK', render_template('index.html', date=request.get('date'))


class AboutView:
    def __call__(self, request):
        return '200 OK', render_template('about.html')


class ContactView:
    def __call__(self, request):
        return '200 OK', render_template('contact_us.html')


class StudyProgramsView:
    def __call__(self, request):
        return '200 OK', render_template('study_programs.html', data = date.today()) #


class CoursesListView:
    def __call__(self, request):
        logger.log('Course list')
        try:
            category = site.find_category_id(int(request['request_params']['id']))
            return '200 OK', render_template('course_list.html',
                                             objects_list = category.courses, name = category.name, id = category.id)
        except KeyError:
            return '200 OK', 'Sorry, these course are no longer exists...'


class CreateCourse:
    category_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)
            category = None
            if self.category_id != -1:
                category = site.find_category_id(int(self.category_id))

                course = site.create_course('record', name, category)
                site.courses.append(course)
            return '200 OK', render_template('course_list.html', objects_list=category.courses,
                                             name=category.name, id=category.id)
        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_id(int(self.category_id))
                return '200 OK', render_template('create_course.html', name=category.name, id=category.id)
            except KeyError:
                return '200 OK', 'Sorry, these category are not exists...'


class CreateCategory:
    def __call__(self, request):
        if request['method'] == 'POST':
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
            return '200 OK', render_template('index.html', objects_list = site.categories)
        else:
            categories = site.categories
            return '200 OK', render_template('create_category.html', categories=categories) # todo create_category.html


# контроллер списка категорий
class CategoryList:
    def __call__(self, request):
        return '200 OK', render_template('category_list.html', objects_list = site.categories)


class CopyCourse:
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
            return '200 OK', render_template('course_list.html', objects_list = site.categories)
        except KeyError:
            return '200 OK', 'This course are not exists'

# пути в приложении:
routes = {
    '/': IndexView,
    '/about/': AboutView,
    '/contact_us/': ContactView,
    '/programs/': StudyProgramsView,
    '/courses/': CoursesListView,
    '/categories/': CategoryList
}
