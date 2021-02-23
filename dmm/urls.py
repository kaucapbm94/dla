from django.urls import path
from . import views

from django.conf.urls import url


urlpatterns = [
    url(r'^book/create', views.BookCreate, name="BookCreate"),
    url(r'^specie/create', views.SpecieCreate, name="SpecieCreate"),
    url(r'^tag/create', views.TagCreate, name="TagCreate"),
    url(r'^author/create', views.AuthorCreatePopup, name="AuthorCreate"),
    url(r'^author/(?P<pk>\d+)/edit', views.AuthorEditPopup, name="AuthorEdit"),
    url(r'^author/ajax/get_author_id', views.get_author_id, name="get_author_id"),
    # path('register/', views.registerPage, name='register'),
    path('', views.createResult),
    path('result/new', views.createResult, name='result_create'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('sample_markup_comment/<uuid:result_id>/', views.MarkupCommentPage, name="markup-comment-page"),
    path('sample_markup_comment/<uuid:result_id>/get_initials', views.GetInitialsView.as_view()),
    path('sample_markup_comment/<uuid:result_id>/get_comment_meta', views.GetCommentMetaView.as_view()),

    path('sample_markup_comment/', views.SampleMarkupCommentPage, name="sample-markup-comment-page"),
    path('sample_markup_comment/add_tag', views.AddTagView.as_view()),
    path('sample_markup_comment/get_initials', views.GetInitialsView.as_view()),

    path('sample_markup_comment/add_specie', views.AddSpecieView.as_view()),
    path('sample_markup_comment/get_comment_meta', views.GetCommentMetaView.as_view()),
    path('sample_markup_comment/add_comment', views.AddCommentView.as_view()),
    path('sample_markup_comment/insert_result', views.InsertResultView.as_view()),
    path('sample_markup_comment/insert_comment', views.InsertCommentView.as_view()),
    path('sample_markup_comment/insert_comment_round', views.InsertCommentRoundView.as_view()),

    path('statistics/', views.Statistics, name='home'),
    path('waiting_round/', views.WaitingRounds, name='waiting_rounds'),
]
