import os
from jinja2 import Template
from jinja2 import FileSystemLoader
from jinja2.environment import Environment


# рендер готовых страниц:
# def render(template_name, folder='templates',  **kwargs):
#     """
#     функция для отрисовки шаблона
#     :param template_name: имя html страницы для отрисовки.
#     :param kwargs: параметры для передачи в шаблон.
#     :param folder: если шаблон положен в папку templates, то оставить пустым.
#     """
#     template_path = os.path.join(folder, template_name)
#     # открываем шаблон по имени
#     with open(template_path, encoding='utf-8') as page:
#         # читаем содержимое
#         template = Template(page.read())
#     # рендерим шаблон с нужными параметрами
#     return template.render(**kwargs)


#  рендер шаблонов
def render_template(template_name, folder='templates', **kwargs):
    env = Environment()
    env.loader = FileSystemLoader(folder)
    template = env.get_template(template_name)
    return template.render(**kwargs)
