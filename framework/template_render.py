import os
from jinja2 import Template


def render(template_name, folder='templates',  **kwargs):
    """
    функция для отрисовки шаблона
    :param template_name: имя html страницы для отрисовки.
    :param kwargs: параметры для передачи в шаблон.
    :param folder: если шаблон положен в папку templates, то оставить пустым.
    """
    template_path = os.path.join(folder, template_name)
    # открываем шаблон по имени
    with open(template_path, **kwargs) as page:
        # читаем содержимое
        template = Template(page.read())
    # рендерим шаблон с нужными параметрами
    return template.render(**kwargs)
