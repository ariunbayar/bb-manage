from django import forms


class FilterIssuesForm(forms.Form):

    def __init__(self, assignees, repos, *args, **kwargs):

        super(FilterIssuesForm, self).__init__(*args, **kwargs)

        self.fields['assignees'] = forms.MultipleChoiceField(
                choices=assignees,
                required=False,
                widget=forms.CheckboxSelectMultiple,
                )

        self.fields['repos'] = forms.MultipleChoiceField(
                choices=repos,
                required=False,
                widget=forms.CheckboxSelectMultiple,
                )

    class Meta:
        fields = ('assignees', 'repos')
