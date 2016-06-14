# coding: UTF-8

from fabric.api import env
from fabric.decorators import task
import rds

@task
def backup(db_name, user, password, backup_dir='/backup'):
  """
  backup:db_name, user, password, backup_dir
  """
  _set_env()
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
  _db_list()
  for db in env.databases:
    #print db
    backup(db["name"], db["name"], db["password"], backup_dir=backup_dir)


def _db_list(list_file='../lists/db_list'):
  """
  DBリストを読み込む
  パスは適当
  """
  d_list = list_file
  items = []
  for line in open(d_list, 'r'):
    item = line[:-1].split(',')
    #print item
    items.append(item)
  #print items
  rds._set_rds_env(items)


def _set_env():
  env.rds = {
    "endpoint": "",
    "user": "",
    "password": "",
    "port": ""
  }
