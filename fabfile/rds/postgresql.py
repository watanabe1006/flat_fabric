from fabric.decorators import task

@task
def backup():
  """RDS Backup"""
  print("RDS Backup")
