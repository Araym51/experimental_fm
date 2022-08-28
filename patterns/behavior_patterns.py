import jsonpickle
from framework.template_render import render_template


class Observer:
    def update(self, subject):
        pass


class Subject:
    def __init__(self):
        self.observers = []

    def notify(self):
        for observer in self.observers:
            observer.update(self)


class SmsNotify(Observer):
    def update(self, subject):
        print('Sending SMS =->', f'{subject.students[-1].name} присоедился к нам')


class EmailNotify(Observer):
    def update(self, subject):
        print('Sending EMAIL =->', f'{subject.students[-1].name} присоедился к нам')


class BaseSerializer:
    def __init__(self, object):
        self.object = object

    def save(self):
        return jsonpickle.dumps(self.object)

    @staticmethod
    def load(data):
        return jsonpickle.loads(data)


class TemplateView:
    template_name = 'template.html'

    def get_context_data(self):
        return {}

    def get_template(self):
        return self.template_name

    def render_template_with_context(self):
        template_name = self.get_template()
        context = self.get_context_data()
        return '200 OK', render_template(template_name, **context)

    def __call__(self, request):
        return self.render_template_with_context()


class ListView(TemplateView):
    query_set = []
    template_name = 'template.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        print(self.query_set)
        return self.query_set

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self):
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
