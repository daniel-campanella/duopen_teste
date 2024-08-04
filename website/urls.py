from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
	path('', views.home, name='home'),
	path('search/', views.search, name='search'),
	path('accounts/', views.show_accounts, name='accounts'),
	path('transactions/', views.show_transactions, name='transactions'),
	path('terms_and_conditions/', views.terms_and_conditions, name='terms_and_conditions'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)