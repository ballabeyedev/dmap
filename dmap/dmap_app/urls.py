from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.index, name='index'),
    path('patient/', views.patient, name='patient'),
    path('structure/', views.structure, name='structure'),
    path('administrateur/', views.admin, name='admin'),
    path('medecin/', views.medecin, name='medecin'),
    path('login/', views.login, name='login'),

    ##PARTIE PATIENT
    path('chatbot/', views.chatbot, name='chatbot'),
    path('consultation/', views.consultation, name='consultation'),
    path('demandecarte/', views.demandecarte, name='demandecarte'),
    path('documentmedical/', views.documentmedical, name='documentmedical'),
    path('dossiermedical/', views.dossiermedical, name='dossiermedical'),
    path('examenmedical/', views.examenmedical, name='examenmedical'),
    path('historiquesoin/', views.historiquesoin, name='historiquesoin'),
    path('prescription/', views.prescription, name='prescription'),
    path('profil/', views.profil, name='profil'),
    path('qrcode/', views.qrcode, name='qrcode'),

    ##PARTIE STRUCTURE
    path('profil_structure/', views.profil_structure, name='profil_structure'),
    path('listeMedecin/', views.listemedecin, name='listeMedecin'),

    ##PARTIE MEDECIN 
    path('profil_medecin/', views.profil_medecin, name='profil_medecin'),
    path('creedossiermedical/', views.creedossiermedical, name='creedossiermedical'),
    path('accederdossiermedical/', views.accederdossiermedical, name='accederdossiermedical'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

