import django.shortcuts as dshortcuts

def index(request):
	return dshortcuts.render(request, 'index.html')