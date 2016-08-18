from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView

from django.conf import settings
from django.conf.urls.static import static

from main.views import get_all_goods, cart_add, cart_get, cart_remove, pay_systems, good_exist, confirm_pay, pay

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='base.html')),
    url(r'^good/all/$', get_all_goods, name="all_goods"),
    url(r'^good/exist/(?P<id>[0-9]+)/', good_exist, name="good_exist"),
    url(r'^cart/add/$', cart_add, name="cart_add"),
    url(r'^cart/get/$', cart_get, name="cart_get"),
    url(r'^cart/remove/$', cart_remove, name="cart_remove"),
    url(r'^cart/confirm-cart/$', confirm_pay, name="confirm_pay"),
    url(r'^cart/pay/$', pay, name="pay"),
    url(r'^cart/pay-systems/$', pay_systems, name="pay_systems"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
