# coding: UTF-8

from fabric.api import env
from fabric.decorators import task
import rds
import s3

@task
def backup(db_name, user, password, backup_dir='/backup'):
  """
  backup:db_name, user, password, backup_dir
  """
  rds._set_rds_env()
  # DBごとのユーザー/パスワードでバックアップ
  rds._set_pgpass(env.rds["endpoint"], env.rds["port"], db_name, user, password)
  # バックアップユーザーを使ったバックアップ
  #rds._set_pgpass(env.rds["endpoint"], env.rds["port"], db_name, env.rds["user"], env.rds["password"])
  rds.backup(db_name, user, backup_dir=backup_dir)

@task
def backup_all(backup_dir='/backup'):
  """
  rds all backup
  """
  rds._db_list()
  # DBバックアップ
  for db in env.databases:
    #print db
    backup(db["name"], db["name"], db["password"], backup_dir=backup_dir)
  # S3に転送
  s3.put(backup_dir)
