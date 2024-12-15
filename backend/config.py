class Config:
    """Base configuration."""
    SECRET_KEY = "your_secret_key"  # 替換為實際密鑰
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:password@database/SOGO"  # 替換為您的數據庫連接字串


# 配置映射
config = {
    "development": DevelopmentConfig,
    "default": DevelopmentConfig,
}
