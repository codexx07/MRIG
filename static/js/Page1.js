const customCursor = document.querySelector('.custom-cursor');
const cursorInner = document.querySelector('.cursor-inner');

document.addEventListener('mousemove', (e) => {
  const x = e.clientX;
  const y = e.clientY;

  customCursor.style.transform = `translate(${x}px, ${y}px)`;
  cursorInner.style.transform = 'translate(-50%, -50%)';
});

function showImage() {
  var imgField = document.getElementById("imgField");
  var target = document.getElementById("target");
  
  target.innerText = "File uploaded"
  target.classList.add("uploaded-button");
}
