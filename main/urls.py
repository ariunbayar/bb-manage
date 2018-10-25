from django.urls import path
import issues.views
import repo.views
import conf.views


urlpatterns = [
    path('configure/', conf.views.configure, name="configure"),

    path('repo/', repo.views.list, name="repo-list"),
    path('repo/<slug>/', repo.views.detail, name="repo-detail"),
    path('repo/<slug>/toggle-sync-issues', repo.views.toggle_sync_issues, name="repo-toggle-sync-issues"),


    path('', issues.views.list, name="issues-list"),
]
