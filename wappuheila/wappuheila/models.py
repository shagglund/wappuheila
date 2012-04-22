# -*- coding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.db.models import permalink
from django.utils.translation import ugettext_lazy
from wappuheila import settings

class Wappuheila(models.Model):
    user = models.OneToOneField(User)
    pic_url = models.URLField(blank=True, null=True, verbose_name=ugettext_lazy(u'Kuvan url'))
    intro = models.TextField(max_length=2048, verbose_name=ugettext_lazy(u'Itsesi kuvaus tai esittely'))
    substantives = models.CharField(max_length=128, verbose_name=ugettext_lazy(u'Kuvaile itseäsi kolmella substantiivilla'))
    joke = models.TextField(max_length=2048, verbose_name=ugettext_lazy(u'Kerro vitsi'))
    if_i_were_you = models.CharField(max_length=128, verbose_name=ugettext_lazy(u'Jos mä oisin sä niin sä oisit...'))
    most_preferably = models.TextField(max_length=256, verbose_name=ugettext_lazy(u'Wappuheilani kanssa mieluiten...'))
    
    def __unicode__(self):
        return self.user.get_full_name()
    
    def __str__(self):
        return self.__unicode__()
    
    def punch_line(self):
        if len(self.intro) > 128:
            return self.intro[0:128] + "..."
        else:
            return self.intro
        
    def get_picture_url(self):
        if self.pic_url is None or len(self.pic_url) == 0:
            return settings.STATIC_URL + "no_avatar.png"
        else:
            return self.pic_url
        
    @permalink
    def get_absolute_url(self):
        return ('wappuheila_details', (), {'wph_id':self.id})
        

class Question(models.Model):
    title = models.TextField()
    answer_type = models.CharField(max_length=1,
                                   choices=(("M","Multiple choice"),
                                            ("S","Single choice"),))
    
    def is_multiple_choice(self):
        return self.answer_type == 'M'
    
    def __unicode__(self):
        return self.title
    
class QuestionOption(models.Model):
    question = models.ForeignKey(Question, related_name='choices')
    text = models.CharField(max_length=128)
    
    def __unicode__(self):
        return unicode(self.text)
    
class Answer(models.Model):
    user = models.OneToOneField(User, blank=True, null=True)
    choices = models.ManyToManyField(QuestionOption, blank=True)
    answer_time = models.DateTimeField(auto_now_add=True, auto_now=True)
    
    def __unicode__(self):
        if self.user is None:
            return "AnonymousUser"
        return "%s / %s" % (self.user.username, self.user.get_full_name())
    
    
class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages")
    receiver = models.ForeignKey(User, related_name="received_messages")
    message = models.TextField()
    
    