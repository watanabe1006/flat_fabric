# coding: UTF-8

from fabric.api import *
from fabric.decorators import *
from fabric.contrib import files
import datetime
import environment
import rds
import s3

environment._set_hosts()
rds._db_list()
environment._set_s3_env()

@task
def db_backup(db_name, user, password, backup_dir='/backup'):
  """
  db_backup:db_name, user, password, backup_dir
  """
  environment._set_rds_env()
  # DBごとのユーザー/パスワードでバックアップ
  rds._set_pgpass(env.rds["endpoint"], env.rds["port"], db_name, user, password)
  # バックアップユーザーを使ったバックアップ
  #rds._set_pgpass(env.rds["endpoint"], env.rds["port"], db_name, env.rds["user"], env.rds["password"])
  rds.backup(db_name, user, backup_dir=backup_dir)

@task
def db_backup_all(backup_dir='/backup'):
  """
  rds all backup
  """
  # DBバックアップ
  for db in env.databases:
    #print db
    db_backup(db["name"], db["name"], db["password"], backup_dir=backup_dir)
  # S3に転送
  s3.put(env.s3['db'], backup_dir)

@task
@roles('webserver')
def file_backup(target_path='/glusterfs/', backup_path='/file_backup'):
  """
  file_backup:target_path, backup_path
  """
  for db in env.databases:
    db_dir = target_path + db['name']
    if files.exists(db_dir):
      #print db
      _file_archive(db_dir, backup_path, db['name'], db['backup'])
      db['backup'] = True
  # S3転送
  # 各DBごとのファイル取得チェックは後で
  _file_put(backup_path)

@runs_once
def _file_put(backup_path):
  s3.put(env.s3['file'], backup_path)

def _file_archive(target_path, backup_path, db_name, flg):
  """
  リモートファイルを持ってきて圧縮
  """
  backup_file_path = backup_path + '/' + db_name
  archive_dir = ['data', 'logs']
  if not flg:
    with hide('running', 'warnings'):
      common._get_remote_file(target_path, backup_file_path)
    date = datetime.datetime.today()
    with lcd(backup_file_path):
      with hide('running', 'warnings', 'stdout'):
        local('tar -cvzf ' + db_name + '_' + date.strftime('%Y%m%d') + '.tar.gz ' + db_name)
        local('rm -fr ' + db_name)

