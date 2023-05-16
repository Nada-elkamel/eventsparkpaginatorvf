from django.db import models

class Conférencier(models.Model):
    nom = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200)
    email = models.CharField(max_length=50)
    telephone = models.CharField(max_length=8)
    bio = models.CharField(max_length=255)
    image = models.ImageField( upload_to="conference/static/conferenciers/", default="conference/static/image/user.png")

    def __str__(self) -> str:
        return self.email

class Conférence(models.Model):
    code= models.CharField(max_length=10)
    nom = models.CharField(max_length=200)
    capacite = models.IntegerField()
    dateDebut = models.CharField(max_length=8)
    dateFin = models.CharField(max_length=8)
    startTime = models.CharField(max_length=200)
    endTime = models.CharField(max_length=200)
    topic = models.CharField(max_length=200)
    duree = models.IntegerField()
    pays = models.CharField(max_length=200)
    region = models.CharField(max_length=200)
    imageConf = models.ImageField( upload_to="conference/static/conferences/", default="conference/static/image/event.jpg")
    programme = models.FileField(upload_to="conference/static/conferences/")
    conferencier=models.ForeignKey('Conférencier',on_delete=models.CASCADE,)
    
    def __str__(self) -> str:
        return self.topic

    def est_pleine(self):
        return self.participant_set.count() >= self.capacite
    
    def add_participant(self, nom, prenom, email, telephone):
        participant = Participant(nom=nom, prenom=prenom, email=email, telephone=telephone, conference=self)
        participant.save()
        
    def get_participants(self):
        return Participant.objects.filter(conference=self)


class Participant(models.Model):
    nom = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200)
    email = models.CharField(max_length=50)
    telephone = models.CharField(max_length=8)
    conference = models.ForeignKey('Conférence', on_delete=models.CASCADE,)

""" class Presenter(models.Model):
    conferencier=models.ForeignKey('Conférencier', on_delete=models.CASCADE,related_name='presentations')
    conference=models.ForeignKey('Conférence', on_delete=models.CASCADE,related_name='presentateurs') """