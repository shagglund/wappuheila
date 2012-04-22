from django.forms.models import ModelForm, ModelMultipleChoiceField, \
    ModelChoiceField
from wappuheila.wappuheila.models import Question, QuestionOption, Wappuheila
from django.forms import widgets
class WappuheilaForm(ModelForm):
    class Meta:
        model = Wappuheila
        exclude = ('user',)
        
class AnswerForm(ModelForm):
    class Meta:
        model = Question
        exclude = ('title', 'answer_type')
        
    def __init__(self, *args, **kwargs):
        ModelForm.__init__(self, *args, **kwargs)
        instance = kwargs['instance']
        if instance.is_multiple_choice():
            self.fields['choices'] = ModelMultipleChoiceField(
                        queryset=QuestionOption.objects.filter(question=instance),
                        widget=widgets.CheckboxSelectMultiple())
        else:
            self.fields['choices'] = ModelChoiceField(
                        queryset=QuestionOption.objects.filter(question=instance),
                        widget=widgets.RadioSelect(), empty_label=None)
    
        
