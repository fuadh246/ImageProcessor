from PIL import Image
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.conf import settings
from .forms import ImageUploadForm
from .filters import apply_gray_filter, apply_sepia_filter, apply_blur_filter
import boto3
import io

# AWS S3 Setup
s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
BUCKET_NAME = settings.AWS_STORAGE_BUCKET_NAME

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            image_name = image.name

            # Upload original image to S3
            s3.upload_fileobj(image, BUCKET_NAME, f'original/{image_name}')

            return redirect('select_filter', image_name=image_name)
    else:
        form = ImageUploadForm()
    return render(request, 'upload.html', {'form': form})

def select_filter(request, image_name):
    if request.method == 'POST':
        filter_type = request.POST.get('filter')

        # Download the image from S3
        image_obj = s3.get_object(Bucket=BUCKET_NAME, Key=f'original/{image_name}')
        image = Image.open(image_obj['Body'])
        image = image.convert('RGB')  # Ensure the image is in a proper format to apply filters

        # Apply the selected filter
        if filter_type == 'gray':
            processed_image = apply_gray_filter(image)
        elif filter_type == 'sepia':
            processed_image = apply_sepia_filter(image)
        elif filter_type == 'blur':
            processed_image = apply_blur_filter(image)
        else:
            processed_image = image

        # Save processed image to a BytesIO object
        processed_image_io = io.BytesIO()
        processed_image.save(processed_image_io, format='JPEG')
        processed_image_io.seek(0)

        # Upload processed image to S3
        processed_image_name = f'processed_{filter_type}_{image_name}'
        s3.upload_fileobj(processed_image_io, BUCKET_NAME, f'processed/{processed_image_name}')
        
        return redirect('view_image', image_name=processed_image_name)

    return render(request, 'select_filter.html', {'image_name': image_name})

def view_image(request, image_name):
    image_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/processed/{image_name}"
    return render(request, 'view_image.html', {'image_url': image_url})

