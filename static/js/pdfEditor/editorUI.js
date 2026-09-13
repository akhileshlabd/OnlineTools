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
            if (this.activeTool === 'select' || this.activeTool === 'draw') return;
            const pt = fc.getPointer(o.e);
            
            if (this.activeTool === 'text') {
                const t = new fabric.IText('New Text', {
                    left: pt.x, top: pt.y,
                    fontFamily: 'Arial', fontSize: 20, fill: '#000000',
                    editable: true
                });
                fc.add(t);
                fc.setActiveObject(t);
                t.enterEditing();
                this.setTool('select'); // revert to select
                return;
            }

            if (['whiteout', 'rect', 'ellipse'].includes(this.activeTool)) {
                isDrawing = true;
                startPt = pt;
                if (this.activeTool === 'whiteout') {
                    tempShape = new fabric.Rect({ left: pt.x, top: pt.y, width: 0, height: 0, fill: '#ffffff', selectable: false });
                } else if (this.activeTool === 'rect') {
                    tempShape = new fabric.Rect({ left: pt.x, top: pt.y, width: 0, height: 0, fill: 'transparent', stroke: '#000000', strokeWidth: 2, selectable: false });
                } else if (this.activeTool === 'ellipse') {
                    tempShape = new fabric.Ellipse({ left: pt.x, top: pt.y, rx: 0, ry: 0, fill: 'transparent', stroke: '#000000', strokeWidth: 2, selectable: false });
                }
                fc.add(tempShape);
            }
        });

        fc.on('mouse:move', (o) => {
            if (!isDrawing || !tempShape) return;
            const pt = fc.getPointer(o.e);
            const w = Math.abs(pt.x - startPt.x);
            const h = Math.abs(pt.y - startPt.y);
            const l = Math.min(pt.x, startPt.x);
            const t = Math.min(pt.y, startPt.y);
            
            if (this.activeTool === 'ellipse') {
                tempShape.set({ left: l, top: t, rx: w/2, ry: h/2 });
            } else {
                tempShape.set({ left: l, top: t, width: w, height: h });
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
        // Text patching workflow
        document.querySelectorAll('.pdf-text-layer span').forEach(span => {
            span.style.cursor = 'text';
            span.addEventListener('click', (e) => {
                if (this.activeTool !== 'select') return;
                const rect = span.getBoundingClientRect();
                const wrapper = span.closest('.pdf-page-wrapper');
                const wrapperRect = wrapper.getBoundingClientRect();
                const pageNum = parseInt(wrapper.dataset.page);
                
                // Calculate position relative to the canvas
                const x = rect.left - wrapperRect.left;
                const y = rect.top - wrapperRect.top;
                const w = rect.width;
                const h = rect.height;

                // 1. Record the whiteout patch for the engine
                this.patches[pageNum].push({ x, y, w, h });
                
                // 2. Hide original text visually in DOM
                span.style.opacity = '0';
                
                // 3. Add editable fabric text directly over it
                const fc = this.fabricCanvases[pageNum - 1];
                
                // Add a visual white background to the fabric canvas to hide it in UI immediately
                const whiteBg = new fabric.Rect({
                    left: x, top: y, width: w, height: h, fill: '#ffffff', selectable: false
                });
                fc.add(whiteBg);

                const t = new fabric.IText(span.textContent, {
                    left: x, top: y,
                    fontFamily: span.style.fontFamily || 'Arial',
                    fontSize: parseFloat(span.style.fontSize) || 16,
                    fill: span.style.color || '#000000',
                    editable: true
                });
                fc.add(t);
                fc.setActiveObject(t);
                t.enterEditing();
                t.selectAll();
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
            } catch (e) {
                console.error(e);
                alert('Error generating PDF');
            }
            this.hideLoading();
        });
    }

    setTool(tool) {
        this.activeTool = tool;
        document.querySelectorAll('[data-tool]').forEach(b => b.classList.toggle('active', b.dataset.tool === tool));
        this.fabricCanvases.forEach(fc => {
            fc.isDrawingMode = (tool === 'draw');
            fc.selection = (tool === 'select');
        });
    }
    
    showLoading() { document.getElementById('loadingOverlay').style.display = 'flex'; }
    hideLoading() { document.getElementById('loadingOverlay').style.display = 'none'; }
}
window.EditorUI = EditorUI;

