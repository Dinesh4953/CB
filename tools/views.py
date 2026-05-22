from django.shortcuts import render
from django.http import FileResponse
from django.views.decorators.http import require_http_methods
import io

from .forms import (
    TextToPdfForm,
    PdfToTextForm,
    WordToPdfForm,
    PdfToWordForm,
    ImageToPdfForm,
    PdfToImageForm,
    ImageToTextForm,
    MergePdfForm
)

from .utils.converters import (
    TextToPdfConverter,
    PdfToTextConverter,
    WordToPdfConverter,
    PdfToWordConverter,
    ImageToPdfConverter,
    PdfToImageConverter,
    ImageToTextConverter,
    PdfMergeConverter
)


def index(request):
    """Home page with all tool options"""

    context = {
        'tools': [

            {
                'name': 'Text to PDF',
                'url': 'tools:text_to_pdf',
                'icon': '📄',
                'desc': 'Convert plain text to PDF'
            },

            {
                'name': 'PDF to Text',
                'url': 'tools:pdf_to_text',
                'icon': '📋',
                'desc': 'Extract text from PDF'
            },

            {
                'name': 'Word to PDF',
                'url': 'tools:word_to_pdf',
                'icon': '📑',
                'desc': 'Convert Word document to PDF'
            },

            {
                'name': 'PDF to Word',
                'url': 'tools:pdf_to_word',
                'icon': '📄',
                'desc': 'Convert PDF to Word document'
            },

            {
                'name': 'Image to PDF',
                'url': 'tools:image_to_pdf',
                'icon': '🖼️',
                'desc': 'Convert images to PDF'
            },

            {
                'name': 'PDF to Image',
                'url': 'tools:pdf_to_image',
                'icon': '🖼️',
                'desc': 'Convert PDF pages to images'
            },

            {
                'name': 'Image to Text (OCR)',
                'url': 'tools:image_to_text',
                'icon': '🔍',
                'desc': 'Extract text from images'
            },

            {
                'name': 'Merge PDFs',
                'url': 'tools:merge_pdf',
                'icon': '📚',
                'desc': 'Merge multiple PDF files'
            },
        ]
    }

    return render(request, 'tools/home.html', context)


@require_http_methods(["GET", "POST"])
def text_to_pdf(request):

    if request.method == 'POST':
        form = TextToPdfForm(request.POST)

        if form.is_valid():

            text_content = form.cleaned_data['text_content']
            title = form.cleaned_data.get('title')
            font_size = form.cleaned_data.get('font_size', 12)

            try:
                pdf_buffer = TextToPdfConverter.convert(
                    text_content=text_content,
                    title=title,
                    font_size=font_size
                )

                return FileResponse(
                    pdf_buffer,
                    as_attachment=True,
                    filename='document.pdf',
                    content_type='application/pdf'
                )

            except Exception as e:
                form.add_error(None, f"Error converting: {str(e)}")

    else:
        form = TextToPdfForm()

    return render(request, 'tools/text_to_pdf.html', {'form': form})


@require_http_methods(["GET", "POST"])
def pdf_to_text(request):

    if request.method == 'POST':

        form = PdfToTextForm(request.POST, request.FILES)

        if form.is_valid():

            pdf_file = request.FILES['pdf_file']

            try:
                text_content = PdfToTextConverter.convert(pdf_file)

                return FileResponse(
                    io.BytesIO(text_content.encode('utf-8')),
                    as_attachment=True,
                    filename='extracted_text.txt',
                    content_type='text/plain'
                )

            except Exception as e:
                form.add_error(None, f"Error converting: {str(e)}")

    else:
        form = PdfToTextForm()

    return render(request, 'tools/pdf_to_text.html', {'form': form})


@require_http_methods(["GET", "POST"])
def word_to_pdf(request):

    if request.method == 'POST':

        form = WordToPdfForm(request.POST, request.FILES)

        if form.is_valid():

            word_file = request.FILES['word_file']

            try:
                pdf_buffer = WordToPdfConverter.convert(word_file)

                return FileResponse(
                    pdf_buffer,
                    as_attachment=True,
                    filename='document.pdf',
                    content_type='application/pdf'
                )

            except Exception as e:
                form.add_error(None, f"Error converting: {str(e)}")

    else:
        form = WordToPdfForm()

    return render(request, 'tools/word_to_pdf.html', {'form': form})


