from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy

from sportifyapp.models import Sport, Echipa, Meci, Jucator
from sportifyapp.forms import TeamForm, MatchForm

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class SportView(View):

    def get(self, request, *args, **kwargs):
        teams_list = Echipa.objects.filter(sport__nume="Fotbal")
        form = TeamForm()
        context = {'teams_list': teams_list, 'form': form, 'id': kwargs['sport_id']}
        return render(request, 'sport.html', context)


    def post(self, request, *args, **kwargs):
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.sport_id = kwargs['sport_id']
            team.save() 
            return HttpResponseRedirect(str(kwargs['sport_id']))
        else:
            context = {'teams_list': teams_list, 'form': form, 'id': kwargs['sport_id']}
            return render(request, 'sport.html', context)

class TeamView(View):

    def get(self, request, *args, **kwargs):
        
        team = Echipa.objects.filter(id=kwargs['team_id'])[0]
        matches = Meci.objects.filter(echipa1 = kwargs['team_id']) | Meci.objects.filter(echipa2 = kwargs['team_id'])
        players = Jucator.objects.filter(echipa=kwargs['team_id'])

        form = MatchForm(team_id=team.id, team_sport=team.sport)

        context = {
            'matches': matches,
            'form': form,
            'players': players
            }
        return render(request, 'team.html', context)
    
    def post(self, request, *args, **kwargs):

        team = Echipa.objects.filter(id=kwargs['team_id'])[0]
        # matches = team.meciuri.all()
        form = MatchForm(request.POST, team_id=team.id, team_sport=team.sport)
        if form.is_valid():
            meci = Meci()
            meci.data = form.cleaned_data['data']
            meci.echipa1 = team
            meci.echipa2 = form.cleaned_data['echipa'] 
            meci.save()
            return HttpResponseRedirect(str(kwargs['team_id']))


#PARTEA LUI ARITON COSMIN


class HomeView(View):
    def get(self, request):
        sports_list = Sport.objects.all()
        jucatori = Jucator.objects.all()
        context = {
            'sports_list': sports_list,
            'jucatori': jucatori
        }

        return render(request, 'home.html', context)



class JucatorCreate(CreateView):
    model = Jucator
    fields = ['prenume', 'nume', 'varsta']
    success_url = reverse_lazy('home')


class JucatorUpdate(UpdateView):
    model = Jucator
    fields = ['echipa']
    success_url = reverse_lazy('home')

class JucatorDelete(DeleteView):
    model = Jucator
    success_url = reverse_lazy('home')


#PARTEA LUI ARITON COSMIN