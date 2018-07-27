from django.urls import path

from . import views

app_name = 'menu'
urlpatterns = [
	path('', views.index.index, name = 'index'),
	path('dish/', views.dish.dish, name = 'dish'),
	path('ingredient/', views.ingredient.ingredient, name = 'ingredient'),
	path('program/', views.program.program, name = 'program'),


	path('reports/', views.reports.report_list, name = 'reports'),
	path('reports/<int:year>/<int:month>/<int:day>/', views.reports.report, name = 'daily_reports'),
	path('reports/<int:year>/<int:month>/<int:day>/<program>', views.reports.report, name = 'program_reports'),
]