@require_http_methods(["GET", "POST"])
def pdf_to_word(request):

    if request.method == 'POST':

        form = PdfToWordForm(request.POST, request.FILES)

        if form.is_valid():

            pdf_file = request.FILES['pdf_file']

            try:
                docx_buffer = PdfToWordConverter.convert(pdf_file)

                return FileResponse(
                    docx_buffer,
                    as_attachment=True,
                    filename='document.docx',
                    content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                )

            except Exception as e:
                form.add_error(None, f"Error converting: {str(e)}")

    else:
        form = PdfToWordForm()

    return render(request, 'tools/pdf_to_word.html', {'form': form})


@require_http_methods(["GET", "POST"])
def image_to_pdf(request):

    if request.method == 'POST':

        form = ImageToPdfForm(request.POST, request.FILES)

        if form.is_valid():

            image_files = form.cleaned_data['image_files']
            orientation = form.cleaned_data.get('orientation', 'portrait')

            try:
                image_bytes = [img.read() for img in image_files]

                pdf_buffer = ImageToPdfConverter.convert(
                    image_files=image_bytes,
                    orientation=orientation
                )

                return FileResponse(
                    pdf_buffer,
                    as_attachment=True,
                    filename='images.pdf',
                    content_type='application/pdf'
                )

            except Exception as e:
                form.add_error(None, f"Error converting: {str(e)}")

    else:
        form = ImageToPdfForm()

    return render(request, 'tools/image_to_pdf.html', {'form': form})


@require_http_methods(["GET", "POST"])
def pdf_to_image(request):

    if request.method == 'POST':

        form = PdfToImageForm(request.POST, request.FILES)

        if form.is_valid():

            pdf_file = request.FILES['pdf_file']
            format_choice = form.cleaned_data.get('format', 'PNG')
            dpi = form.cleaned_data.get('dpi', 200)

            try:
                image_buffers = PdfToImageConverter.convert(
                    pdf_file=pdf_file,
                    format=format_choice,
                    dpi=dpi
                )

                if len(image_buffers) == 1:

                    return FileResponse(
                        image_buffers[0],
                        as_attachment=True,
                        filename=f'page_1.{format_choice.lower()}',
                        content_type=f'image/{format_choice.lower()}'
                    )

                else:
                    import zipfile

                    zip_buffer = io.BytesIO()

                    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:

                        for idx, img_buffer in enumerate(image_buffers, 1):

                            zip_file.writestr(
                                f'page_{idx}.{format_choice.lower()}',
                                img_buffer.getvalue()
                            )

                    zip_buffer.seek(0)

                    return FileResponse(
                        zip_buffer,
                        as_attachment=True,
                        filename='pdf_pages.zip',
                        content_type='application/zip'
                    )

            except Exception as e:
                form.add_error(None, f"Error converting: {str(e)}")

    else:
        form = PdfToImageForm()

    return render(request, 'tools/pdf_to_image.html', {'form': form})


@require_http_methods(["GET", "POST"])
def image_to_text(request):

    if request.method == 'POST':

        form = ImageToTextForm(request.POST, request.FILES)

        if form.is_valid():

            image_file = request.FILES['image_file']

            try:
                text_content = ImageToTextConverter.convert(image_file)

                return FileResponse(
                    io.BytesIO(text_content.encode('utf-8')),
                    as_attachment=True,
                    filename='extracted_text.txt',
                    content_type='text/plain'
                )

            except Exception as e:
                form.add_error(None, f"Error extracting text: {str(e)}")

    else:
        form = ImageToTextForm()

    return render(request, 'tools/image_to_text.html', {'form': form})


@require_http_methods(["GET", "POST"])
def merge_pdf(request):

    if request.method == 'POST':

        form = MergePdfForm(request.POST, request.FILES)

        if form.is_valid():

            pdf_files = request.FILES.getlist('pdf_files')

            if len(pdf_files) < 2:

                form.add_error(
                    None,
                    "Please upload at least 2 PDF files to merge"
                )

            else:

                try:
                    pdf_buffer = PdfMergeConverter.merge(pdf_files)

                    return FileResponse(
                        pdf_buffer,
                        as_attachment=True,
                        filename='merged.pdf',
                        content_type='application/pdf'
                    )

                except Exception as e:
                    form.add_error(None, f"Error merging: {str(e)}")

    else:
        form = MergePdfForm()

    return render(request, 'tools/merge_pdf.html', {'form': form})