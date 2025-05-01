from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# ADMINISTRATEUR
class Administrateur(models.Model):
    SEXE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin')
    ]

    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    telephone = models.CharField(max_length=25)
    image = models.ImageField(upload_to='img/', null=True, blank=True)
    adresse = models.CharField(max_length=50)
    status = models.CharField(max_length=15)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.status})"


# STRUCTURE DE SANTE
class StructureSante(models.Model):
    TYPE_CHOICES = [
        ('hopital', 'Hôpital'),
        ('clinique', 'Clinique'),
    ]
    STATUT_CHOICES = [
        ('actif', 'Actif'),
        ('inactif', 'Inactif'),
    ]

    nom = models.CharField(max_length=100)
    type_structure = models.CharField(max_length=20, choices=TYPE_CHOICES)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)
    adresse = models.TextField()
    ville = models.CharField(max_length=30)
    region = models.CharField(max_length=30)
    telephone = models.CharField(max_length=25)
    site_web = models.URLField(blank=True, null=True)
    role = models.CharField(max_length=15)
    status = models.CharField(max_length=50, choices=STATUT_CHOICES)
    date_inscription = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='img/', null=True, blank=True)
    created_by = models.ForeignKey(Administrateur, on_delete=models.SET_NULL, related_name='structuresante_created', null=True, blank=True)
    updated_by = models.ForeignKey(Administrateur, on_delete=models.SET_NULL, related_name='structuresante_updated', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nom} - {self.type_structure}"


# SPECIALISATION
class Specialisation(models.Model):
    nom = models.CharField(max_length=50)
    created_by = models.ForeignKey(Administrateur, on_delete=models.SET_NULL, related_name='specialisations_created', null=True, blank=True)
    updated_by = models.ForeignKey(Administrateur, on_delete=models.SET_NULL, related_name='specialisations_updated', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom


# SERVICE
class Service(models.Model):
    nom = models.CharField(max_length=50)
    created_by = models.ForeignKey(Administrateur, on_delete=models.SET_NULL, related_name='services_created', null=True, blank=True)
    updated_by = models.ForeignKey(Administrateur, on_delete=models.SET_NULL, related_name='services_updated', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom


# UTILISATEUR
class Utilisateur(AbstractUser):
    SEXE_CHOICES = [('M', 'Masculin'), ('F', 'Féminin')]
    ROLES = (
        ('medecin', 'Médecin'),
        ('patient', 'Patient'),
    )

    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=50)
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    telephone = models.CharField(max_length=25)
    adresse = models.TextField()
    image = models.ImageField(upload_to='img/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Administrateur, on_delete=models.SET_NULL, related_name='utilisateurs_created', null=True, blank=True)
    updated_by = models.ForeignKey(Administrateur, on_delete=models.SET_NULL, related_name='utilisateurs_updated', null=True, blank=True)
    statut = models.CharField(max_length=20, choices=ROLES)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'prenom', 'nom']

    def __str__(self):
        return f"{self.prenom} {self.nom}"


# MEDECIN
class Medecin(Utilisateur):
    specialisation = models.ForeignKey(Specialisation, on_delete=models.CASCADE)
    structure_sante = models.ForeignKey(StructureSante, on_delete=models.CASCADE)
    numero_licence = models.CharField(max_length=50)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return f"Dr {self.prenom} {self.nom} - {self.specialisation.nom}"


# PATIENT
class Patient(Utilisateur):
    SITUATION_FAMILIALE = (
        ('celibataire', 'Célibataire'),
        ('marie', 'Marié'),
    )
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length=50)
    groupe_sanguin = models.CharField(max_length=5)
    situation_familiale = models.CharField(max_length=15, choices=SITUATION_FAMILIALE)
    profession = models.CharField(max_length=100)
    contact_urgence = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.prenom} {self.nom} - Patient"


# DOSSIER MEDICAL
class DossierMedical(models.Model):
    STATUT = [
        ('cree', 'Créé'),
        ('noncree', 'Non Créé')
    ]

    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Medecin, on_delete=models.SET_NULL, related_name='dossiers_created', null=True, blank=True)
    updated_by = models.ForeignKey(Medecin, on_delete=models.SET_NULL, related_name='dossiers_updated', null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT)

    def __str__(self):
        return f"Dossier de {self.created_at} {self.created_by}"

# EXAMEN MEDICAL
class ExamenMedical(models.Model):
    type_examen = models.CharField(max_length=50)
    resultat = models.CharField(max_length=255)
    diagnostic = models.TextField()
    date_examen = models.DateField()
    lieu = models.CharField(max_length=255)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Medecin, on_delete=models.SET_NULL, related_name='examens_created', null=True, blank=True)
    updated_by = models.ForeignKey(Medecin, on_delete=models.SET_NULL, related_name='examens_updated', null=True, blank=True)

    def __str__(self):
        return f"Examen {self.type_examen} de {self.patient.prenom} {self.patient.nom}"
    

# CONSULTATION
class Consultation(models.Model):
    date_consultation = models.DateField()
    temperature = models.FloatField()
    taille = models.FloatField()
    poids = models.FloatField()
    motif = models.CharField(max_length=100)
    resultat = models.TextField()
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Medecin, on_delete=models.SET_NULL, related_name='consultations_created', null=True, blank=True)
    updated_by = models.ForeignKey(Medecin, on_delete=models.SET_NULL, related_name='consultations_updated', null=True, blank=True)

    def __str__(self):
        return f"Consultation du {self.date_consultation} - {self.patient.prenom} {self.patient.nom}"


# PRESCRIPTION
class Prescription(models.Model):
    medicament = models.CharField(max_length=255)
    duree = models.IntegerField(help_text="Durée du traitement en jours")
    posologie = models.CharField(max_length=255, help_text="Exemple : 2 comprimés par jour")
    mode_administration = models.CharField(max_length=255, help_text="Exemple : Oral, Intraveineuse, etc.")

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Medecin, on_delete=models.SET_NULL, related_name='prescriptions_created', null=True, blank=True)
    updated_by = models.ForeignKey(Medecin, on_delete=models.SET_NULL, related_name='prescriptions_updated', null=True, blank=True)

    def __str__(self):
        return f"Prescription de {self.medicament} pour {self.patient.prenom} {self.patient.nom}"


# DOCUMENT MEDICAL 
class DocumentMedical(models.Model):
    url = models.URLField(max_length=255)
    nom = models.CharField(max_length=255)
    nom_original = models.CharField(max_length=255)
    extension = models.CharField(max_length=10)
    path = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Medecin, on_delete=models.SET_NULL, related_name='documents_created', null=True, blank=True)
    updated_by = models.ForeignKey(Medecin, on_delete=models.SET_NULL, related_name='documents_updated', null=True, blank=True)

    def __str__(self):
        return f"Document {self.nom_original} pour {self.patient.prenom} {self.patient.nom}"
    
# INFO CONFIDENTIEL 
class InfoConfidentielle(models.Model):
    description = models.CharField(max_length=255)
    visible_par_patient = models.BooleanField(default=False)

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Medecin, on_delete=models.SET_NULL, related_name='infos_created', null=True, blank=True)
    updated_by = models.ForeignKey(Medecin, on_delete=models.SET_NULL, related_name='infos_updated', null=True, blank=True)

    def __str__(self):
        return f"Info Confidentielle de {self.patient.prenom} {self.patient.nom}" 
