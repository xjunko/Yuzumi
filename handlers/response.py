def Success(*args: list):
  reason = ' '.join([str(x) for x in args])
  return f'SUCCESS\n{reason}'

def Failed(*args: list):
  reason = ' '.join([str(x) for x in args])
  return f'FAILED\n{reason}'

