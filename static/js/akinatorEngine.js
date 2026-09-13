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
        let minEntropy = Infinity;

        // Shannon Entropy / Info Gain Approximation
        // We want a question that splits the active candidates as close to 50/50 as possible
        const activeCandidates = this.candidates.filter(c => c.active);
        
        if (activeCandidates.length === 0) return null;
        
        const askedKeys = this.askedQuestions.map(a => a.q);

        for (const q of this.allQuestions) {
            if (askedKeys.includes(q)) continue;

            let yesCount = 0;
            let noCount = 0;

            for (const c of activeCandidates) {
                if (c.traits[q]) yesCount++;
                else noCount++;
            }

            // If a question applies to all or none of the remaining, it's useless
            if (yesCount === 0 || noCount === 0) continue;

            const diff = Math.abs(yesCount - noCount);

            if (diff < minEntropy) {
                minEntropy = diff;
                bestQ = q;
            }
        }
        
        // Fallback if no perfect question found (e.g., all remaining traits are unique)
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
        // Recalculate scores from scratch based on all asked questions
        for (let c of this.candidates) {
            let score = 0;
            let possibleScore = 0;
            
            for (const ans of this.askedQuestions) {
                const charHasTrait = c.traits[ans.q] === true;
                const charDoesNotHaveTrait = c.traits[ans.q] === false;
                
                // If the trait is undefined for the character, we treat it neutrally or slightly negatively
                if (!charHasTrait && !charDoesNotHaveTrait) {
                    score += 0;
                } else {
                    const expected = charHasTrait ? 1 : -1;
                    score += ans.weight * expected;
                }
                possibleScore += Math.abs(ans.weight);
            }
            c.currentScore = score;
            c.active = possibleScore === 0 ? true : (score > -(possibleScore * 0.3)); 
            // Inactivate candidates that are wildly wrong to speed up entropy
        }

        // Sort by score
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
