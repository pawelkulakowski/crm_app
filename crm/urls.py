"""crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from salesleads.views import (
    LoginView,
    LogoutView,
    UserListView,
    SalesLeadAddFormView,
    SalesLeadListView,
    SalesLeadDetailView,
    SearchResults,
    SalesLeadMap,
    DashboardView,
    SalesLeadDelete,
    ContactPersonDelete,
    PlannedActitivitiesDelete,
    CommentDelete,
    CommentUpdate,
    ContactPersonUpdate,
    PlannedActivitiesUpdate,
    country_create,
    ReportView,
    ChangeUserView,
    SalesLeadModalDelete,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users/', UserListView.as_view(), name='users'),
    path('contactperson_delete/<int:contactperson_id>', ContactPersonDelete.as_view(), name='contactperson-delete'),
    path('contactperson_update/<int:contactperson_id>', ContactPersonUpdate.as_view(), name='contactperson-update'),
    path('comment_delete/<int:comment_id>', CommentDelete.as_view(), name='comment-delete'),
    path('comment_update/<int:comment_id>', CommentUpdate.as_view(), name='comment-update'),
    path('plannedactivities_delete/<int:plannedactivity_id>', PlannedActitivitiesDelete.as_view(), name='plannedactivity-delete'),
    path('plannedactivities_update/<int:plannedactivities_id>', PlannedActivitiesUpdate.as_view(), name='plannedactivity-update'),
    path('saleslead_add/', SalesLeadAddFormView.as_view(), name='saleslead-add'),
    path('saleslead_delete/<int:saleslead_id>', SalesLeadDelete.as_view(), name='saleslead-delete'),
    path('saleslead_delete2/<int:saleslead_id>', SalesLeadModalDelete.as_view(), name='saleslead-delete-modal'),
    path('salesleads/', SalesLeadListView.as_view(), name='salesleads'),
    path('saleslead_detail/<int:saleslead_id>/', SalesLeadDetailView.as_view(), name='saleslead-detail'),
    path('search_results/', SearchResults.as_view(), name='search-results'),
    path('map/', SalesLeadMap.as_view(), name='map'),
    path('', DashboardView.as_view(), name='dashboard'),
    path('country_create/', country_create, name='country-create'),
    path('report/', ReportView.as_view(), name='report'),
    path('user_change/<int:saleslead_id>/', ChangeUserView.as_view(), name='user-change')
]
