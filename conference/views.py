from tempfile import template
from urllib import request
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from conference.models import Conférencier,Participant
from conference.models import Conférence
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

def loginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('dashboard'))
        
        else:
            messages.error(request, "Vos identifiants ne correspondent pas !")
            return redirect('login')
            
    context = {}
    return render(request,'login.html',context)

@login_required(login_url='login')
def LogoutPage(request):
    logout(request)
    return redirect('accueil')


@login_required(login_url='login')
def dashboard (request):
      conference = Conférence.objects.all().values()
      conferencier = Conférencier.objects.all().values()
      participant = Participant.objects.all().values()
      template =loader.get_template('dashboard.html')

      total_conferences = conference.count()
      total_conferenciers = conferencier.count()
      total_participants = participant.count()

      context = {
        'conference' : conference,
        'total_conferences' : total_conferences,
        'conferencier' : conferencier,
        'total_conferenciers' : total_conferenciers,
        'participant' : participant,
        'total_participants' : total_participants,
      }
      return HttpResponse (template.render(context,request))

""" @login_required(login_url='login')
def conference(request):
    conferences = Conférence.objects.all().values()
    conferencier = Conférencier.objects.all().values()
    context = {
        'conferences': conferences,
        'conferencier' : conferencier,
        }
    return render(request, 'conference.html', context) """
@login_required(login_url='login')
def conference(request):
    conferences = Conférence.objects.all().values()
    conferencier = Conférencier.objects.all().values()

    paginator = Paginator(conferences, 3)  # Number of conferences per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'conferences': page_obj,
        'conferencier': conferencier,
    }
    return render(request, 'conference.html', context)

@login_required(login_url='login')
def addConf(request):
    conference = Conférence.objects.all().values()
    conferencier = Conférencier.objects.all().values()
    template = loader.get_template('addConference.html')
    context = {
        'conference': conference,
        'conferencier': conferencier,
    }
    return HttpResponse(template.render(context, request))
@login_required(login_url='login')
def add_conference(request):
    if request.method == 'POST':
        code = request.POST['code']
        nom = request.POST['nom']
        topic = request.POST['topic']
        date_debut = request.POST['dateDebut']
        date_fin = request.POST['dateFin']
        start_time = request.POST['startTime']
        end_time = request.POST['endTime']
        capacite = request.POST['capacite']
        duree = request.POST['duree']
        pays = request.POST['pays']
        region = request.POST['region']
        conferencier = request.POST['conferencier']
        conferencier = Conférencier.objects.get(id=conferencier)

        if Conférence.objects.filter(code=code).exists():
            messages.error(request, "La conférence existe déjà !")
            return redirect('addConf')

        conference = Conférence()
        conference.code = code
        conference.nom = nom
        conference.topic = topic
        conference.dateDebut = date_debut
        conference.dateFin = date_fin
        conference.startTime = start_time
        conference.endTime = end_time
        conference.capacite = capacite
        conference.duree = duree
        conference.pays = pays
        conference.region = region
        conference.conferencier = conferencier

        if len(request.FILES) != 0:
            conference.programme = request.FILES['programme']
        conference.save()
        messages.success(request, "La conférence est ajoutée avec succès")
        return redirect('conference')
    else:
        conferenciers = Conférencier.objects.all()
        context = {'conferenciers': conferenciers}
        return render(request, 'add_conference.html', context)

@login_required(login_url='login')
def del_con(request, id):
    conference = Conférence.objects.get(id=id)
    conference.delete()
    return HttpResponseRedirect(reverse('conference'))

@login_required(login_url='login')
def update_con(request, id):
    conf = Conférence.objects.filter(id=id).values().first()
    con = Conférencier.objects.all().values()
    template = loader.get_template('updateConference.html')
    context = {
        'conf': conf,
        'con': con,
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='login')
def update_con_action(request, id):
    code = request.POST['code']
    nom = request.POST['nom']
    capacite = request.POST['capacite']
    dateDebut = request.POST['dateDebut']
    startTime = request.POST['startTime']
    endTime = request.POST['endTime']
    topic = request.POST['topic']
    duree = request.POST['duree']
    pays = request.POST['pays']
    region = request.POST['region']
    conferencier = request.POST['conferencier']
    conferencier = Conférencier.objects.get(id=conferencier)

    conference = Conférence.objects.get(id=id)
    if len(request.FILES) != 0:
       conference.imageConf=request.FILES['imageConf']
       conference.programme = request.FILES['programme']

    conference.code = code
    conference.nom = nom
    conference.capacite = capacite
    conference.dateDebut = dateDebut
    conference.startTime = startTime
    conference.endTime = endTime
    conference.topic = topic
    conference.duree = duree
    conference.pays = pays
    conference.region = region
    conference.conferencier = conferencier

    conference.save()
    messages.success(request, " La conférence a été modifiée avec succés ")
    return redirect('conference')


