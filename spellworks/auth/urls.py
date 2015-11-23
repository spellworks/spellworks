from auth import auth
from views import Login, unconfirmed, Regist


url = auth.add_url_rule

login_view = Login.as_view('login_index')
url('/login/', view_func=login_view)

url('/unconfirmed', view_func=unconfirmed)

regist_view = Regist.as_view('regist_view')
url('/regist/', view_func=regist_view)
