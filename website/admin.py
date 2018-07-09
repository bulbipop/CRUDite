from django.contrib import admin
import django.apps

exclude = ['Group', 'User']

for model in django.apps.apps.get_models():
	if model.__name__ not in exclude:
		admin.site.register(model)
