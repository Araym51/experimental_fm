class RequestParse:
    @staticmethod
    def parse_input_data(data: str):
        """
        функция парсит входящие запросы от пользователей
        :param data: принимает строку с запросом
        :return: возвращает словарь для дальнейшей работы с данными
        """
        result = {}
        if data:
            # убираем &
            parametrs = data.split('&')
            for items in parametrs:
                key, value = items.split('=')  # получаем ключ, значение для словаря
                result[key] = value
        return result


class GetRequest(RequestParse):
    @staticmethod
    def get_req_params(environ):
        # получаем данные из environ query string
        query_string = environ['QUERY_STRING']
        # с помощью парсера разбираем строку и получаем словарь
        req_parametrs = GetRequest.parse_input_data(query_string)
        return req_parametrs


class PostRequest(RequestParse):
    @staticmethod
    def get_wsgi_input_data(env) -> bytes:
        # пролучаем длинну тела
        content_lenght_data = env.get('CONTENT_LENGTH')
        # приводим длинну тела к int
        content_lenght = int(content_lenght_data) if content_lenght_data else 0
        # считываем данные если есть. Если нет возвращаем пустую байтовую строку
        data = env['wsgi.input'].read(content_lenght) if content_lenght > 0 else b''
        print(data)
        return data

    def parse_wsgi_input_data(data: bytes) -> dict:
        result = {}
        if data:
            # декодируем данные
            data_str = data.decode(encoding='utf-8')
            print(data_str)
            result = PostRequest.parse_input_data(data_str)
        return result

    def request_params(self, environ):
        # получаем данные из environ
        data = self.get_wsgi_input_data(environ)
        # превращаем данные в словарь
        data = self.parse_input_data(data)
        return data
