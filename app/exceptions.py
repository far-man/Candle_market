from fastapi import HTTPException, status


# Создание собственных исключений (exceptions) было изменено
# на предпочтительный подход.
# Подробнее в курсе: https://stepik.org/lesson/919993/step/15?unit=925776

class BasketException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class BasketGetException(BasketException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Basket отсутствует"


class UserAlreadyExistsException(BasketException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class IncorrectEmailOrPasswordException(BasketException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"


class TokenExpiredException(BasketException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Срок действия токена истек"


class TokenAbsentException(BasketException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class IncorrectTokenFormatException(BasketException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserIsNotPresentException(BasketException):
    status_code = status.HTTP_401_UNAUTHORIZED


class CandleFullyBooked(BasketException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Нет в наличии"


class CandleCannotBeBooked(BasketException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось купить свечу ввиду неизвестной ошибки"


class DateFromCannotBeAfterDateTo(BasketException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Дата заезда не может быть позже даты выезда"


class CannotBookHotelForLongPeriod(BasketException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Невозможно забронировать отель сроком более месяца"


class CannotAddDataToDatabase(BasketException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось добавить запись"


class CannotProcessCSV(BasketException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось обработать CSV файл"