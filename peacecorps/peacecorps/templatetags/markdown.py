from markdown import markdown
from django_jinja import library

@library.filter
def markdown(text):
    return markdown(text)