import re

with open('static/js/akinatorEngine.js', 'r') as f:
    content = f.read()

# 1. Update getBestQuestion to use Split Quality + Coverage
old_bestQ = """    getBestQuestion() {
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
    }"""

new_bestQ = """    getBestQuestion() {
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
    }"""

# 2. Update Probabilities to be fuzzy and forgiving
old_prob = """    updateProbabilities() {
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
    }"""

new_prob = """    updateProbabilities() {
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
    }"""

content = content.replace(old_bestQ, new_bestQ)
content = content.replace(old_prob, new_prob)

with open('static/js/akinatorEngine.js', 'w') as f:
    f.write(content)

