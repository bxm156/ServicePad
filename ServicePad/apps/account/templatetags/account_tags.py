from django import template

register = template.Library()

@register.inclusion_tag('account_sidebar.djhtml', takes_context=True)
def account_sidebar(context):
    user = context['user']
    if user.is_authenticated():
        return {'name':user.get_full_name(),'account_type':user.get_profile().account_type}

@register.filter
def at(value,index):
    return value[index][1]
