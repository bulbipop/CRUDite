from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path
from django.apps import apps
from . import views

urlpatterns = [
	path('login', LoginView.as_view(template_name='login.html'), name='login'),
	path('logout', LogoutView.as_view(), name='logout'),
	path('', views.generic_template, {'template':'index'}),
	path('about', views.generic_template, {'template':'about'}),
	path('<model_name>/', views.list_view, {'not_in': ['password']}),
	path('<model_name>/<int:pk>', views.details_view),
	path('<model_name>/create', views.create),
	path('<model_name>/update/<int:pk>', views.update),
	path('<model_name>/delete/<int:pk>', views.delete),
]
