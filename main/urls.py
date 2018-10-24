from django.urls import path
import issues.views
import conf.views


urlpatterns = [
    path('', issues.views.list, name="issues-list"),
    path('configure/', conf.views.configure, name="configure"),
]
