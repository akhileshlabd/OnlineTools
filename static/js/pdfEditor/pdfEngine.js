class PDFEngine {
    constructor() {}

    async compilePDF(originalBytes, pagesData, scale) {
        const { PDFDocument, rgb } = PDFLib;
        const pdfDoc = await PDFDocument.load(originalBytes);
        const pdfPages = pdfDoc.getPages();

        for (let i = 0; i < pagesData.length; i++) {
            const pageData = pagesData[i];
            const pdfPage = pdfPages[i];
            const { width, height } = pdfPage.getSize();

            // Handle Text Patching (Whiteouts)
            for (const patch of pageData.patches) {
                // Coordinates need transformation from DOM to PDF
                // PDF origin is bottom-left
                const pdfX = patch.x / scale;
                const pdfY = height - (patch.y / scale) - (patch.h / scale);
                const pdfW = patch.w / scale;
                const pdfH = patch.h / scale;
                
                pdfPage.drawRectangle({
                    x: pdfX,
                    y: pdfY,
                    width: pdfW,
                    height: pdfH,
                    color: rgb(1, 1, 1) // Whiteout original text
                });
            }

            // Export Fabric canvas layer as PNG and overlay it
            if (pageData.fabricDataURL) {
                const pngBytes = this._dataURLToBytes(pageData.fabricDataURL);
                const pngImage = await pdfDoc.embedPng(pngBytes);
                pdfPage.drawImage(pngImage, {
                    x: 0,
                    y: 0,
                    width: width,
                    height: height
                });
            }
        }

        return await pdfDoc.save();
    }

    _dataURLToBytes(dataUrl) {
        const base64 = dataUrl.split(',')[1];
        const bin = atob(base64);
        const arr = new Uint8Array(bin.length);
        for (let i = 0; i < bin.length; i++) arr[i] = bin.charCodeAt(i);
        return arr;
    }
}
window.PDFEngine = PDFEngine;

