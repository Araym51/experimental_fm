import jsonpickle
from framework.template_render import render_template


# базовый класс наблюдатель
class Observer:
    def update(self, subject):
        pass


# класс - объект наблюдения
class Subject:
    def __init__(self):
        self.observers = []

    def notify(self):
        for observer in self.observers:
            observer.update(self)


# дочерний класс наблюдателя, служит для оповещения по СМС при добалении нового пользователя
class SmsNotify(Observer):
    def update(self, subject):
        print('Sending SMS =->', f'{subject.students[-1].name} присоедился к нам')


# дочерний класс наблюдателя, служит для оповещения по email при добалении нового пользователя
class EmailNotify(Observer):
    def update(self, subject):
        print('Sending EMAIL =->', f'{subject.students[-1].name} присоедился к нам')


# базовый сериализатор для API
class BaseSerializer:
    def __init__(self, object):
        self.object = object

    def save(self):
        return jsonpickle.dumps(self.object)

    @staticmethod
    def load(data):
        return jsonpickle.loads(data)



class TemplateView:
    # шаблон отображаемой страницы:
    template_name = 'template.html'
    error_template = 'template.html'

    def get_context_data(self):
        """необходимо переопределить если есть контекстная информация"""
        return {}

    def get_template(self):
        """возвращает назначенный шаблон"""
        return self.template_name

    def render_template_with_context(self):
        """рендер шаблона с контекстной информацией"""
        template_name = self.get_template()
        context = self.get_context_data()
        return '200 OK', render_template(template_name, **context)

    def error_render(self, error_template):
        return '200 OK', render_template(self.template_name)

    def __call__(self, request):
        try:
            return self.render_template_with_context()
        except KeyError:
            return self.error_render(self.error_template)


class ListView(TemplateView):
    # здесь хранятся данные из нашего движка (creating_patterns.Engine)
    query_set = []
    # шаблон страницы
    template_name = 'template.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        """данные получаемые из creating_patterns.Engine.
        Необходимо переопределить и явно указать какие данные используем"""
        print(self.query_set)
        return self.query_set

    def get_context_object_name(self):
        """ключ словаря по которому будем искать query_set"""
        return self.context_object_name

    def get_context_data(self):
        """возвращает словарь имя_контекста: набор данных"""
        query_set = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: query_set}
        return context


class CreateView(TemplateView):
    template_name = 'create.html'

    @staticmethod
    def get_request_data(request):
        return request['data']

    def create_obj(self, data):
        """метод для создания объектов. Необходимо переопределить в view"""
        pass

    def __call__(self, request):
        if request['method'] == 'POST':
            data = self.get_request_data(request)
            self.create_obj(data)
            return self.render_template_with_context()
        else:
            return super().__call__(request)


class ConsoleWriter:
    def write(self, text):
        print(text)


class FileWriter:
    def __init__(self, file_name):
        self.file_name = file_name

    def write(self, text):
        with open(self.file_name, 'a', encoding='utf-8') as file:
            file.write(f'{text}\n')
