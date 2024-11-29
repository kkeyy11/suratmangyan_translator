from django.shortcuts import render
from django.http import JsonResponse
from .models import UploadedImage
from .utils import predict_translation

def translate_image(request):
    if request.method == 'POST':
        # Handle uploaded image
        uploaded_image = request.FILES.get('image')
        if not uploaded_image:
            return JsonResponse({'error': 'No image uploaded'}, status=400)

        # Save the image
        img_instance = UploadedImage(image=uploaded_image)
        img_instance.save()

        # Perform translation
        try:
            translated_text = predict_translation(img_instance.image.path)
            return JsonResponse({'translated_text': translated_text})
        except Exception as e:
            return JsonResponse({'error': f"Prediction error: {str(e)}"}, status=500)

    # Render the upload form for GET requests
    return render(request, 'translator/translate.html')

#under development :<