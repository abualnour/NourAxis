from django import forms

from employees.models import Employee

from .models import BranchPost, BranchPostReply


class BranchPostForm(forms.ModelForm):
    class Meta:
        model = BranchPost
        fields = [
            "post_type",
            "title",
            "body",
            "assignee",
            "priority",
            "due_date",
            "is_pinned",
            "requires_acknowledgement",
            "attachment",
        ]
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Write a structured branch update, instruction, issue, or task details.",
                }
            ),
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, branch=None, can_manage=False, **kwargs):
        self.branch = branch
        self.can_manage = can_manage
        super().__init__(*args, **kwargs)

        if branch is not None:
            self.fields["assignee"].queryset = (
                Employee.objects.select_related("job_title")
                .filter(branch=branch, is_active=True)
                .order_by("full_name", "employee_id")
            )
        else:
            self.fields["assignee"].queryset = Employee.objects.none()

        if not can_manage:
            self.fields["post_type"].choices = [
                choice
                for choice in self.fields["post_type"].choices
                if choice[0] in {BranchPost.POST_TYPE_UPDATE, BranchPost.POST_TYPE_ISSUE}
            ]
            self.fields["is_pinned"].widget = forms.HiddenInput()
            self.fields["requires_acknowledgement"].widget = forms.HiddenInput()
            self.fields["priority"].choices = [
                ("", "---------"),
                (BranchPost.PRIORITY_LOW, "Low"),
                (BranchPost.PRIORITY_MEDIUM, "Medium"),
            ]

        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs["class"] = "form-check-input"
            elif isinstance(widget, forms.FileInput):
                widget.attrs["class"] = "form-control"
            else:
                existing = widget.attrs.get("class", "")
                widget.attrs["class"] = f"{existing} form-control".strip()

        self.fields["title"].widget.attrs.setdefault("placeholder", "Example: Friday stock count follow-up")
        self.fields["assignee"].required = False
        self.fields["priority"].required = False
        self.fields["due_date"].required = False
        self.fields["attachment"].required = False

    def clean_title(self):
        title = (self.cleaned_data.get("title") or "").strip()
        if not title:
            raise forms.ValidationError("Title is required.")
        return title

    def clean_body(self):
        return (self.cleaned_data.get("body") or "").strip()


class BranchPostReplyForm(forms.ModelForm):
    class Meta:
        model = BranchPostReply
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Add a reply, progress update, or completion note.",
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        existing = self.fields["body"].widget.attrs.get("class", "")
        self.fields["body"].widget.attrs["class"] = f"{existing} form-control".strip()

    def clean_body(self):
        body = (self.cleaned_data.get("body") or "").strip()
        if not body:
            raise forms.ValidationError("Reply text is required.")
        return body
