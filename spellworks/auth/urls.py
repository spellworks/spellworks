from auth import auth
from views import Login, unconfirmed, Regist, Confirm, log_out


url = auth.add_url_rule

login_view = Login.as_view('login')
confirm_view = Confirm.as_view('confirm')
regist_view = Regist.as_view('regist')


url('/login/', view_func=login_view)
url('/unconfirmed/', view_func=unconfirmed)
url('/regist/', view_func=regist_view)
url('/<confirm_type>/<token>/', view_func=confirm_view)
url('/logout/', view_func=log_out)
