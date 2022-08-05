from jinja2 import Template


def render(template_name, **kwargs):
    """
    функция для отрисовки шаблона
    :param template_name: имя html страницы для отрисовки
    :param kwargs: параметры для передачи в шаблон
    :return:
    """
    # открываем шаблон по имени
    with open(template_name, **kwargs) as page:
        # читаем содержимое
        template = Template(page.read())
    # рендерим шаблон с нужными параметрами
    return template.render(**kwargs)
