# coding: UTF-8

from fabric.api import env, local
#import boto3

def put(directory_path):
  """
  put:file_path
  S3にファイルを保存する
  """
  #s3 = boto3.resource('s3')
  _set_s3_env()

  #for bucket in s3.buckets.all():
  #  print(bucket.name)

  #s3.Object(env.s3, file_path).put(Body=open(file_path, 'rb'))
  # とりあえずコマンド
  command = '/usr/bin/aws s3 sync ' + directory_path + ' s3://' + env.s3['bucket'] + ' --delete'
  local(command)

def _set_s3_env():
  env.s3 = {
    'bucket': ''
  }
