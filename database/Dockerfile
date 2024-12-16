FROM mysql:8.0

# 環境變數
ENV MYSQL_ROOT_PASSWORD=password
ENV MYSQL_DATABASE=SOGO

# 設置 MySQL 默認字元集為 utf8mb4
RUN echo "[mysqld]" >> /etc/mysql/conf.d/custom.cnf && \
    echo "character-set-server=utf8mb4" >> /etc/mysql/conf.d/custom.cnf && \
    echo "collation-server=utf8mb4_general_ci" >> /etc/mysql/conf.d/custom.cnf && \
    echo "[client]" >> /etc/mysql/conf.d/custom.cnf && \
    echo "default-character-set=utf8mb4" >> /etc/mysql/conf.d/custom.cnf && \
    echo "[mysql]" >> /etc/mysql/conf.d/custom.cnf && \
    echo "default-character-set=utf8mb4" >> /etc/mysql/conf.d/custom.cnf

# 初始化數據庫的 SQL 文件
COPY init.sql /docker-entrypoint-initdb.d/
