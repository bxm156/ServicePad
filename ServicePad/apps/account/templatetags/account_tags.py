from django import template

register = template.Library()

@register.inclusion_tag('account_sidebar.html', takes_context=True)
def account_sidebar(context):
    user = context['user']
    if user.is_authenticated():
        text = "Hello %s %s" % (user.first_name,user.last_name)
    return {'text':text}
    
