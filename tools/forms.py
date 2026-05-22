from django import forms
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError


# CUSTOM MULTIPLE FILE INPUT
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):

        if not data:
            raise ValidationError("Please upload at least one file.")

        if not isinstance(data, (list, tuple)):
            data = [data]

        cleaned_files = []

        for file in data:
            cleaned_files.append(super().clean(file, initial))

        return cleaned_files


class TextToPdfForm(forms.Form):
    """Form for converting text to PDF"""

    text_content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 10,
            'placeholder': 'Enter text content here...'
        }),
        label='Text Content',
        required=True
    )

    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter document title (optional)'
        }),
        label='Document Title',
        required=False
    )

    font_size = forms.IntegerField(
        initial=12,
        min_value=8,
        max_value=24,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'type': 'number'
        }),
        label='Font Size'
    )


class PdfToTextForm(forms.Form):
    """Form for extracting text from PDF"""

    pdf_file = forms.FileField(
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf'])
        ],
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf'
        }),
        label='Upload PDF',
        required=True
    )


class WordToPdfForm(forms.Form):
    """Form for converting Word to PDF"""

    word_file = forms.FileField(
        validators=[
            FileExtensionValidator(allowed_extensions=['docx', 'doc'])
        ],
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.docx,.doc'
        }),
        label='Upload Word Document',
        required=True
    )


class PdfToWordForm(forms.Form):
    """Form for converting PDF to Word"""

    pdf_file = forms.FileField(
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf'])
        ],
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf'
        }),
        label='Upload PDF',
        required=True
    )


class ImageToPdfForm(forms.Form):

    ORIENTATION_CHOICES = [
        ('portrait', 'Portrait'),
        ('landscape', 'Landscape'),
    ]

    image_files = MultipleFileField(
        widget=MultipleFileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*',
            'multiple': True
        }),
        label='Upload Images',
        required=True
    )

    orientation = forms.ChoiceField(
        choices=ORIENTATION_CHOICES,
        initial='portrait',
        widget=forms.RadioSelect,
        label='Page Orientation'
    )

    # def clean_image_files(self):

    #     files = self.files.getlist('image_files')

    #     if not files:
    #         raise ValidationError("Please upload at least one image.")

    #     allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp']

    #     for file in files:

    #         ext = file.name.split('.')[-1].lower()

    #         if ext not in allowed_extensions:
    #             raise ValidationError(
    #                 f"{file.name} is not a supported image file."
    #             )

    #     return files


class PdfToImageForm(forms.Form):
    """Form for converting PDF to images"""

    IMAGE_FORMAT_CHOICES = [
        ('PNG', 'PNG'),
        ('JPG', 'JPG/JPEG'),
        ('BMP', 'BMP'),
    ]

    pdf_file = forms.FileField(
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf'])
        ],
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf'
        }),
        label='Upload PDF',
        required=True
    )

    format = forms.ChoiceField(
        choices=IMAGE_FORMAT_CHOICES,
        initial='PNG',
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input'
        }),
        label='Image Format'
    )

    dpi = forms.IntegerField(
        initial=200,
        min_value=100,
        max_value=300,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'type': 'number'
        }),
        label='DPI (Quality)'
    )


class ImageToTextForm(forms.Form):
    """Form for extracting text from images (OCR)"""

    image_file = forms.FileField(
        validators=[
            FileExtensionValidator(
                allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'bmp']
            )
        ],
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        label='Upload Image',
        required=True
    )


class MergePdfForm(forms.Form):
    """Form for merging multiple PDFs"""

    pdf_files = MultipleFileField(
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf'])
        ],
        widget=MultipleFileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf',
            'multiple': True
        }),
        label='Upload PDFs to Merge',
        required=True
    )