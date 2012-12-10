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

class RangeNode(template.Node):
    def __init__(self, num, context_name):
        self.num = template.Variable(num)
        self.context_name = context_name

    def render(self, context):
        context[self.context_name] = range(int(self.num.resolve(context)))
        return ""
@register.tag
def num_range(parser, token):
    """
    Takes a number and iterates and returns a range (list) that can be 
    iterated through in templates
    
    Syntax:
    {% num_range 5 as some_range %}
    
    {% for i in some_range %}
      {{ i }}: Something I want to repeat\n
    {% endfor %}
    
    Produces:
    0: Something I want to repeat 
    1: Something I want to repeat 
    2: Something I want to repeat 
    3: Something I want to repeat 
    4: Something I want to repeat
    """
    try:
        fnctn, num, trash, context_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%s takes the syntax %s number_to_iterate\
            as context_variable" % (fnctn, fnctn)
    if not trash == 'as':
        raise template.TemplateSyntaxError, "%s takes the syntax %s number_to_iterate\
            as context_variable" % (fnctn, fnctn)
    return RangeNode(num, context_name)
