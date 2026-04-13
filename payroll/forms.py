from django import forms

from organization.models import Company

from .models import PayrollAdjustment, PayrollLine, PayrollObligation, PayrollPeriod, PayrollProfile


class PayrollProfileForm(forms.ModelForm):
    class Meta:
        model = PayrollProfile
        fields = [
            "company",
            "base_salary",
            "housing_allowance",
            "transport_allowance",
            "fixed_deduction",
            "bank_name",
            "iban",
            "status",
        ]
        widgets = {
            "bank_name": forms.TextInput(attrs={"placeholder": "Bank name"}),
            "iban": forms.TextInput(attrs={"placeholder": "IBAN / account reference"}),
        }

    def __init__(self, *args, employee=None, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            widget = field.widget
            existing = widget.attrs.get("class", "")
            widget.attrs["class"] = f"{existing} form-control".strip()

        self.fields["company"].queryset = Company.objects.filter(is_active=True).order_by("name")

        if employee and employee.company_id and not self.instance.pk:
            self.fields["company"].initial = employee.company_id
            if employee.salary:
                self.fields["base_salary"].initial = employee.salary

    def clean_iban(self):
        return (self.cleaned_data.get("iban") or "").strip().upper()


class PayrollPeriodForm(forms.ModelForm):
    class Meta:
        model = PayrollPeriod
        fields = ["company", "title", "period_start", "period_end", "pay_date", "notes"]
        widgets = {
            "period_start": forms.DateInput(attrs={"type": "date"}),
            "period_end": forms.DateInput(attrs={"type": "date"}),
            "pay_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["company"].queryset = Company.objects.filter(is_active=True).order_by("name")


class PayrollLineGenerationForm(forms.Form):
    payroll_period = forms.ModelChoiceField(
        queryset=PayrollPeriod.objects.none(),
        label="Payroll period",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["payroll_period"].queryset = PayrollPeriod.objects.order_by("-period_start", "-id")


class PayrollLineForm(forms.ModelForm):
    class Meta:
        model = PayrollLine
        fields = [
            "base_salary",
            "allowances",
            "deductions",
            "overtime_amount",
            "notes",
        ]
        widgets = {
            "notes": forms.TextInput(attrs={"placeholder": "Notes or adjustment reason"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            widget = field.widget
            existing = widget.attrs.get("class", "")
            widget.attrs["class"] = f"{existing} form-control".strip()

    def save(self, commit=True):
        payroll_line = super().save(commit=False)
        payroll_line.net_pay = payroll_line.calculate_net_pay()
        if commit:
            payroll_line.save()
        return payroll_line


class PayrollAdjustmentForm(forms.ModelForm):
    class Meta:
        model = PayrollAdjustment
        fields = ["title", "adjustment_type", "amount", "notes"]
        widgets = {
            "notes": forms.TextInput(attrs={"placeholder": "Optional note"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            widget = field.widget
            existing = widget.attrs.get("class", "")
            widget.attrs["class"] = f"{existing} form-control".strip()


class PayrollObligationForm(forms.ModelForm):
    class Meta:
        model = PayrollObligation
        fields = [
            "employee",
            "company",
            "title",
            "obligation_type",
            "principal_amount",
            "installment_amount",
            "total_installments",
            "start_date",
            "status",
            "notes",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.TextInput(attrs={"placeholder": "Optional payroll note"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            widget = field.widget
            existing = widget.attrs.get("class", "")
            widget.attrs["class"] = f"{existing} form-control".strip()
