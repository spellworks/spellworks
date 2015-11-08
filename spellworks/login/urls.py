from . import login
from views import LoginIndex


url = login.add_url_rule

login_view = LoginIndex.as_view('login_index')
url('/', view_func=login_view)
