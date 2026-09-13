class EditorUI {
    constructor(renderer, engine) {
        this.renderer = renderer;
        this.engine = engine;
        this.fabricCanvases = [];
        this.activeTool = 'select';
        this.patches = {}; // pageNum -> array of patches
        
        this.setupToolbar();
    }

    initFabricCanvases(numPages) {
        this.fabricCanvases = [];
        this.patches = {};
        for (let i = 1; i <= numPages; i++) {
            const el = document.getElementById(`fabric-page-${i}`);
            const fc = new fabric.Canvas(el, { selection: true });
            this.fabricCanvases.push(fc);
            this.patches[i] = [];
            this.bindCanvasEvents(fc, i);
        }
        this.bindTextLayerEvents();
    }

    bindCanvasEvents(fc, pageNum) {
        let isDrawing = false;
        let startPt = null;
        let tempShape = null;

        fc.on('mouse:down', (o) => {
            if (this.activeTool === 'select' || this.activeTool === 'draw' || this.activeTool === 'text') return;
            const pt = fc.getPointer(o.e);

            if (['whiteout', 'rect', 'ellipse', 'line'].includes(this.activeTool)) {
                isDrawing = true;
                startPt = pt;
                
                const colorInput = document.getElementById('colorPicker');
                const strokeColor = colorInput ? colorInput.value : '#000000';
                const sizeInput = document.getElementById('sizePicker');
                const strokeW = sizeInput ? parseInt(sizeInput.value) : 2;

                if (this.activeTool === 'whiteout') {
                    tempShape = new fabric.Rect({ left: pt.x, top: pt.y, width: 0, height: 0, fill: '#ffffff', selectable: false });
                } else if (this.activeTool === 'rect') {
                    tempShape = new fabric.Rect({ left: pt.x, top: pt.y, width: 0, height: 0, fill: 'transparent', stroke: strokeColor, strokeWidth: strokeW, selectable: false });
                } else if (this.activeTool === 'ellipse') {
                    tempShape = new fabric.Ellipse({ left: pt.x, top: pt.y, rx: 0, ry: 0, fill: 'transparent', stroke: strokeColor, strokeWidth: strokeW, selectable: false });
                } else if (this.activeTool === 'line') {
                    tempShape = new fabric.Line([pt.x, pt.y, pt.x, pt.y], { stroke: strokeColor, strokeWidth: strokeW, selectable: false });
                }
                fc.add(tempShape);
            }
        });

        fc.on('mouse:move', (o) => {
            if (!isDrawing || !tempShape) return;
            const pt = fc.getPointer(o.e);
            if (this.activeTool === 'line') {
                tempShape.set({ x2: pt.x, y2: pt.y });
            } else {
                const w = Math.abs(pt.x - startPt.x);
                const h = Math.abs(pt.y - startPt.y);
                const l = Math.min(pt.x, startPt.x);
                const t = Math.min(pt.y, startPt.y);
                
                if (this.activeTool === 'ellipse') {
                    tempShape.set({ left: l, top: t, rx: w/2, ry: h/2 });
                } else {
                    tempShape.set({ left: l, top: t, width: w, height: h });
                }
            }
            fc.renderAll();
        });

        fc.on('mouse:up', () => {
            if (!isDrawing || !tempShape) return;
            isDrawing = false;
            tempShape.set({ selectable: true });
            fc.setActiveObject(tempShape);
            tempShape = null;
        });
    }

    bindTextLayerEvents() {
        document.querySelectorAll('.pdf-text-layer').forEach(layer => {
            layer.addEventListener('click', (e) => {
                if (this.activeTool !== 'text') return;
                
                const wrapper = layer.closest('.pdf-page-wrapper');
                const wrapperRect = wrapper.getBoundingClientRect();
                const pageNum = parseInt(wrapper.dataset.page);
                const fc = this.fabricCanvases[pageNum - 1];
                
                if (e.target.tagName === 'SPAN') {
                    // Inline editing (Patching)
                    const span = e.target;
                    const rect = span.getBoundingClientRect();
                    
                    const x = rect.left - wrapperRect.left;
                    const y = rect.top - wrapperRect.top;
                    const w = rect.width;
                    const h = rect.height;

                    // 1. Record the whiteout patch for the engine
                    this.patches[pageNum].push({ x, y, w, h });
                    
                    // 2. Hide original text visually in DOM
                    span.style.opacity = '0';
                    span.style.pointerEvents = 'none'; // Prevent double clicking
                    
                    // 3. Add visual white background to the fabric canvas to hide it in UI immediately
                    const whiteBg = new fabric.Rect({
                        left: x, top: y, width: w, height: h, fill: '#ffffff', selectable: false
                    });
                    fc.add(whiteBg);
                    
                    const colorInput = document.getElementById('colorPicker');
                    const textColor = colorInput ? colorInput.value : '#000000';

                    const t = new fabric.IText(span.textContent, {
                        left: x, top: y,
                        fontFamily: 'Arial',
                        fontSize: parseFloat(span.style.fontSize) || 16,
                        fill: textColor,
                        editable: true
                    });
                    fc.add(t);
                    fc.setActiveObject(t);
                    t.enterEditing();
                    t.selectAll();
                    this.setTool('select'); // revert to select to manipulate the text
                } else {
                    // Add new text at clicked coordinates
                    const x = e.clientX - wrapperRect.left;
                    const y = e.clientY - wrapperRect.top;
                    
                    const colorInput = document.getElementById('colorPicker');
                    const textColor = colorInput ? colorInput.value : '#000000';
                    
                    const t = new fabric.IText('New Text', {
                        left: x, top: y,
                        fontFamily: 'Arial', fontSize: 20, fill: textColor,
                        editable: true
                    });
                    fc.add(t);
                    fc.setActiveObject(t);
                    t.enterEditing();
                    t.selectAll();
                    this.setTool('select'); // revert to select
                }
            });
        });
    }

    setupToolbar() {
        document.querySelectorAll('[data-tool]').forEach(btn => {
            btn.addEventListener('click', () => this.setTool(btn.dataset.tool));
        });

        document.getElementById('btnDownload').addEventListener('click', async () => {
            this.showLoading();
            try {
                const pagesData = this.fabricCanvases.map((fc, i) => {
                    return {
                        patches: this.patches[i + 1] || [],
                        fabricDataURL: fc.getObjects().length > 0 ? fc.toDataURL({ format: 'png', multiplier: 1 }) : null
                    };
                });
                const outBytes = await this.engine.compilePDF(this.renderer.pdfBytes, pagesData, this.renderer.scale);
                const blob = new Blob([outBytes], { type: 'application/pdf' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'edited.pdf';
                a.click();
                URL.revokeObjectURL(url);
            } catch (e) {
                console.error(e);
                alert('Error generating PDF');
            }
            this.hideLoading();
        });

        // Properties bindings
        const btnDelete = document.getElementById('btnDelete');
        if (btnDelete) btnDelete.addEventListener('click', () => {
            this.fabricCanvases.forEach(fc => {
                const obj = fc.getActiveObject();
                if (obj) { fc.remove(obj); fc.discardActiveObject(); fc.renderAll(); }
            });
        });

        const colorPicker = document.getElementById('colorPicker');
        if (colorPicker) colorPicker.addEventListener('input', e => {
            const color = e.target.value;
            this.fabricCanvases.forEach(fc => {
                if (fc.freeDrawingBrush) fc.freeDrawingBrush.color = color;
                const obj = fc.getActiveObject();
                if (obj) {
                    if (obj.type === 'i-text' || obj.type === 'text') obj.set('fill', color);
                    else obj.set('stroke', color);
                    fc.renderAll();
                }
            });
        });

        const sizePicker = document.getElementById('sizePicker');
        if (sizePicker) sizePicker.addEventListener('input', e => {
            const sz = parseInt(e.target.value);
            this.fabricCanvases.forEach(fc => {
                if (fc.freeDrawingBrush) fc.freeDrawingBrush.width = sz;
                const obj = fc.getActiveObject();
                if (obj) {
                    if (obj.type === 'i-text' || obj.type === 'text') obj.set('fontSize', sz);
                    else obj.set('strokeWidth', sz);
                    fc.renderAll();
                }
            });
        });

        const fontFamily = document.getElementById('fontFamily');
        if (fontFamily) fontFamily.addEventListener('change', e => {
            this.fabricCanvases.forEach(fc => {
                const obj = fc.getActiveObject();
                if (obj && (obj.type === 'i-text' || obj.type === 'text')) {
                    obj.set('fontFamily', e.target.value);
                    fc.renderAll();
                }
            });
        });
        
        const btnNewFile = document.getElementById('btnNewFile');
        const pdfFileInput2 = document.getElementById('pdfFileInput2');
        if (btnNewFile && pdfFileInput2) {
            btnNewFile.addEventListener('click', () => pdfFileInput2.click());
            pdfFileInput2.addEventListener('change', (e) => {
                const file = e.target.files[0];
                if (file) {
                    document.getElementById('pdfFileInput').files = e.target.files;
                    document.getElementById('pdfFileInput').dispatchEvent(new Event('change'));
                }
            });
        }

        const btnUndo = document.getElementById('btnUndo');
        if (btnUndo) {
            btnUndo.addEventListener('click', () => {
                this.fabricCanvases.forEach(fc => {
                    const objs = fc.getObjects();
                    if(objs.length > 0) { fc.remove(objs[objs.length - 1]); }
                });
            });
        }

        const btnBold = document.getElementById('btnBold');
        if (btnBold) {
            btnBold.addEventListener('click', () => {
                btnBold.classList.toggle('active');
                const weight = btnBold.classList.contains('active') ? 'bold' : 'normal';
                this.fabricCanvases.forEach(fc => {
                    const obj = fc.getActiveObject();
                    if (obj) { obj.set('fontWeight', weight); fc.renderAll(); }
                });
            });
        }

        const btnItalic = document.getElementById('btnItalic');
        if (btnItalic) {
            btnItalic.addEventListener('click', () => {
                btnItalic.classList.toggle('active');
                const style = btnItalic.classList.contains('active') ? 'italic' : 'normal';
                this.fabricCanvases.forEach(fc => {
                    const obj = fc.getActiveObject();
                    if (obj) { obj.set('fontStyle', style); fc.renderAll(); }
                });
            });
        }

        const btnImage = document.querySelector('[data-tool="image"]');
        if (btnImage) {
            btnImage.addEventListener('click', () => {
                this.setTool('image');
                const imgInput = document.createElement('input');
                imgInput.type = 'file';
                imgInput.accept = 'image/*';
                imgInput.onchange = ev => {
                    const file = ev.target.files[0];
                    if (!file) return;
                    const reader = new FileReader();
                    reader.onload = e => {
                        fabric.Image.fromURL(e.target.result, img => {
                            img.scaleToWidth(200);
                            if (this.fabricCanvases.length > 0) {
                                img.set({ left: 50, top: 50 });
                                this.fabricCanvases[0].add(img);
                                this.fabricCanvases[0].setActiveObject(img);
                                this.fabricCanvases[0].renderAll();
                            }
                        });
                    };
                    reader.readAsDataURL(file);
                };
                imgInput.click();
            });
        }
    }

    setTool(tool) {
        this.activeTool = tool;
        document.querySelectorAll('[data-tool]').forEach(b => b.classList.toggle('active', b.dataset.tool === tool));
        this.fabricCanvases.forEach(fc => {
            fc.isDrawingMode = (tool === 'draw' || tool === 'highlight');
            fc.selection = (tool === 'select');
            
            if (fc.isDrawingMode) {
                const colorInput = document.getElementById('colorPicker');
                const sizeInput = document.getElementById('sizePicker');
                if (tool === 'highlight') {
                    fc.freeDrawingBrush.color = 'rgba(255, 255, 0, 0.4)';
                    fc.freeDrawingBrush.width = 24;
                } else {
                    fc.freeDrawingBrush.color = colorInput ? colorInput.value : '#000000';
                    fc.freeDrawingBrush.width = sizeInput ? parseInt(sizeInput.value) : 2;
                }
            }
        });
        
        // Allow clicking PDF text when tool is 'text'
        document.querySelectorAll('.pdf-text-layer').forEach(layer => {
            if (tool === 'text') {
                layer.style.zIndex = '3';
                layer.style.pointerEvents = 'auto';
            } else {
                layer.style.zIndex = '1';
                layer.style.pointerEvents = 'none';
            }
        });
    }
    
    showLoading() { document.getElementById('loadingOverlay').style.display = 'flex'; }
    hideLoading() { document.getElementById('loadingOverlay').style.display = 'none'; }
}
window.EditorUI = EditorUI;

