from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from .models import Administrateur, StructureSante, Utilisateur

# PAGE ACCUEIL(VITRINE)
def index(request):
    return render(request, 'index.html')

# PAGE DE CONNEXION
def login(request):
    return render(request, 'login.html')

# PAGE D'INSCRIPTION
def inscription_view(request):
    return render(request, 'inscription.html')

# METHODE POUR GERER L'AUTHENTIFICATION DES UTILISATEURS
def store(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")

        # ADMIN PAR DEFAUT (1er utilisateur)
        if email == "admin@gmail.com" and password == "admin123":
            request.session['user_type'] = 'admin'
            request.session['admin_id'] = 0  
            request.session['email'] = email
            request.session['full_name'] = "Super Admin"
            return redirect('admin')

        # AUTHENTIFICATION ADMIN (depuis BDD)
        try:
            admin = Administrateur.objects.get(email=email)
            if check_password(password, admin.mot_de_passe):
                login(request, admin)
                request.session['user_type'] = 'admin'
                request.session['admin_id'] = admin.id
                request.session['email'] = admin.email
                return redirect('admin')
        except Administrateur.DoesNotExist:
            pass

        # AUTHENTIFICATION STRUCTURE DE SANTE
        try:
            structure = StructureSante.objects.get(email=email)
            if check_password(password, structure.mot_de_passe):
                login(request, structure)
                request.session['user_type'] = 'structure'
                request.session['structure_id'] = structure.id
                request.session['email'] = structure.email
                return redirect('structure')
        except StructureSante.DoesNotExist:
            pass

        # AUTHENTIFICATION UTILISATEUR
        try:
            user = Utilisateur.objects.get(email=email)
            if check_password(password, user.password):
                login(request, user)
                request.session['user_type'] = user.status
                request.session['user_id'] = user.id
                request.session['full_name'] = f"{user.nom} {user.prenom}"
                request.session['email'] = user.email

                if user.status == "patient":
                    return redirect('patient')
                elif user.status == "medecin":
                    return redirect('medecin')
        except Utilisateur.DoesNotExist:
            pass

        # AUCUNE CORRESPONDANCE
        error_message = "Email ou mot de passe incorrect."
        return render(request, "login.html", {"error_message": error_message})

    return render(request, "login.html")

#REDIRECTION VERS LA PAGE ADMIN
def admin(request):
    return render(request, 'Administrateur/index.html')

#REDIRECTION VERS LA PAGE STRUCTURE DE SANTE
def structure(request):
    return render(request, 'Structure/index.html')

#REDIRECTION VERS LA PAGE MEDECIN
def medecin(request):
    return render(request, 'Medecin/index.html')

#REDIRECTION VERS LA PAGE PATIENT
def patient(request):
    return render(request, 'Patient/index.html')

### PARTIE ADMIN

### PARTIE STRUCTURE DE SANTE
def profil_structure(request):
    return render(request, 'Structure/page/profil.html')
def listemedecin(request):
    return render(request, 'Structure/page/listemedecin.html')


### PARTIE MEDECIN
def profil_medecin(request):
    return render(request, 'Medecin/page/profil.html')
def creedossiermedical(request):
    return render(request, 'Medecin/page/creedossiermedical.html')
def accederdossiermedical(request):
    return render(request, 'Medecin/page/accederdossiermedical.html')


### PARTIE PATIENT
def chatbot(request):
    return render(request, 'Patient/page/chatbot.html')
def consultation(request):
    return render(request, 'Patient/page/consultation.html')
def demandecarte(request):
    return render(request, 'Patient/page/demandecarte.html')
def documentmedical(request):
    return render(request, 'Patient/page/documentMedical.html')
def dossiermedical(request):
    return render(request, 'Patient/page/dossierMedicalComplet.html')
def examenmedical(request):
    return render(request, 'Patient/page/examenmedicaux.html')
def historiquesoin(request):
    return render(request, 'Patient/page/historiquesoins.html')
def prescription(request):
    return render(request, 'Patient/page/prescription.html')
def profil(request):
    return render(request, 'Patient/page/profil.html')
def qrcode(request):
    return render(request, 'Patient/page/qrcode.html')
