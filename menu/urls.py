from django.urls import path

from . import views

app_name = 'menu'
urlpatterns = [
    path('', views.index.index, name='index'),
    path('dish/', views.dish.dish, name='dish'),
    path('ingredient/', views.ingredient.ingredient, name='ingredient'),
    path('program/', views.program.program, name='program'),

    path('reports/', views.reports.report_list, name='reports'),
    path('reports/<int:year>/<int:month>/<int:day>/', views.reports.report, name='daily_reports'),
    path(
        'reports/<int:year>/<int:month>/<int:day>/program/<program>',
        views.reports.report,
        {'is_super_program': False},
        name='program_reports'
    ),
    path(
        'reports/<int:year>/<int:month>/<int:day>/super_program/<program>',
        views.reports.report,
        {'is_super_program': True},
        name='super_program_reports'
    ),
]
