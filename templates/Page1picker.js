// Get the file input and picker button elements
var fileInput = document.getElementById('fileInput');
var filePickerButton = document.getElementById('filePickerButton');

// Add event listener to the picker button
filePickerButton.addEventListener('click', function () {
    // Trigger the file input click event
    fileInput.click();
});

// Optional: Add change event listener to the file input to handle file selection
fileInput.addEventListener('change', function () {
    // You can access the selected file(s) via 'fileInput.files'
    var files = fileInput.files;
    if(files.length > 0) {
        console.log("File selected:", files[0].name);
        // Handle the file upload or processing here
    }
});