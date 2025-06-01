from django import template

register = template.Library()

@register.filter
def star_class(average_review, star_index):
    """
    Returns the appropriate star class suffix for the given star index (1 to 5)
    based on the average_review value.
    """
    try:
        average_review = float(average_review)
        star_index = int(star_index)
    except (ValueError, TypeError):
        return ''
    if average_review < (star_index - 0.5):
        return '-o'
    elif average_review >= (star_index - 0.5) and average_review < star_index:
        return '-half-o'
    else:
        return ''
