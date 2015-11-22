from auth import auth
from views import Login, unconfirmed


url = auth.add_url_rule

login_view = Login.as_view('login_index')
url('/', view_func=login_view)

url('/unconfirmed', view_func=unconfirmed)
