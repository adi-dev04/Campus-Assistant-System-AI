from django.db import models

class CampusSystem(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100,default='')
    email = models.EmailField(unique=True)
    enrollment_number = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    course = models.CharField(max_length=100)

    def __str__(self):
        return self.name + " (" + self.enrollment_number + ")"


from django.db import models


class PDFDocument(models.Model):
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    semester = models.CharField(max_length=20)
    category = models.CharField(max_length=100)
    academic_year = models.CharField(max_length=20)
    summary = models.TextField(blank=True)

    file = models.FileField(upload_to="pdfs/")
    extracted_text = models.TextField(blank=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

