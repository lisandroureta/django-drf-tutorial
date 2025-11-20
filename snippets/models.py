from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
# 1. Importamos estas librerías para el resaltado de sintaxis
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])

class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
    
    # 2. Campo nuevo: El dueño del snippet
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    # 3. Campo nuevo: El código ya coloreado en HTML
    highlighted = models.TextField()

    class Meta:
        ordering = ['created']

    # 4. Sobrescribimos el método save() para generar el HTML automáticamente
    def save(self, *args, **kwargs):
        """
        Usa la librería `pygments` para crear una representación HTML coloreada del código.
        """
        lexer = get_lexer_by_name(self.language)
        linenos = 'table' if self.linenos else False
        options = {'title': self.title} if self.title else {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                  full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super().save(*args, **kwargs)