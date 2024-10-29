from django.db import models
import hashlib
import time


def random_filename(instance, filename):
  #Extrai a extensão do arquivo
  ext = filename.split('.')[-1]

  # Usa o timestamp atual e o nome original para gerar o hash simples
  hash_object = hashlib.md5(f"{filename}{time.time()}".encode('utf-8'))
  return f"{hash_object.hexdigest()}.{ext}"

# Create your models here.
class Video(models.Model):
  title = models.CharField(max_length=100, unique=True, verbose_name='Título')
  description = models.TextField(verbose_name='Descrição')
  thumbnail = models.ImageField(upload_to=random_filename, verbose_name='Thumbnail')
  slug = models.SlugField(unique=True)
  published_at = models.DateTimeField(verbose_name='Publicado em', null=True, editable=False)
  is_published = models.BooleanField(default=False, verbose_name='Publicado')
  num_likes = models.IntegerField(default=0, verbose_name='Likes', editable=False)
  num_views = models.IntegerField(default=0, verbose_name='Visualizações', editable=False)
  tags = models.ManyToManyField('Tag', verbose_name='Tags', related_name='videos')
  author = models.ForeignKey('auth.user', on_delete=models.PROTECT, verbose_name='Autor', related_name='videos', editable=False)


class VideoMedia(models.Model):
  
  class Status(models.TextChoices):
    UPLOADED_STARTED = 'UPLOADED_STARTED', 'Upload Iniciado'
    PROCESS_STARTED = 'PROCESS_STARTED', 'Processamento Inicializado',
    PROCESS_FINISHED = 'PROCESS_FINISHED', 'Processamento Finalizad',
    PROCESS_ERROR = 'PROCESS_ERROR', 'Erro no Processamento'

  video_path = models.CharField(max_length=255, verbose_name='Vídeo')
  status = models.CharField(max_length=20, choices=Status.choices, default=Status.UPLOADED_STARTED, verbose_name='Status')
  video = models.OneToOneField('Video', on_delete=models.PROTECT, verbose_name='Vídeo', related_name='video_media')

  def get_status_display(self):
    return VideoMedia.Status(self.status).label
  
  class Media:
    verbose_name = 'Midia'
    verbose_name_plural = 'Mídias'
    

class Tag(models.Model):
  name = models.CharField(max_length=50, unique=True, verbose_name='Nome')

  class Meta:
    verbose_name = 'Tag'
    verbose_name_plural = 'Tags'

  def __str__(self):
    return self.name