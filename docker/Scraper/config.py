from configparser import ConfigParser
import os

def config():
    # create a parser
    #parser = ConfigParser()
    # read config file
    #parser.read(filename)

    # get section, default to postgresql
    #db = {}
    #if parser.has_section(section):
    #    params = parser.items(section)
    #    for param in params:
    #        db[param[0]] = param[1]
    #else:
    #    raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    #return db
    params = { 'host' : os.getenv('DB_HOST', 'localhost') , \
	       'port' : os.getenv('DB_PORT', '5432') , \
	       'database' : os.getenv('DB_NAME', 'postgres') , \
	       'user' : os.getenv('DB_USER', 'postgres') , \
	       'password' : os.getenv('DB_PASSWORD', 'somePassword') }
    return params

