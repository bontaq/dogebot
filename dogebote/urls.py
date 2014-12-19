from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api
from core.api import MessageResource, WalletResource, TransactionResource, UserResource

admin.autodiscover()

api_v1 = Api(api_name='v1')

api_v1.register(MessageResource())
api_v1.register(WalletResource())
api_v1.register(TransactionResource())
api_v1.register(UserResource())


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dogebote.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'core.views.home', name='home'),
    (r'^api/', include(api_v1.urls)),
)
