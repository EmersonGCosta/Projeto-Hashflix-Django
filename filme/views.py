from django.shortcuts import render, redirect, reverse
from .models import Filme, Usuario
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CriarContaForm, FormHomepage
# Create your views here.
#classes

class Homepage(FormView):
    template_name = "homepage.html"
    form_class = FormHomepage

    def get(self, request, *args, **kwargs):
        #descobrir se o usuário está logado no site, caso positivo redirecionar para a página dos filmes.
        if request.user.is_authenticated:
            return redirect('filme:homefilmes')
        # redireciona o usuário para a homepage caso o usuario não esteja logado.
        else:
            return super().get(request, *args, **kwargs)
    def get_success_url(self):
        email = self.request.POST.get('email')
        usuarios = Usuario.objects.filter(email=email)
        if usuarios:
            return reverse("filme:login")
        else:
            return reverse("filme:criarconta")


class Homefilmes(LoginRequiredMixin, ListView):
    template_name = "homefilmes.html"
    model = Filme
    #object_list > lista de itens do modelo

class DetalhesFilme(LoginRequiredMixin, DetailView):
    template_name = "detalhesfilme.html"
    model = Filme
    # object_list > Um item do modelo

    def get(self, request, *args, **kwargs):
        #descobrir qual filme esta acessando
        filme = self.get_object()
        #somar 1 nas visualizações do filme
        filme.visualizacoes += 1
        #salvar a lista
        filme.save()
        usuario = request.user
        usuario.filmes_vistos.add(filme)
        return super().get(request, *args, **kwargs) #rediraciona o usuário para a url final


    def get_context_data(self, **kwargs):
        context = super(DetalhesFilme, self).get_context_data(**kwargs)
        #filtrar a tabela de filmes pegando os filmes cuja categoria é igual a categoria da página
        #self.get_object()
        filmes_relacionados = self.model.objects.filter(categoria = self.get_object().categoria)
        context['filmes_relacionados'] = filmes_relacionados
        return context

class PesquisaFilme(ListView):
    template_name = "pesquisa.html"
    model = Filme

    #object list
    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('query')
        if termo_pesquisa:
            object_list= self.model.objects.filter(titulo__icontains=termo_pesquisa)
            return object_list
        else:
            return None

class Paginaperfil(LoginRequiredMixin, UpdateView):
    template_name = "editarperfil.html"
    model = Usuario
    fields = ["first_name", "last_name", "email"]

    def get_success_url(self):
        return reverse("filme:homefilmes")

class Criarconta(FormView):
    template_name = "criarconta.html"
    form_class = CriarContaForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("filme:login")

# functions
# Create your views here.

# def homepage(request):
#     return render(request, "homepage.html")
# def homefilmes(request):
#     context = {}
#     lista_filmes = Filme.objects.all()
#     context['lista_filmes'] = lista_filmes
#     return render(request, "homefilmes.html", context)

