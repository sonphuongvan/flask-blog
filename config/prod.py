class ProdConfig:
    SECRET_KEY = '80e6d3630da10e2216af26fb704de701'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:secret@172.20.0.2:3306/flask_blog' # mysql+pymysql://root:secret@mysql/flask_blog