const fs = require('fs');
fetch('https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js')
.then(res => res.text())
.then(text => {
    console.log(text.includes('renderTextLayer'));
});
