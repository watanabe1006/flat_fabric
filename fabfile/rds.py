# coding: UTF-8

from fabric.api import env, local, lcd
from fabric.decorators import task
import os
import datetime

def backup(db_name, user, backup_dir):
  """
  backup:db_name, user, backup_dir
  """
  with lcd(backup_dir):
    #local("pwd")
    # ファイル名はDB名 + 取得日
    d = datetime.datetime.today()
    file_name = db_name + "_" + d.strftime("%Y%m%d") + ".dump"

    # バックアップディレクトリ
    path = backup_dir + "/"  + d.strftime("%Y%m%d")
    if not os.path.isdir(path):
      #print(path + " is not exists")
      os.mkdir(path)

    # 最終的にはバックアップ用ユーザーを作る
    #command = "pg_dump -U " + env.rds["user"] + " -h " + env.rds["endpoint"] + " " + db_name + " > " + path + "/" + file_name
    command = "pg_dump -U " + user + " -h " + env.rds["endpoint"] + " " + db_name + " > " + path + "/" + file_name
    print(command)
    #local(command)

def _set_rds_env(data):
  """
  配列でもらったDBデータをenvにセットする
  """
  env.databases = []
  for db in data:
    #print db
    env.databases.append({
      "name": db[0],
      "password": db[1]
    })
  #print env.databases

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
