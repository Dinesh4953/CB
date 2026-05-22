from django.urls import path
from . import views

app_name = 'tools'

urlpatterns = [

    path('', views.index, name='index'),

    path(
        'text-to-pdf/',
        views.text_to_pdf,
        name='text_to_pdf'
    ),

    path(
        'pdf-to-text/',
        views.pdf_to_text,
        name='pdf_to_text'
    ),

    path(
        'word-to-pdf/',
        views.word_to_pdf,
        name='word_to_pdf'
    ),

    path(
        'pdf-to-word/',
        views.pdf_to_word,
        name='pdf_to_word'
    ),

    path(
        'image-to-pdf/',
        views.image_to_pdf,
        name='image_to_pdf'
    ),

    path(
        'pdf-to-image/',
        views.pdf_to_image,
        name='pdf_to_image'
    ),

    path(
        'image-to-text/',
        views.image_to_text,
        name='image_to_text'
    ),

    path(
        'merge-pdf/',
        views.merge_pdf,
        name='merge_pdf'
    ),
]
# from django.urls import path
# from . import views

# app_name = 'tools'

# urlpatterns = [
#     path('', views.index, name='index'),

#     path('text-to-pdf/', views.text_to_pdf, name='text_to_pdf'),

#     path('pdf-to-text/', views.pdf_to_text, name='pdf_to_text'),

#     path('word-to-pdf/', views.word_to_pdf, name='word_to_pdf'),

#     path('pdf-to-word/', views.pdf_to_word, name='pdf_to_word'),

#     path('image-to-pdf/', views.image_to_pdf, name='image_to_pdf'),

#     path('pdf-to-image/', views.pdf_to_image, name='pdf_to_image'),

#     path('image-to-text/', views.image_to_text, name='image_to_text'),

#     path('merge-pdf/', views.merge_pdf, name='merge_pdf'),
# ]
