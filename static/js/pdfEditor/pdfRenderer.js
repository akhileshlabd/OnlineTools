class PDFRenderer {
    constructor(containerId, thumbnailContainerId) {
        this.container = document.getElementById(containerId);
        this.thumbContainer = document.getElementById(thumbnailContainerId);
        this.pdfDoc = null;
        this.pdfBytes = null;
        this.scale = 1.5;
        this.pages = []; // { pageNum, pdfPage, viewport, canvas, textLayer }
    }

    async loadDocument(file) {
        this.pdfBytes = await file.arrayBuffer();
        this.pdfDoc = await pdfjsLib.getDocument({ data: this.pdfBytes.slice(0) }).promise;
        this.container.innerHTML = '';
        this.thumbContainer.innerHTML = '';
        this.pages = [];

        for (let i = 1; i <= this.pdfDoc.numPages; i++) {
            await this.renderPage(i);
        }
        return this.pdfDoc.numPages;
    }

    async renderPage(pageNum) {
        const page = await this.pdfDoc.getPage(pageNum);
        const viewport = page.getViewport({ scale: this.scale });
        
        // Main wrapper
        const wrapper = document.createElement('div');
        wrapper.className = 'pdf-page-wrapper';
        wrapper.dataset.page = pageNum;
        wrapper.style.width = viewport.width + 'px';
        wrapper.style.height = viewport.height + 'px';

        // Canvas for PDF render
        const canvas = document.createElement('canvas');
        canvas.className = 'pdf-render-canvas';
        canvas.width = viewport.width;
        canvas.height = viewport.height;
        const ctx = canvas.getContext('2d');
        
        await page.render({ canvasContext: ctx, viewport }).promise;

        // Text layer for extracting text and enabling patching
        const textLayerDiv = document.createElement('div');
        textLayerDiv.className = 'pdf-text-layer';
        textLayerDiv.style.width = viewport.width + 'px';
        textLayerDiv.style.height = viewport.height + 'px';
        
        const textContent = await page.getTextContent();
        
        // Cluster text items into lines (rows)
        const lines = [];
        for (const item of textContent.items) {
            // PDF.js transform: [scaleX, skewY, skewX, scaleY, tx, ty]
            const tx = item.transform[4] * this.scale;
            const ty = viewport.height - (item.transform[5] * this.scale); // Invert Y
            const fontSize = Math.sqrt(item.transform[0] * item.transform[0] + item.transform[1] * item.transform[1]) * this.scale;
            const width = item.width * this.scale;
            
            // Skip empty items but keep spaces
            if (item.str.trim() === '' && item.str.length === 0) continue; 

            let foundLine = null;
            for (const line of lines) {
                // Group if Y-coordinate is within 30% of the font size (same row)
                if (Math.abs(line.ty - ty) < fontSize * 0.3) {
                    foundLine = line;
                    break;
                }
            }
            
            if (foundLine) {
                foundLine.items.push({ str: item.str, tx, ty, width, fontSize, fontName: item.fontName });
            } else {
                lines.push({
                    ty: ty,
                    items: [{ str: item.str, tx, ty, width, fontSize, fontName: item.fontName }]
                });
            }
        }
        
        // Render clustered lines
        for (const line of lines) {
            // Sort items in this row from left to right
            line.items.sort((a, b) => a.tx - b.tx);
            
            let combinedStr = '';
            let minX = line.items[0].tx;
            let maxX = minX;
            let maxFontSize = 0;
            let fontName = line.items[0].fontName;
            
            let lastItem = null;
            for (const item of line.items) {
                if (lastItem) {
                    // Add space if there's a significant visual gap between fragments
                    const gap = item.tx - (lastItem.tx + lastItem.width);
                    if (gap > item.fontSize * 0.2 && !lastItem.str.endsWith(' ') && !item.str.startsWith(' ')) {
                        combinedStr += ' ';
                    }
                }
                combinedStr += item.str;
                maxX = Math.max(maxX, item.tx + item.width);
                maxFontSize = Math.max(maxFontSize, item.fontSize);
                lastItem = item;
            }
            
            // Skip purely empty lines
            if (combinedStr.trim() === '') continue;

            const span = document.createElement('span');
            span.textContent = combinedStr;
            span.style.left = minX + 'px';
            span.style.top = (line.ty - maxFontSize) + 'px';
            span.style.width = (maxX - minX) + 'px';
            span.style.height = (maxFontSize * 1.2) + 'px'; // 1.2 line height for better bounding box
            span.style.fontSize = maxFontSize + 'px';
            span.style.fontFamily = fontName || 'sans-serif';
            span.style.lineHeight = '1.2';
            span.style.display = 'block'; // Ensure width/height are respected
            
            textLayerDiv.appendChild(span);
        }

        // Overlay for Fabric.js (handled by EditorUI)
        const overlayCanvas = document.createElement('canvas');
        overlayCanvas.className = 'pdf-fabric-canvas';
        overlayCanvas.id = `fabric-page-${pageNum}`;
        overlayCanvas.width = viewport.width;
        overlayCanvas.height = viewport.height;

        wrapper.appendChild(canvas);
        wrapper.appendChild(textLayerDiv);
        wrapper.appendChild(overlayCanvas);
        this.container.appendChild(wrapper);

        // Thumbnail
        this.renderThumbnail(page, pageNum);

        this.pages.push({
            pageNum,
            viewport,
            originalWidth: viewport.width / this.scale,
            originalHeight: viewport.height / this.scale
        });
    }

    async renderThumbnail(page, pageNum) {
        const thumbScale = 0.2;
        const viewport = page.getViewport({ scale: thumbScale });
        const canvas = document.createElement('canvas');
        canvas.width = viewport.width;
        canvas.height = viewport.height;
        canvas.className = 'pdf-thumb-canvas';
        canvas.onclick = () => {
            document.querySelector(`.pdf-page-wrapper[data-page="${pageNum}"]`).scrollIntoView({ behavior: 'smooth' });
        };
        await page.render({ canvasContext: canvas.getContext('2d'), viewport }).promise;
        
        const wrap = document.createElement('div');
        wrap.className = 'thumb-wrap';
        wrap.appendChild(canvas);
        const lbl = document.createElement('div');
        lbl.textContent = pageNum;
        wrap.appendChild(lbl);
        this.thumbContainer.appendChild(wrap);
    }
}
window.PDFRenderer = PDFRenderer;

