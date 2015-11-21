from auth import auth
from views import LoginIndex, unconfirmed


url = auth.add_url_rule

login_view = LoginIndex.as_view('login_index')
url('/', view_func=login_view)

url('/unconfirmed', view_func=unconfirmed)
