from django import template

register = template.Library ()

@register.filter
def index ( l, i ):
    return l [ int ( i ) ]

@register.filter
def add ( x, y ):
    return int ( x ) + int ( y )

@register.filter
def iseven ( x ):
    return ((int ( x ) & 1) == 0)