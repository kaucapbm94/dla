from django.urls import path
from . import views
from .decorators import allowed_users
from django.conf.urls import url


urlpatterns = [
    # url(r'^book/create', views.BookCreate, name="BookCreate"),
    path('tag/create/<uuid:expert_id>', views.TagCreate, name="TagCreate"),
    path('specie/create/<uuid:expert_id>', views.SpecieCreate, name="SpecieCreate"),
    # url(r'^author/create', views.AuthorCreatePopup, name="AuthorCreate"),
    # url(r'^author/(?P<pk>\d+)/edit', views.AuthorEditPopup, name="AuthorEdit"),
    # url(r'^author/ajax/get_author_id', views.get_author_id, name="get_author_id"),
    path('', views.createResult, name=''),

    path('result/new', views.createResult, name='sample-markup-comment-page'),
    path('result/new/<uuid:result_id>', views.roundResult, name='markup-comment-page'),
    path('comment_round/show/<uuid:comment_round_id>', views.CommentRoundShow, name='comment-round-show'),
    path('result/show/<uuid:result_id>', views.ResultShow, name='result-show'),

    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('statistics/', views.Statistics, name='home'),
]
