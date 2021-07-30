import pathlib
abs_path = str(pathlib.Path().absolute())

PORT = 7000
DOCUMENT_ROOT = abs_path
# print(DOCUMENT_ROOT)

COOKIE_EXPIRE=4
TIMEOUT=20
#Maximum number of conncetions supported simulataneously
MAXCONNECTIONS = 1
#ErrorLog
ERROR_LOG = abs_path + '/logs/error_log'
#AccessLog
ACCESS_LOG = abs_path + '/logs/access_log'
