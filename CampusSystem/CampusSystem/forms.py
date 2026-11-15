
from django import forms
from .models import PDFDocument


class PDFDocumentForm(forms.ModelForm):
    class Meta:
        model = PDFDocument
        fields = [
            "title",
            "subject",
            "semester",
            "category",
            "academic_year",
            "file",
        ]

    def clean_file(self):
        uploaded_file = self.cleaned_data.get("file")

        if uploaded_file:
            if not uploaded_file.name.lower().endswith(".pdf"):
                raise forms.ValidationError(
                    "Only PDF files are allowed."
                )

        return uploaded_file
