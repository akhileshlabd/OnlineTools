const form = document.getElementById('resize-form');
const imageInput = document.getElementById('image');
const widthInput = document.getElementById('width');
const heightInput = document.getElementById('height');
const keepRatioCheckbox = document.getElementById('keep_ratio');
const previewContainer = document.getElementById('preview-container');
const originalPreview = document.getElementById('original-preview');
const resizedPreview = document.getElementById('resized-preview');
const downloadLink = document.getElementById('download-link');

let originalImage = new Image();

imageInput.addEventListener('change', e => {
  const file = e.target.files[0];
  if (!file) return;

  const url = URL.createObjectURL(file);
  originalPreview.src = url;
  previewContainer.classList.remove('d-none');

  originalImage.onload = () => {
    widthInput.value = originalImage.width;
    heightInput.value = originalImage.height;
  };
  originalImage.src = url;
});

let isSyncing = false;
keepRatioCheckbox.addEventListener('change', () => {
  if (keepRatioCheckbox.checked) {
    syncDimensions();
  }
});

function syncDimensions() {
  if (isSyncing) return;
  isSyncing = true;
  const ratio = originalImage.width / originalImage.height;

  widthInput.oninput = () => {
    if (keepRatioCheckbox.checked) {
      heightInput.value = Math.round(widthInput.value / ratio);
    }
  };

  heightInput.oninput = () => {
    if (keepRatioCheckbox.checked) {
      widthInput.value = Math.round(heightInput.value * ratio);
    }
  };
  isSyncing = false;
}
syncDimensions();

form.addEventListener('submit', async e => {
  e.preventDefault();

  if (!imageInput.files[0]) {
    alert('Please upload an image!');
    return;
  }

  const formData = new FormData(form);
  formData.set('keep_ratio', keepRatioCheckbox.checked);

  try {
    const response = await fetch('/resize', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const err = await response.json();
      alert('Error: ' + err.error);
      return;
    }

    const blob = await response.blob();
    const resizedURL = URL.createObjectURL(blob);

    resizedPreview.src = resizedURL;
    downloadLink.href = resizedURL;
    downloadLink.download = 'resized_' + imageInput.files[0].name;

  } catch (error) {
    alert('Something went wrong: ' + error.message);
  }
});
