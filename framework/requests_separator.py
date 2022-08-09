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
    pass
