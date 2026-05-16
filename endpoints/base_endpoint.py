#Базовый класс всех эндпоинтов
class Endpoint:
    BASE_URL = "https://secby.ru"
    
    response = None
    response_json = None

    #удачный запрос
    def check_response_is_200(self):
        assert self.response.status_code == 200

    #удачный запрос
    def check_response_is_201(self):
        assert self.response.status_code == 201

    #
    def check_response_is_400(self):
        assert self.response.status_code == 400

    #"Incorrect username or password"
    def check_response_is_401(self):
        assert self.response.status_code == 401

    #"Permission denied"
    def check_response_is_403(self):
        assert self.response.status_code == 403
    
    #"Profile not found"
    def check_response_is_404(self):
        assert self.response.status_code == 404

    #ошибка валидации
    def check_response_is_422(self):
        assert self.response.status_code == 422

    def check_response_is_500(self):
        assert self.response.status_code == 500