from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

path('', views.loginPage,name='login'),

path('dashboard/', views.dashboard, name='dashboard'),


path('conference/',views.conference,name='conference'),

path('conference/details_conference/<int:id>',views.details_conference,name='details_conference'),

path('conference/addConference/', views.addConf, name='addConf'),
path('conference/addConference/add_conference/', views.add_conference, name='add_conference'),

path('conference/update_con/<int:id>', views.update_con, name='update_con'),
path('conference/update_con/update_con_action/<int:id>', views.update_con_action, name='update_con_action'),

path('conference/del_con/<int:id>',views.del_con,name='del_con'),
path('conference/<int:pk>/participants/', views.liste_participants, name='liste_participants'),
path('conference/<int:pk>/participants/del_participant/<int:id>', views.del_participant, name='del_participant'),
path('conference/<int:pk>/participants/update_participant/<int:id>', views.update_participant, name='update_participant'),
path('conference/<int:pk>/participants/update_participant/update_participant_action/<int:id>', views.update_participant_action, name='update_participant_action'),

#path('presenter/',views.presenter,name='presenter'),
#path('presenter/addPresenter/',views.addPresenter,name='addPresenter'),
#path('presenter/addPresenter/add_presenter/',views.add_presenter,name='add_presenter'),


path('conferencier/',views.conferencier,name='conferencier'),
path('conferencier/addConferencier/', views.add, name='add'),
path('conferencier/addConferencier/add_conferencier/', views.add_conferencier, name='add_conferencier'),
path('conferencier/del_conferencier/<int:id>',views.del_conferencier,name='del_conferencier'),
path('conferencier/update_conferencier/<int:id>', views.update_conferencier, name='update_conferencier'),
path('conferencier/update_conferencier/update_conferencier_action/<int:id>', views.update_conferencier_action, name='update_conferencier_action'),


path('login/', views.loginPage,name='login'),
path('logout/', views.LogoutPage,name='logout'),
path('accueil/',views.homePage,name='accueil'),
path('accueil/detailsConference/<int:id>',views.details_conferenceAccueil,name='details_conferenceAccueil'),

path('conference/<int:conference_id>/inscription/', views.inscription_conference, name='inscription_conference'),


]