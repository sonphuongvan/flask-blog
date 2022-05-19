import os

if os.environ["app"] == "prod":
    from config.prod import ProdConfig as Config
else:
    from config.dev import DevConfig as Config
