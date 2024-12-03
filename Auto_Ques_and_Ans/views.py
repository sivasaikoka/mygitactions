# views.py
from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from .forms import MyInputForm
from .question_and_answers import generate_questions,get_answer

class QuestionInputView(APIView):
    def get(self, request):
        form = MyInputForm()
        return render(request, 'index.html', {'form': form})

    def post(self, request):
        form = MyInputForm(request.POST)
        if form.is_valid():
            given_text = form.cleaned_data['Given_input']
            questions = generate_questions(given_text)
            ques_and_ans = {}
            for question in questions:
                answer = get_answer(question)
                ques_and_ans[question] = answer
            return render(request, 'result.html', {'ques_and_ans': ques_and_ans})
        else:
            return render(request, 'index.html', {'form': form})

class ResultView(APIView):
    def get(self, request):
        # You can retrieve the generated questions and answers from the session
        ques_and_ans = request.session.get('ques_and_ans', {})
        return render(request, 'result.html', {'ques_and_ans': ques_and_ans})
    def post(self, request):
        form = MyInputForm(request.POST)
        if form.is_valid():
            given_text = form.cleaned_data['Given_input']
            questions = generate_questions(given_text)
            ques_and_ans = {}
            for question in questions:
                answer = get_answer(question)
                ques_and_ans[question] = answer
            # Store the generated questions and answers in the session
            request.session['ques_and_ans'] = ques_and_ans
            # Redirect to the result page
            return render(request, 'result.html', {'form': ques_and_ans})

            
        else:
            # Form is not valid, render the result page with form errors
            return redirect('Auto_Ques_and_Ans:generate_questions')
        

class Homepage(TemplateView):
    template_name = "Homepage.html"

