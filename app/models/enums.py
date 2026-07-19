from enum import Enum


class RequestStatus(str, Enum):
    NEW = "Новая"
    IN_PROGRESS = "В работе"
    DONE = "Выполнена"