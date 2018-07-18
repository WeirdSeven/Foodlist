from django.urls import path

from . import views

app_name = 'menu'
urlpatterns = [
	path('', views.index.index, name = 'index'),
	path('dish/', views.dish.dish, name = 'dish'),
	path('ingredient/', views.ingredient.ingredient, name = 'ingredient'),
	path('program/', views.program.program, name = 'program'),


	path('reports/', views.reports.report, name = 'reports'),
	


]

#path('reports/ingredient/days/<int:year>/<int:month>/<int:day>/', views.reports.daily_ingredient_report, name = 'daily_ingredient_report'),
	#path('reports/ingredient/programs/<name>/<int:year>/<int:month>/<int:day>/', views.reports.program_ingredient_report, name = 'program_ingredient_report'),