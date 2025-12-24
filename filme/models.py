from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
LISTA_CATEGORIAS = (
    ("ANALISES", "Análises"),
    ("PROGRAMACAO", "Programação"),
    ("APRESENTACAO", "Apresentação"),
    ("OUTROS", "Outros"),
)
# criar a classe para os filmes
class Filme(models.Model):
    titulo = models.CharField(max_length=100)
    thumb = models.ImageField(upload_to='tumb_filmes')
    descricao = models.TextField(max_length=1000)
    categoria = models.CharField(max_length=15, choices=LISTA_CATEGORIAS)
    visualizacoes = models.IntegerField (default=0)
    data_de_criacao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titulo

# criar o episódio
class Episodio(models.Model):
    filme = models.ForeignKey("Filme", related_name="episodios", on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    video = models.URLField()

    def __str__(self):
        return self.filme.titulo + " - " + self.titulo


# criar o usuário

class Usuario (AbstractUser):
    filmes_vistos = models.ManyToManyField("Filme")