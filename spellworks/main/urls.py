from . import main
from views import Index


url = main.add_url_rule

main_view = Index.as_view('index')
url('/', view_func=main_view)
