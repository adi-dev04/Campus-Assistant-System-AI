from django.contrib import admin, messages
import fitz
from .views import extract_pdf_text
from CampusSystem.models import CampusSystem, PDFDocument

admin.site.register(CampusSystem)

@admin.register(PDFDocument)
class PDFDocumentAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "subject",
        "semester",
        "category",
        "academic_year",
        "uploaded_at",
    )

    search_fields = ("title", "subject")
    list_filter = ("semester", "category", "academic_year")

def save_model(self, request, obj, form, change):
    super().save_model(request, obj, form, change)

    if obj.file and (not obj.extracted_text or "file" in form.changed_data):
        extract_pdf_text(obj)

        if obj.extracted_text:
            messages.success(
                request,
                "PDF text extracted and summary generated."
            )
        else:
            messages.warning(
                request,
                "No text found. This PDF may contain scanned images."
            )