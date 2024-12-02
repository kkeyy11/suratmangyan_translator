const video = document.getElementById('camera');
const captureButton = document.getElementById('captureButton');
const captureCanvas = document.getElementById('captureCanvas');
const imageInput = document.getElementById('image');
const preview = document.getElementById('preview');

// Access the user's webcam
navigator.mediaDevices.getUserMedia({ video: true })
    .then((stream) => {
        video.srcObject = stream;
    })
    .catch((error) => {
        console.error("Error accessing camera:", error);
        video.textContent = "Camera access is not available.";
    });

// Capture image from camera feed
captureButton.addEventListener('click', () => {
    const context = captureCanvas.getContext('2d');
    captureCanvas.width = video.videoWidth;
    captureCanvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, captureCanvas.width, captureCanvas.height);

    // Convert the captured image to a data URL
    const capturedImage = captureCanvas.toDataURL('image/png');

    // Set the preview image to the captured image
    preview.src = capturedImage;
    preview.style.display = "block";

    // Add the captured image to the form data for submission
    const blob = dataURLtoBlob(capturedImage);
    const file = new File([blob], 'captured.png', { type: 'image/png' });
    const dataTransfer = new DataTransfer();
    dataTransfer.items.add(file);
    imageInput.files = dataTransfer.files;

    console.log("Image captured successfully!");
});

// Helper function to convert Data URL to Blob
function dataURLtoBlob(dataURL) {
    const parts = dataURL.split(',');
    const byteString = atob(parts[1]);
    const mimeString = parts[0].split(':')[1].split(';')[0];

    const arrayBuffer = new ArrayBuffer(byteString.length);
    const uint8Array = new Uint8Array(arrayBuffer);
    for (let i = 0; i < byteString.length; i++) {
        uint8Array[i] = byteString.charCodeAt(i);
    }

    return new Blob([arrayBuffer], { type: mimeString });
}

// Preview uploaded image
imageInput.addEventListener('change', () => {
    const file = imageInput.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            preview.src = e.target.result;
            preview.style.display = "block";
        };
        reader.readAsDataURL(file);
    } else {
        preview.style.display = "none";
    }
});

// Handle form submission
document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);

    try {
        const response = await fetch("", {
            method: "POST",
            body: formData,
        });
        const data = await response.json();
        document.getElementById('output').textContent = data.translated_text || data.error;
    } catch (error) {
        document.getElementById('output').textContent = `Error: ${error.message}`;
    }
});
