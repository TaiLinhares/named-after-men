from jinja2 import Environment, PackageLoader, FileSystemLoader

file_loader = FileSystemLoader("template")
env = Environment(loader=file_loader)

template = env.get_template("template.html")

print(
    template.render(
        imgsrc="http:abc.com",
        img="abc",
        post_day="2",
        name="Planta Bonitas",
        wiki=None,
        synonyms="",
        men="Alberto",
        year="1879",
        countries="Brazil South",
    )
)
