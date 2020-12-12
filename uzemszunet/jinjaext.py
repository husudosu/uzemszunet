from jinja2 import Environment, PackageLoader, select_autoescape

# Jinja 2 config
jinja_env = Environment(
    loader=PackageLoader('uzemszunet', 'templates'),
    autoescape=select_autoescape(['html', 'xml', 'jinja'])
)
