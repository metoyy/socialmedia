from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Chat(models.Model):
    DIALOG = 'D'
    CHAT = 'C'
    CHAT_TYPE_CHOICES = (
        (DIALOG, _('Dialog')),
        (CHAT, _('Chat'))
    )

    type = models.CharField(
        _('Type'),
        max_length=1,
        choices=CHAT_TYPE_CHOICES,
        default=DIALOG
    )
    members = models.ManyToManyField(User, verbose_name=_("Member"), related_name='member_of')


class Message(models.Model):
    chat = models.ForeignKey(Chat, verbose_name=_("Chat"), on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.SET('deleted'),
                               related_name='messages_count')
    message = models.TextField(_("Message"))
    pub_date = models.DateTimeField(_('Date'), auto_now_add=True)
    is_read = models.BooleanField(_('Is read'), default=False)

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return self.message
