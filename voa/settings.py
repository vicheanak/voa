BOT_NAME = 'voa'

SPIDER_MODULES = ['voa.spiders']
NEWSPIDER_MODULE = 'voa.spiders'


ROBOTSTXT_OBEY = True
LOG_LEVEL = 'WARNING'

ITEM_PIPELINES = {
    'voa.pipelines.MySQLPipeline': 2
}
DOWNLOAD_DELAY = 2

DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWD = 'tU/x@168rY'
DB_DB = 'khmergoo_sequelize'