# coding: UTF-8

from fabric.api import env

def _set_rds_env():
  """
  RDS環境設定
  """
  env.rds = {
    'endpoint': '',
    'user': '',
    'password': '',
    'port': ''
  }

def _set_s3_env():
  env.s3 = {
    'db': '',
    'file': ''
  }

def _set_hosts():
  env.use_ssh_config = True
  env.user = ''
  env.roledefs.update({
    'webserver': [
      'web01', 'web02'
    ]
  })
