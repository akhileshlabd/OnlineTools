export class AkinatorEngine {
    constructor() {
        this.baseCandidates = [];
        this.candidates = [];
        this.allQuestions = new Set();
        this.askedQuestions = []; // Array of objects { q, weight }
    }

    async init(jsonPath) {
        // Load base dataset
        const res = await fetch(jsonPath);
        this.baseCandidates = await res.json();
        
        // Load learned dataset from localStorage
        const learned = JSON.parse(localStorage.getItem('akinator_learned') || '[]');
        this.candidates = [...this.baseCandidates, ...learned];
        
        this.resetGame();
    }

    resetGame() {
        this.askedQuestions = [];
        this.allQuestions = new Set();
        
        // Extract all possible traits from current active candidates
        this.candidates.forEach(c => {
            Object.keys(c.traits).forEach(q => this.allQuestions.add(q));
            c.currentScore = 0;
            c.active = true;
        });
    }

    getBestQuestion() {
        let bestQ = null;
        let bestScore = -Infinity; // Higher is better (Coverage + Entropy)

        const activeCandidates = this.candidates.filter(c => c.active);
        if (activeCandidates.length === 0) return null;
        
        const askedKeys = this.askedQuestions.map(a => a.q);

        for (const q of this.allQuestions) {
            if (askedKeys.includes(q)) continue;

            let yesCount = 0;
            let noCount = 0;

            for (const c of activeCandidates) {
                if (c.traits[q] === true) yesCount++;
                else if (c.traits[q] === false) noCount++;
            }

            const totalDefined = yesCount + noCount;
            // Skip questions that don't apply to any remaining candidates
            if (totalDefined === 0) continue;

            // Split Diff: 0 means perfectly split 50/50
            const diff = Math.abs(yesCount - noCount);
            
            // Normalize the split quality (1.0 = perfect 50/50 split)
            const splitQuality = 1.0 - (diff / totalDefined);
            
            // Normalize coverage (1.0 = trait is defined for 100% of active candidates)
            const coverage = totalDefined / activeCandidates.length;

            // Algorithm Core: High coverage (broad questions) early on, High split (narrow questions) later
            // We weight coverage slightly higher to ensure it doesn't ask obscure questions too early
            const qScore = (splitQuality * 0.4) + (coverage * 0.6);

            if (qScore > bestScore) {
                bestScore = qScore;
                bestQ = q;
            }
        }
        
        if (!bestQ) {
            for (const q of this.allQuestions) {
                if (!askedKeys.includes(q)) return q;
            }
        }
        
        return bestQ;
    }

    answer(question, weight) {
        this.askedQuestions.push({ q: question, weight: weight });
        this.updateProbabilities();
    }

    undo() {
        if (this.askedQuestions.length === 0) return false;
        this.askedQuestions.pop();
        this.updateProbabilities();
        return true;
    }

    updateProbabilities() {
        for (let c of this.candidates) {
            let score = 0;
            
            for (const ans of this.askedQuestions) {
                const hasTrait = c.traits[ans.q];
                
                // Robust Fuzzy Logic Scoring
                if (hasTrait === true) {
                    score += (ans.weight * 2.0); // Reward true matches heavily
                } else if (hasTrait === false) {
                    score -= (ans.weight * 2.0); // Penalize direct contradictions heavily
                } else {
                    // Trait is missing from dataset for this character.
                    // If user says "Yes" (weight > 0), we apply a minor penalty instead of a hard knockout
                    // If user says "No" (weight < 0), we apply a minor bonus (assume missing traits are generally false)
                    score -= (ans.weight * 0.5); 
                }
            }
            c.currentScore = score;
            
            // Dynamic Thresholding: Only deactivate characters if they are mathematically completely irredeemable
            const maxPossible = this.askedQuestions.length * 2.0;
            c.active = score > -(maxPossible * 0.65); 
        }

        this.candidates.sort((a, b) => b.currentScore - a.currentScore);
    }

    getTopCandidate() {
        return this.candidates[0];
    }
    
    getTopCandidates(n = 3) {
        return this.candidates.slice(0, n);
    }

    getConfidence() {
        const activeCount = this.candidates.filter(c => c.active).length;
        if (activeCount <= 1 && this.askedQuestions.length > 3) return 100;
        
        if (this.candidates.length < 2) return 100;
        
        const top = this.candidates[0].currentScore;
        const second = this.candidates[1].currentScore;
        
        const diff = top - second;
        
        // Base confidence grows with questions asked (up to 60%)
        const base = Math.min(this.askedQuestions.length * 4, 60); 
        // Diff adds up to 40%
        let conf = base + (diff * 10);
        
        if (conf > 99) conf = 99;
        if (conf < 0) conf = 0;
        
        return conf;
    }

    learnCharacter(name, distinguishingTrait) {
        // Save to local storage
        const learned = JSON.parse(localStorage.getItem('akinator_learned') || '[]');
        
        // Construct traits based on the game's asked questions
        let newTraits = {};
        for (const ans of this.askedQuestions) {
            if (ans.weight > 0.5) newTraits[ans.q] = true;
            else if (ans.weight < -0.5) newTraits[ans.q] = false;
        }
        
        // Add the distinguishing trait
        if (distinguishingTrait) {
            newTraits[distinguishingTrait] = true;
        }
        
        const newChar = {
            name: name,
            image: "🤔",
            traits: newTraits
        };
        
        learned.push(newChar);
        localStorage.setItem('akinator_learned', JSON.stringify(learned));
        
        // Add to current session
        this.candidates.push(newChar);
        this.allQuestions.add(distinguishingTrait);
    }
}
