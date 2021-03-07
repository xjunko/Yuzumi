def args_join(args):
  return ' '.join([str(x) for x in args])

def Success(*args: list):
  return f'SUCCESS\n{args_join(args)}'

def Failed(*args: list):
  return f'FAILED\n{args_join(args)}'

