#Базовый класс всех эндпоинтов
class Endpoint:
    BASE_URL = "https://secby.ru"
    
    response = None
    response_json = None

    def check_response_is_200(self):
        assert self.response.status_code == 200

    def check_response_is_201(self):
        assert self.response.status_code == 201

    #bad request
    def check_response_is_400(self):
        assert self.response.status_code == 400

    #invalid data
    def check_response_is_401(self):
        assert self.response.status_code == 401

    #permission denied
    def check_response_is_403(self):
        assert self.response.status_code == 403
    
    #not found
    def check_response_is_404(self):
        assert self.response.status_code == 404

    #missing fields
    def check_response_is_422(self):
        assert self.response.status_code == 422

    #internal server error
    def check_response_is_500(self):
        assert self.response.status_code == 500

    #валидация текста простых ошибок (400, 401, 403, 404, 500)
    def check_error_detail_contains(self, expected_text):
        detail = self.response_json.get('detail')
        assert expected_text.lower() in detail.lower(), f'Не нашли {expected_text} в ответе: {self.response_json}'
    
    #проверка текста ошибки валидации (422)
    #создали отдельную функцию, т.к. в ошибке 422 может быть несколько полей пропущено
    def check_validation_error(self, field_name):
        details = self.response_json.get('detail')
        assert isinstance(details, list), f'Ожидался список ошибок в detail, получен {type(details)}: {details}'
        
        #находим ВСЕ пропущенные поля, если не нашли поднимаем ошибку 
        for error in details:
            if (error.get('type') == 'missing' and field_name in error.get('loc')):
                return
        
        raise AssertionError(
            f'Не найдена ошибка валидации типа missing для поля {field_name}.\n'
            f'Получен ответ: {self.response_json}'
        )