@login_required(login_url='login')
def conferencier(request):
    conferencier_list = Conférencier.objects.all()
    paginator = Paginator(conferencier_list, 3)  # Show 10 conferenciers per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'conferencier.html', context)
@login_required(login_url='login')
def add(request):
    conferencier = Conférencier.objects.all().values()
    template = loader.get_template('addConferencier.html')
    context = {
        'conferencier': conferencier,
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='login')
def add_conferencier(request):
    if request.method == 'POST':
        nom = request.POST.get('nom', '').strip()
        prenom = request.POST.get('prenom', '').strip()
        email = request.POST.get('email', '').strip()
        telephone = request.POST.get('telephone', '').strip()
        bio = request.POST.get('bio', '').strip()

        if not nom or not prenom or not email or not telephone or not bio:
            messages.error(request, "Veuillez remplir tous les champs!")
            return redirect('add')

        conf = Conférencier()
        conf.nom = nom
        conf.prenom = prenom
        conf.email = email
        conf.telephone = telephone
        conf.bio = bio

        if Conférencier.objects.filter(email=email).exists():
            messages.error(request, "L'email existe déjà!")
            return redirect('add')

        if len(request.FILES) != 0:
            conf.image = request.FILES['image']
        conf.save()

        messages.success(request, "Le conférencier est ajouté avec succès")
        return redirect('conferencier')
    else:
        template = loader.get_template('add_conferencier.html')
        context = {}
        return HttpResponse(template.render(context, request))

@login_required(login_url='login')
def update_conferencier(request, id):
    conferencier = Conférencier.objects.filter(id=id).values().first()
    template = loader.get_template('updateConferencier.html')
    context = {
        'conferencier': conferencier,
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='login')
def update_conferencier_action(request, id):
    nom = request.POST['nom']
    prenom = request.POST['prenom']
    email = request.POST['email']
    telephone = request.POST['telephone']
    bio = request.POST['bio']
    
    conferencier = Conférencier.objects.get(id=id)
    if len(request.FILES) != 0:
       conferencier.image=request.FILES['image']

    conferencier.nom = nom
    conferencier.prenom = prenom
    conferencier.email = email
    conferencier.telephone = telephone
    conferencier.bio = bio

    conferencier.save()
    messages.success(request, " Le conférencier a été modifié avec succés ")
    return redirect('conferencier')

@login_required(login_url='login')
def del_conferencier(request, id):
    conferencier = Conférencier.objects.get(id=id)
    conferencier.delete()
    return HttpResponseRedirect(reverse('conferencier'))

@login_required(login_url='login')
def liste_participants(request, pk):
    conference = Conférence.objects.get(pk=pk)
    participants = conference.get_participants()
    context = {
        'conference': conference,
        'participants': participants
    }
    return render(request, 'list_participant.html', context)

@login_required(login_url='login')
def del_participant(request, pk, id):
    participant = Participant.objects.get(id=id)
    participant.delete()
    return HttpResponseRedirect(reverse('liste_participants', args=[pk]))

@login_required(login_url='login')
def update_participant(request, pk, id):
    conference = Conférence.objects.get(pk=pk)
    participant = Participant.objects.filter(id=id).values().first()
    template = loader.get_template('updateParticipant.html')
    context = {
        'participant': participant,
        'conference': conference,
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='login')
def update_participant_action(request,pk, id):
    nom = request.POST['nom']
    prenom = request.POST['prenom']
    email = request.POST['email']
    telephone = request.POST['telephone']
    
    participant = Participant.objects.get(id=id)

    participant.nom = nom
    participant.prenom = prenom
    participant.email = email
    participant.telephone = telephone

    participant.save()
    messages.success(request, " Le participant a été modifié avec succés ")
    return redirect('liste_participants', pk=participant.conference.pk)

@login_required(login_url='login')
def details_conference(request,id):
    conference = Conférence.objects.get(id=id)
    context = {'conference': conference}
    return render(request, 'details-conference.html', context)


def homePage (request):
      conferences = Conférence.objects.all().values()
      template =loader.get_template('accueil.html')
      context = {'conferences': conferences}

      return HttpResponse(template.render(context, request))

def details_conferenceAccueil(request,id):
    conference = Conférence.objects.get(id=id)
    context = {'conference': conference}
    return render(request, 'detailsConference.html', context)

@require_POST
def inscription_conference(request, conference_id):
    conference = Conférence.objects.get(id=conference_id)

    nom = request.POST.get('nom')
    prenom = request.POST.get('prenom')
    email = request.POST.get('email')
    telephone = request.POST.get('telephone')

    # Vérifier si la conférence est pleine
    if conference.est_pleine():
        messages.error(request, 'Cette conférence est pleine.')
        return redirect('details_conferenceAccueil', id=conference_id)
    else:
        # Ajouter le participant à la conférence
        conference.add_participant(nom=nom, prenom=prenom, email=email, telephone=telephone)
        messages.success(request, 'Vous êtes inscrit avec succés !')
        return redirect('details_conferenceAccueil', id=conference_id)

