from auth import auth
from views import LoginIndex


url = auth.add_url_rule

login_view = LoginIndex.as_view('login_index')
url('/', view_func=login_view)
