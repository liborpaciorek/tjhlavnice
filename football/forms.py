from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from .models import Gallery, GalleryAlbum, Event, BulkImageUpload
import os


class MultipleFileInput(forms.ClearableFileInput):
    """Custom widget for multiple file upload"""
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    """Custom field for handling multiple files"""
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class BulkImageUploadForm(forms.ModelForm):
    """Form for bulk image upload"""
    images = MultipleFileField(
        label="Obrázky",
        help_text="Vyberte více obrázků najednou (podržte Ctrl/Cmd pro výběr více souborů)",
        required=True
    )
    
    class Meta:
        model = BulkImageUpload
        fields = ['album', 'event', 'images', 'default_title_prefix']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['album'].required = True
        self.fields['images'].widget.attrs.update({
            'multiple': True,
            'accept': 'image/*',
            'class': 'bulk-image-upload'
        })

    def save(self, commit=True):
        """Override save to handle multiple images"""
        # Don't save the BulkImageUpload instance
        bulk_upload = super().save(commit=False)
        
        if commit:
            images = self.cleaned_data.get('images', [])
            if not isinstance(images, list):
                images = [images]
            
            created_galleries = []
            for i, image_file in enumerate(images, 1):
                if image_file:
                    # Create individual Gallery instances
                    gallery = Gallery(
                        title=f"{bulk_upload.default_title_prefix} {i}",
                        image=image_file,
                        album=bulk_upload.album,
                        event=bulk_upload.event
                    )
                    gallery.save()
                    created_galleries.append(gallery)
            
            return created_galleries
        
        return bulk_upload
