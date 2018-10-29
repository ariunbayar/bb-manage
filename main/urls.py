from django.urls import path
import issues.views
import repo.views
import conf.views


urlpatterns = [

    path('configure/', conf.views.configure, name="configure"),

    path('repo/', repo.views.list, name="repo-list"),
    path('all-repo/', repo.views.all_repos, name="all-repos"),
    path('repo/<slug>/', repo.views.detail, name="repo-detail"),
    path('repo/<slug>/toggle-watching', repo.views.toggle_watching, name="repo-toggle-watching"),
    path('fetch-repo/', repo.views.fetch_all_repo, name="queue-fetch-repo"),
    path('fetch-issues/<slug>/', repo.views.fetch_issues, name="queue-fetch-issues"),

    path('', issues.views.list, name="issues-list"),
    path('repo/<slug>/issue/<int:issue_id>/', issues.views.detail, name="issue-detail"),

]
