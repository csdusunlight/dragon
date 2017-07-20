from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', 'account.views.account', name='account_index'),
    url(r'^get_nums$', 'account.views.get_nums', name='get_nums'),
    url(r'^welfare/$', 'account.views.welfare', name='account_welfare'),
    url(r'^welpage/$', 'account.views.get_user_wel_page', name='get_user_wel_page'),
    url(r'^channelwelpage/$', 'account.views.get_channel_result_page', name='get_channel_result_page'),
    url(r'^score/$', 'account.views.score', name='account_score'),
    url(r'^scorepage/$', 'account.views.get_user_score_page', name='get_user_score_page'),
    url(r'^money/$', 'account.views.money', name='account_money'),
    url(r'^moneypage/$', 'account.views.get_user_money_page', name='get_user_money_page'),
#     url(r'money/$', 'account.views.money', name='account_money'),
#     url(r'user/$', 'account.views.user', name='account_user'),
    url(r'^coupon/$', 'account.views.coupon', name='account_coupon'),
    url(r'^couponpage/$', 'account.views.get_user_coupon_page', name='get_user_coupon_page'),
    url(r'^coupondetail/$', 'account.views.get_user_coupon_exchange_detail', name='get_user_coupon_exchange_detail'),
    url(r'^useCoupon/$', 'account.views.useCoupon', name='useCoupon'),
    url(r'security/$', 'account.views.security', name='account_security'),
    url(r'^bankcard/$', 'account.views.bankcard', name='account_bankcard'),
    url(r'^withdraw/$', 'account.views.withdraw', name='account_withdraw'),
    url(r'^invite/$', 'account.views.invite', name='account_invite'),
    url(r'^invitepage/$', 'account.views.get_user_invite_page', name='get_user_invite_page'),
    url(r'^message/$', 'account.views.message', name='account_message'),
    url(r'^messagepage/$', 'account.views.get_user_message_page', name='get_user_message_page'),
    url(r'^register/$', 'account.views.register', name='register'),
    url(r'^login/$', 'account.views.login', {'template_name': 'registration/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'registration/logged_out.html', 'next_page':'login'}, name='logout'),
    url(r'signin/$', 'account.views.signin', name='signin'),
    url(r'^password_change/$', 'account.views.password_change', name='password_change'),
    url(r'^change_pay_password/$', 'account.views.change_pay_password', name='change_pay_password'),
    url(r'^active_email/$', 'account.views.active_email', name='active_email'),
    url(r'^bind_bankcard/$', 'account.views.bind_bankcard', name='bind_bankcard'),
    url(r'^password_change/done/$', auth_views.password_change_done, name='password_change_done'),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^verifyemail/$', 'account.views.verifyemail', name='verifyemail'),
    url(r'^verifymobile/$', 'account.views.verifymobile', name='verifymobile'),
    url(r'^verifyusername/$', 'account.views.verifyusername', name='verifyusername'),
    url(r'^verifyinviter/$', 'account.views.verifyinviter', name='verifyinviter'),
    url(r'^phoneImageV/$', 'account.views.phoneImageV', name='phoneImageV'),
#    url(r'verifytelcode/$', 'account.views.verifytelcode', name='verifytelcode'),
    url(r'^callback/$', 'account.views.callbackby189', name='callback'),

    url(r'^resetpw/$', 'account.forgot_passwd.forgot_passwd', name='forgot_passwd'),
    url(r'^forgot_validate_randcode/$', 'account.forgot_passwd.validate_randcode', name='forgot-validate-randcode'),
    url(r'^forgot_validate_telcode/$', 'account.forgot_passwd.validate_telcode', name='forgot-validate-telcode'),

    url(r'^channel/$', 'account.channel.channel', name='account_channel'),
    url(r'^export/$', 'account.channel.export_audit_result', name='export_audit_result'),

    url(r'^submit_itembyitem/$', 'account.channel.submit_itembyitem', name='submit_itembyitem'),
    url(r'^revise_project/$', 'account.channel.revise_project', name='revise_project'),

    url(r'^vip/$', 'account.views.vip', name='account_vip'),
]
