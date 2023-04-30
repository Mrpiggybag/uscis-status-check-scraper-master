##!/usr/local/bin/python

from sys import exit, stderr

def log_error(msg: str) -> None:
  """
  Logs message to stderr
  """
  print(msg, file=stderr)

def construct_app_num(num: int) -> str:
  """
  Returns the application receipt number string for the given application
  number (Integer).
  """
  return '{num}'

