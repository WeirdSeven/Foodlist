from django.urls import path

from . import views

app_name = 'menu'
urlpatterns = [
	path('', views.index.index, name = 'index'),
	path('dish/', views.dish.dish, name = 'dish'),
	path('ingredient/', views.ingredient.ingredient, name = 'ingredient'),
	path('program/', views.program.program, name = 'program'),
	path('download/program/', views.download.program_report, name = 'download_program_report'),
	path('download/program/<name>/<int:year>/<int:month>/<int:day>/ingredient/', views.download.program_ingredient_report, name = 'download_program_ingredient_report'),
	path('download/company/', views.download.company_report, name = 'download_company_report'),
	path('download/company/<int:year>/<int:month>/<int:day>/ingredient/', views.download.company_ingredient_report, name = 'download_company_ingredient_report'),
]