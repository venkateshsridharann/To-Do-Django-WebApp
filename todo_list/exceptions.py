from rest_framework.exceptions import APIException


class ItemIntegrityException(APIException):
    status_code = 400
    default_detail = 'User already has list with given specified name.'
    default_code = 'BAD REQUEST'


class ListDoesNotExistException(APIException):
    status_code = 400
    default_detail = 'User has no list with specified ID.'
    default_code = 'BAD REQUEST'


class ItemDoesNotExistException(APIException):
    status_code = 400
    default_detail = 'User has no item with specified ID.'
    default_code = 'BAD REQUEST'