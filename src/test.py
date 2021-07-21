from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader

file_loader = FileSystemLoader('template')
env = Environment(loader=file_loader)

template = env.get_template("template.html")

print(template.render(imsrc='http:abc.com',img='abc',post_day='2',name='Planta Bonitas',wiki=None,synonyms='Planta, Bonita, and Plants',men='Alberto, Beto, and Roberto',year='1879',countries='Brazil South'))
