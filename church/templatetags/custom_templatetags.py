from django import template

register = template.Library()

@register.filter
def replace(value, arg):
  """
  Replacing filter
  Use `{{ "aaa"|replace:"a,b" }}`
  """
  if len(arg.split(',')) != 2:
      return value

  what, to = arg.split(',')
  return value.replace(what, to)
  
@register.filter
def str_pad0(value, arg):
  """
  Padding filter
  Use `{{ "aaa"|str_pad0:5 }}`
  """

  # if value is int:
  #   value = str(value)
    
  # if len(arg) != 1:
  #     return value
      
  value = value.zfill(arg)
  # value = value.rjust(arg, "0"))
  return value
  