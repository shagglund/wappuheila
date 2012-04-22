# Create your views here.
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.forms.models import modelformset_factory
from django.views.generic.simple import redirect_to
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from wappuheila.common.utils import render_to_request_context_response
from wappuheila.wappuheila.models import Wappuheila, Question, Answer,\
    QuestionOption, Message
from wappuheila.wappuheila.forms import AnswerForm

def home(request):
    return render_to_request_context_response(request, "main_page.html",{"user" : request.user})

def wappuheila(request, wph_id = None):
    if wph_id is not None:
        wappuheila = get_object_or_404(Wappuheila, id=wph_id)
        return render_to_request_context_response(request,"wappuheila_details.html", {"wappuheila" : wappuheila})
    
    wappuheilas = Wappuheila.objects.all()
    return render_to_request_context_response(request,"wappuheilas.html", {"wappuheilas" : wappuheilas})


def questions(request):
    def add_choices_to_answer(formset, answer):
        """
        An utility function to add choices to a persisted Answer-object
        """
        for form in formset:
            tmp_q = form.save(commit=False)
            if tmp_q.is_multiple_choice():
                for choice in form.cleaned_data['choices']:
                    answer.choices.add(choice)
            else:
                choice = form.cleaned_data['choices']
                answer.choices.add(choice)
        answer.save()
    if not request.user.is_anonymous():
        try:
            Answer.objects.get(user=request.user)
            #render without the questions
            return render_to_request_context_response(request,"questions.html")
        except Answer.DoesNotExist:
            pass
    
    #Create a formset to hold the Questions and the choices from which to pick answers    
    QuestionAnswerFormSet = modelformset_factory(Question, form=AnswerForm, extra=0)
    
    #This is an answer
    if request.method == "POST":
        formset = QuestionAnswerFormSet(request.POST)
        if formset.is_valid():
            if request.user.is_anonymous():
                #a hack to display the results for users not participating in the contest
                answer = Answer.objects.create()
                add_choices_to_answer(formset, answer)
                return results(request, answer)
            else:
                answer,created = Answer.objects.get_or_create(user=request.user)
                if not created:
                    answer.choices.clear()
                add_choices_to_answer(formset, answer)
                return redirect_to(request,reverse('questions_results'),False)   
    
    else:
        formset = QuestionAnswerFormSet()
        
    #The questions should be rendered
    return render_to_request_context_response(request,"questions.html", {"formset": formset, })

def results(request, answer = None):
    if answer is None:
            answer = get_object_or_404(Answer, user = request.user)
    
    #calculate the percentage of same answers compared to each wappuheilas answers
    results = []
    for wappuheila in Wappuheila.objects.all():
        wph_answer = Answer.objects.get(user = wappuheila.user)
        same_answers = QuestionOption.objects.filter(id__in=wph_answer.choices.all()).filter(id__in=answer.choices.all()).distinct().count()
        percentage = float(same_answers) / wph_answer.choices.all().count() * 100
        results.append((percentage, wappuheila))
        
    #sort from largest to smallest percentage
    results.sort(reverse=True)
    rcontext = {'results':results}
    
    #if the user is anonymous
    if request.user.is_anonymous():
        answer.choices.clear()
        answer.delete()
    else:
        try:
            rcontext['sent_message'] = Message.objects.get(sender = request.user)
        except Message.DoesNotExist:
            pass;
        
    return render_to_request_context_response(request, 'questions_results.html', rcontext)

@login_required
@require_POST
def leave_message(request, wph_id):
    data = request.POST.get('message')
    
    #if there is no message raise a 
    if data is None:
        raise Http404
    
    wappuheila = get_object_or_404(Wappuheila, id=wph_id)
    
    Message.objects.create(sender=request.user, receiver=wappuheila.user, message=data)
    
    return HttpResponse(status=204)
    
@login_required
@require_GET
def show_messages(request):
    messages = Message.objects.filter(Q(sender = request.user) | Q(receiver = request.user))
    return render_to_request_context_response(request, 'messages.html', {'messages':messages});
        
    
    
    
    