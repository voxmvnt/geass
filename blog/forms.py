from .models import Comment
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'comment-form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        self.fields['content'].widget.attrs.update({'rows': 4, 'cols': 40})

class EditCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

    def __init__(self, *args, **kwargs):
        super(EditCommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'edit-comment-form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Edit Comment'))
        self.fields['content'].widget.attrs.update({'id': 'id_edit_content'})
        self.fields['content'].widget.attrs.update({'rows': 2, 'cols': 20})
