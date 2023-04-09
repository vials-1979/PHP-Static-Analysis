class SourceRule:
    def __init__(self):
        self.other_input_sources={
            'get_headers': {'description': 'Fetches all the headers sent by the server in response to an HTTP request'},
            'getallheaders': {'description': 'Fetch all HTTP request headers'},
            'get_browser': {'description': 'Tells what the user\'s browser is capable of'},
            'getenv': {'description': 'Gets the value of an environment variable'},
            'gethostbyaddr': {'description': 'Get the Internet host name corresponding to a given IP address'},
            'runkit_superglobals': {'description': 'Return numerically indexed list of registered superglobals'},
            'import_request_variables': {'description': 'Import GET/POST/Cookie variables into the global scope'}
        }

        self.database_input_sources = {
            'mysql_fetch_array': {'description': 'Fetch a result row as an associative array, a numeric array, or both'},
            'mysql_fetch_assoc': {'description': 'Fetch a result row as an associative array'},
            'mysql_fetch_field': {'description': 'Get column information from a result and return as an object'},
            'mysql_fetch_object': {'description': 'Fetch a result row as an object'},
            'mysql_fetch_row': {'description': 'Get a result row as an enumerated array'},
            'pg_fetch_all': {'description': 'Fetch all rows in a PostgreSQL result as an array'},
            'pg_fetch_array': {'description': 'Fetch a row as an array'},
            'pg_fetch_assoc': {'description': 'Fetch a row as an associative array'},
            'pg_fetch_object': {'description': 'Fetch a row as an object'},
            'pg_fetch_result': {'description': 'Returns values from a result resource'},
            'pg_fetch_row': {'description': 'Get a row as an enumerated array'},
            'sqlite_fetch_all': {'description': 'Fetch all the rows of a result set'},
            'sqlite_fetch_array': {'description': 'Fetch the next row from a result set as an array'},
            'sqlite_fetch_object': {'description': 'Fetch the next row from a result set as an object'},
            'sqlite_fetch_single': {'description': 'Fetch the first column of a result set as a string'},
            'sqlite_fetch_string': {'description': 'Alias of sqlite_fetch_single'}
        }
        
        self.file_input_sources = {
            'bzread': {'description': 'Reads data from a bzip2 file'},
            'dio_read': {'description': 'Reads data from a file descriptor'},
            'exif_imagetype': {'description': 'Determine the type of an image'},
            'exif_read_data': {'description': 'Reads the EXIF data from an image file'},
            'exif_thumbnail': {'description': 'Retrieve the embedded thumbnail of an image'},
            'fgets': {'description': 'Reads a line from a file pointer'},
            'fgetss': {'description': 'Reads a line from a file pointer and strips HTML tags'},
            'file': {'description': 'Reads entire file into an array'},
            'file_get_contents': {'description': 'Reads entire file into a string'},
            'fread': {'description': 'Reads data from a file pointer'},
            'get_meta_tags': {'description': 'Extracts all meta tag content attributes from a file'},
            'glob': {'description': 'Find pathnames matching a pattern'},
            'gzread': {'description': 'Reads data from a gz-file'},
            'readdir': {'description': 'Reads entry from a directory handle'},
            'read_exif_data': {'description': 'Alias of exif_read_data'},
            'scandir': {'description': 'List files and directories inside the specified path'},
            'zip_read': {'description': 'Reads the next file in a ZIP archive'}
        }
        
        self.global_variables = {
            "$_GET": {"description": "User-provided input via GET method"},
            "$_POST": {"description": "User-provided input via POST method"},
            "$_COOKIE": {"description": "User-provided input via COOKIE"},
            "$_REQUEST": {"description": "User-provided input via GET, POST or COOKIE"},
            "$_FILES": {"description": "User-provided input via file uploads"},
            "$_SERVER": {"description": "Server and execution environment information"},
            "$HTTP_GET_VARS": {"description": "User-provided input via GET method (older version)"},
            "$HTTP_POST_VARS": {"description": "User-provided input via POST method (older version)"},
            "$HTTP_COOKIE_VARS": {"description": "User-provided input via COOKIE (older version)"},
            "$HTTP_REQUEST_VARS": {"description": "User-provided input via GET, POST or COOKIE (older version)"},
            "$HTTP_POST_FILES": {"description": "User-provided input via file uploads (older version)"},
            "$HTTP_SERVER_VARS": {"description": "Server and execution environment information (older version)"},
            "$HTTP_RAW_POST_DATA": {"description": "Raw POST data"},
            "$argc": {"description": "Number of arguments passed to the script"},
            "$argv": {"description": "Array of arguments passed to the script"},
        }
        
        self.server_variables = {
            "HTTP_ACCEPT": {"description": "Content types that are acceptable by the user agent"},
            "HTTP_ACCEPT_LANGUAGE": {"description": "Natural languages that are acceptable by the user agent"},
            "HTTP_ACCEPT_ENCODING": {"description": "Content encodings that are acceptable by the user agent"},
            "HTTP_ACCEPT_CHARSET": {"description": "Character sets that are acceptable by the user agent"},
            "HTTP_CONNECTION": {"description": "Options that are desired for the connection"},
            "HTTP_HOST": {"description": "Host and port information"},
            "HTTP_KEEP_ALIVE": {"description": "Connection keep-alive information"},
            "HTTP_REFERER": {"description": "Address of the page that linked to the requested resource"},
            "HTTP_USER_AGENT": {"description": "User agent string of the user agent"},
            "HTTP_X_FORWARDED_FOR": {"description": "Client IP address when connected through a proxy"},
            "PHP_AUTH_DIGEST": {"description": "Digest string for HTTP Digest Authentication"},
            "PHP_AUTH_USER": {"description": "Username for HTTP authentication"},
            "PHP_AUTH_PW": {"description": "Password for HTTP authentication"},
            "AUTH_TYPE": {"description": "Type of authentication used"},
            "QUERY_STRING": {"description": "Query string that was passed to the script"},
            "REQUEST_METHOD": {"description": "HTTP request method used"},
            "REQUEST_URI": {"description": "URI requested by the user agent"},
            "PATH_INFO": {"description": "Path information"},
            "ORIG_PATH_INFO": {"description": "Original path information before processing by PHP"},
            "PATH_TRANSLATED": {"description": "Filesystem path for the requested document"},
            "REMOTE_HOSTNAME": {"description": "Hostname of the user agent"},
            "PHP_SELF": {"description": "Path of the current executing script"},
        }

    def is_tainted_source(self, tac_instruction):
        # 检查全局变量输入源
        if tac_instruction.op=="LOAD_ARRAY_OFFSET":
            if tac_instruction.left_operand in self.global_variables or \
               tac_instruction.left_operand  in self.server_variables or \
               tac_instruction.left_operand  in self.file_input_sources or \
               tac_instruction.left_operand  in self.data_input_sources or \
               tac_instruction.left_operand  in self.other_input_sources:
                return True

        return False
