# coding: UTF-8

from fabric.api import env, local, lcd
from fabric.decorators import task
import os
import datetime
from . import common
from . import environment

def backup(db_name, user, backup_dir):
  """
  backup:db_name, user, backup_dir
  """
  with lcd(backup_dir):
    # ファイル名はDB名 + 取得日
    d = datetime.datetime.today()
    file_name = db_name + "_" + d.strftime("%Y%m%d") + ".dump"

    # バックアップディレクトリ
    path = backup_dir + "/"  + db_name
    if not os.path.isdir(path):
      #print(path + " is not exists")
      os.makedirs(path)
    file_path = path + "/" + file_name
    # 最終的にはバックアップ用ユーザーを作る
    #command = "pg_dump -U " + env.rds["user"] + " -h " + env.rds["endpoint"] + " " + db_name + " > " + path + "/" + file_name
    command = "pg_dump -U " + user + " -h " + env.rds["endpoint"] + " " + db_name + " > " + file_path
    #print(command)
    local(command)

    # 圧縮
    common._archive(file_path)

def _db_list(list_file='../lists/db_list'):
  """
  DBリストを読み込んでenvに設定
  パスは適当
  """
  d_list = list_file
  # リストからDB情報を取得
  items = []
  for line in open(d_list, 'r'):
    item = line[:-1].split(',')
    items.append(item)
  # DBデータをenvにセットする
  env.databases = []
  for db in items:
    env.databases.append({
      "name": db[0],
      "password": db[1],
      "backup": False
    })

def _set_pgpass(endpoint, port, db_name, user, password):
  """
  .pgpass作成
  そのうち削除も作る
  """
  path = os.getenv("HOME") + "/.pgpass"
  f = open(path, "w")
  value = endpoint + ":" + port + ":" + db_name + ":" + user + ":" + password
  f.write(value)
  f.close

  # 権限変更
  os.chmod(path, 0600)
