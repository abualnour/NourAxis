from django import forms

from .models import WEEKDAY_CHOICES, RegionalHoliday, RegionalWorkCalendar


class RegionalWorkCalendarForm(forms.ModelForm):
    weekend_day_selection = forms.MultipleChoiceField(
        label="Weekly Off Days",
        choices=WEEKDAY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = RegionalWorkCalendar
        fields = ["name", "region_code", "notes", "is_active"]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs["class"] = "calendar-checkbox-list"
            else:
                existing = field.widget.attrs.get("class", "")
                field.widget.attrs["class"] = f"{existing} form-control".strip()

        if self.instance and self.instance.pk:
            self.fields["weekend_day_selection"].initial = [
                str(value) for value in sorted(self.instance.weekend_day_numbers)
            ]

    def clean_weekend_day_selection(self):
        values = self.cleaned_data.get("weekend_day_selection") or []
        if not values:
            raise forms.ValidationError("Select at least one weekly off day.")
        return values

    def save(self, commit=True):
        instance = super().save(commit=False)
        weekend_values = sorted({int(value) for value in self.cleaned_data.get("weekend_day_selection") or []})
        instance.weekend_days = ",".join(str(value) for value in weekend_values)
        if commit:
            instance.save()
        return instance


class RegionalHolidayForm(forms.ModelForm):
    class Meta:
        model = RegionalHoliday
        fields = ["holiday_date", "title", "holiday_type", "is_non_working_day", "notes"]
        widgets = {
            "holiday_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
            else:
                existing = field.widget.attrs.get("class", "")
                field.widget.attrs["class"] = f"{existing} form-control".strip()
