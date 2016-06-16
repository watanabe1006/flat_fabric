# coding: UTF-8

from fabric.api import *
import os
import zipfile

def _archive(file_path):
  """
  archive:file_path
  """
  file_name = file_path + ".zip"
  print(file_name)
  zip_file = zipfile.ZipFile(file_name, "w", zipfile.ZIP_DEFLATED)
  zip_file.write(file_path, os.path.basename(file_path))
  zip_file.close
  # 元ファイル削除
  os.remove(file_path)

def _get_remote_file(target_path, local_path):
  """
  _get_remote_file:target_path, local_path
  絶対パスで指定
  ローカルのディレクトリ確認は面倒なのでしない
  """
  get(target_path, local_path)
