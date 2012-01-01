from django import template

register = template.Library()

@register.inclusion_tag('account_sidebar.html')
def account_sidebar():
    return {'text':'SideBar'}
    
