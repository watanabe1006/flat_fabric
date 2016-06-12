# coding: UTF-8

from fabric.api import local, lcd
from fabric.decorators import task
import datetime

@task
def backup(db_name, backup_dir="/backup"):
  """
  backup:db_name=DB_NAME,backup_dir=BACKUP_DIR
  """
  with lcd(backup_dir):
    local("pwd")
    _rds_env()
    # ファイル名はDB名 + 取得日
    d = datetime.datetime.today()
    file_name = db_name + d.strftime("%Y_%m_%d") + ".dump"
    command = "pg_dump -U " + rds_user + " -h " + rds_host + " " + db_name + " > " + backup_dir + "/" + file_name
    print(command)

def _rds_env():
    global rds_host
    global rds_user

    rds_host = "rds_host"
    rds_user = "aipo001"
