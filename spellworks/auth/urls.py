from auth import auth
from views import Login, unconfirmed, Regist, Confirm


url = auth.add_url_rule

login_view = Login.as_view('login_index')
url('/login/', view_func=login_view)

url('/unconfirmed', view_func=unconfirmed)

regist_view = Regist.as_view('regist_view')
url('/regist/', view_func=regist_view)

confirm_view = Confirm.as_view('confirm_view')
url('/<confirm_type>/<token>/', view_func=confirm_view)
