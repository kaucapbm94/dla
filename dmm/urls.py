from django.urls import path
from . import views

urlpatterns = [
    # path('register/', views.registerPage, name='register'),
    path('', views.Statistics),
    path('contact/', views.contact, name='contact'),
    path('example/', views.index, name='example'),
    path('create_normal/', views.create_book_model_form, name='book_list'),
    path('programmer/show/<programmer_id>/', views.programmer, name='programmer'),
    path('programmer/new/', views.programmer_new, name='programmer_new'),
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
