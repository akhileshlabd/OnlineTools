export class AkinatorUI {
    constructor(engine) {
        this.engine = engine;
        
        this.ui = {
            loading: document.getElementById('loadingState'),
            question: document.getElementById('questionState'),
            guess: document.getElementById('guessState'),
            learn: document.getElementById('learnState'),
            
            qText: document.getElementById('questionText'),
            qCount: document.getElementById('questionCount'),
            undoBtn: document.getElementById('undoBtn'),
            
            confText: document.getElementById('confidenceText'),
            confBar: document.getElementById('confidenceBar'),
            
            gName: document.getElementById('guessName'),
            gImg: document.getElementById('guessImage'),
            
            btnYes: document.getElementById('btnGuessYes'),
            btnNo: document.getElementById('btnGuessNo'),
            
            ansBtns: document.querySelectorAll('.ans-btn'),
            
            learnName: document.getElementById('learnName'),
            learnTrait: document.getElementById('learnTrait'),
            btnLearnSubmit: document.getElementById('btnLearnSubmit')
        };
        
        this.currentQuestion = null;
        this.bindEvents();
    }

    async initGame(jsonUrl) {
        this.show(this.ui.loading);
        
        const progressBar = document.getElementById('loadingProgressBar');
        const statusText = document.getElementById('loadingStatusText');
        
        let progress = 0;
        // Simulate a smooth progression to accommodate future large datasets
        const progressInterval = setInterval(() => {
            progress += Math.floor(Math.random() * 15) + 5;
            if (progress > 90) progress = 90; // Hold at 90% until fetch finishes
            
            if (progressBar && statusText) {
                progressBar.style.width = progress + '%';
                statusText.textContent = `Processing Data: ${progress}%`;
            }
        }, 150);

        try {
            await this.engine.init(jsonUrl);
            
            // Finish the progress bar
            clearInterval(progressInterval);
            if (progressBar && statusText) {
                progressBar.style.width = '100%';
                statusText.textContent = 'Brain Loaded! 100%';
            }
            
            // Brief pause to let user see 100% completion
            setTimeout(() => {
                this.nextTurn();
            }, 600);
            
        } catch (err) {
            clearInterval(progressInterval);
            if (statusText) {
                statusText.textContent = 'Error loading data. Please refresh.';
                statusText.classList.replace('text-muted', 'text-danger');
            }
            console.error(err);
        }
    }

    show(el) {
        [this.ui.loading, this.ui.question, this.ui.guess, this.ui.learn].forEach(x => {
            if (x === el) x.style.setProperty('display', 'flex', 'important');
            else x.style.setProperty('display', 'none', 'important');
        });
    }

    updateConfidence() {
        const conf = this.engine.getConfidence();
        this.ui.confText.textContent = Math.round(conf) + '%';
        this.ui.confBar.style.width = conf + '%';
    }
    
    formatQuestion(qStr) {
        let result = qStr.replace(/([A-Z])/g, " $1");
        result = result.charAt(0).toUpperCase() + result.slice(1);
        
        if (qStr.startsWith('is')) return qStr.replace('is', 'Is (a/an) ') + '?';
        if (qStr.startsWith('has')) return qStr.replace('has', 'Does your character have ') + '?';
        if (qStr.startsWith('wears')) return qStr.replace('wears', 'Does your character wear ') + '?';
        if (qStr.startsWith('lives')) return qStr.replace('lives', 'Does your character live ') + '?';
        
        return "Does your character " + result.toLowerCase() + "?";
    }

    nextTurn() {
        const conf = this.engine.getConfidence();
        
        if (conf > 85 || this.engine.askedQuestions.length > 20) {
            this.makeGuess();
            return;
        }

        this.currentQuestion = this.engine.getBestQuestion();
        
        if (!this.currentQuestion) {
            this.makeGuess();
            return;
        }

        this.ui.qText.textContent = this.formatQuestion(this.currentQuestion);
        this.ui.qCount.textContent = `Question ${this.engine.askedQuestions.length + 1}`;
        this.ui.undoBtn.disabled = this.engine.askedQuestions.length === 0;
        
        this.updateConfidence();
        this.show(this.ui.question);
    }

    makeGuess() {
        const topChar = this.engine.getTopCandidate();
        this.ui.gName.textContent = topChar.name;
        this.ui.gImg.textContent = topChar.image || "🤔";
        this.show(this.ui.guess);
    }

    bindEvents() {
        this.ui.ansBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const weight = parseFloat(btn.getAttribute('data-weight'));
                this.engine.answer(this.currentQuestion, weight);
                this.nextTurn();
            });
        });

        this.ui.undoBtn.addEventListener('click', () => {
            if (this.engine.undo()) {
                this.nextTurn();
            }
        });

        this.ui.btnYes.addEventListener('click', () => {
            Swal.fire({
                title: 'I knew it!',
                text: 'I can read your mind. Play again?',
                icon: 'success',
                confirmButtonText: 'Play Again'
            }).then(() => {
                this.engine.resetGame();
                this.nextTurn();
            });
        });

        this.ui.btnNo.addEventListener('click', () => {
            this.show(this.ui.learn);
        });

        this.ui.btnLearnSubmit.addEventListener('click', () => {
            const name = this.ui.learnName.value.trim();
            let trait = this.ui.learnTrait.value.trim();
            
            if (!name || !trait) {
                Swal.fire('Wait!', 'Please fill out both fields so I can learn.', 'warning');
                return;
            }
            
            trait = trait.replace(/(?:^\w|[A-Z]|\b\w)/g, function(word, index) {
                return index === 0 ? word.toLowerCase() : word.toUpperCase();
            }).replace(/\s+/g, '');

            this.engine.learnCharacter(name, trait);
            
            Swal.fire('Thanks!', 'I have learned a new character.', 'success').then(() => {
                this.ui.learnName.value = '';
                this.ui.learnTrait.value = '';
                this.engine.resetGame();
                this.nextTurn();
            });
        });
    }
}
