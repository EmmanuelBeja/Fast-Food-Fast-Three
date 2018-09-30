import os


class Config(object):
    """
    Common configurations
    """
    DEBUG = True


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DEBUG = True
    SECRET_KEY = "3d6e1695ba974064b7d6c2ef2ebc39e3"


class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = False
    TESTING = False
    SECRET_KEY = "3d6e1695ba974064b7d6c2ef2ebc39e3"

class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True

class TestingConfig(Config):
    """
    Testing configurations
    """
    TESTING = True
    SECRET_KEY = "3d6e1695ba974064b7d6c2ef2ebc39e3"
    DATABASE_URL="dbname=fastfoodfasttests user=emmanuelbeja password=#1Emmcodes host=localhost"
    DEBUG = True

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
