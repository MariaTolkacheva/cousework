from django import forms


class QuizForm(forms.Form):
    def __init__(self, questions, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for question in questions:
            self.fields[f'question_{question.id}'] = forms.CharField(
                label=question.text,
                required=True,
            )


class AskLLMForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['question'] = forms.CharField(
            label="Вы можете задать вопрос модели и она ответит на него, опираясь на контекст из книг",
            required=True,
        )
