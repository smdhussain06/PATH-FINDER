// Data Handler for PATH-FINDER
// Manages all data operations and localStorage

class DataHandler {
    constructor() {
        this.storageKeys = {
            userData: 'pathfinder_user_data',
            psychometric: 'pathfinder_psychometric',
            ikigai: 'pathfinder_ikigai',
            preferences: 'pathfinder_preferences',
            results: 'pathfinder_results'
        };
    }

    // Save user data
    saveUserData(data) {
        return Utils.storage.set(this.storageKeys.userData, {
            ...data,
            lastUpdated: Date.now()
        });
    }

    // Get user data
    getUserData() {
        return Utils.storage.get(this.storageKeys.userData);
    }

    // Save psychometric results
    savePsychometricResults(results) {
        return Utils.storage.set(this.storageKeys.psychometric, {
            ...results,
            completedAt: Date.now()
        });
    }

    // Get psychometric results
    getPsychometricResults() {
        return Utils.storage.get(this.storageKeys.psychometric);
    }

    // Save Ikigai analysis
    saveIkigaiAnalysis(analysis) {
        return Utils.storage.set(this.storageKeys.ikigai, {
            ...analysis,
            completedAt: Date.now()
        });
    }

    // Get Ikigai analysis
    getIkigaiAnalysis() {
        return Utils.storage.get(this.storageKeys.ikigai);
    }

    // Save user preferences
    savePreferences(preferences) {
        return Utils.storage.set(this.storageKeys.preferences, {
            ...preferences,
            updatedAt: Date.now()
        });
    }

    // Get user preferences
    getPreferences() {
        return Utils.storage.get(this.storageKeys.preferences);
    }

    // Save career matching results
    saveCareerResults(results) {
        return Utils.storage.set(this.storageKeys.results, {
            ...results,
            generatedAt: Date.now()
        });
    }

    // Get career matching results
    getCareerResults() {
        return Utils.storage.get(this.storageKeys.results);
    }

    // Get complete user profile
    getCompleteProfile() {
        return {
            userData: this.getUserData(),
            psychometric: this.getPsychometricResults(),
            ikigai: this.getIkigaiAnalysis(),
            preferences: this.getPreferences(),
            careerResults: this.getCareerResults()
        };
    }

    // Calculate completion percentage
    getCompletionPercentage() {
        const profile = this.getCompleteProfile();
        let completed = 0;
        let total = 4; // Total assessment steps

        if (profile.userData) completed++;
        if (profile.psychometric) completed++;
        if (profile.ikigai) completed++;
        if (profile.careerResults) completed++;

        return Math.round((completed / total) * 100);
    }

    // Export all data
    exportAllData() {
        const profile = this.getCompleteProfile();
        const exportData = {
            ...profile,
            exportedAt: new Date().toISOString(),
            version: '1.0'
        };

        const blob = new Blob([JSON.stringify(exportData, null, 2)], {
            type: 'application/json'
        });

        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `pathfinder-profile-${Date.now()}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    // Import data
    importData(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => {
                try {
                    const data = JSON.parse(e.target.result);
                    
                    // Validate data structure
                    if (this.validateImportData(data)) {
                        // Save imported data
                        if (data.userData) this.saveUserData(data.userData);
                        if (data.psychometric) this.savePsychometricResults(data.psychometric);
                        if (data.ikigai) this.saveIkigaiAnalysis(data.ikigai);
                        if (data.preferences) this.savePreferences(data.preferences);
                        if (data.careerResults) this.saveCareerResults(data.careerResults);
                        
                        resolve(data);
                    } else {
                        reject(new Error('Invalid data format'));
                    }
                } catch (error) {
                    reject(error);
                }
            };
            reader.readAsText(file);
        });
    }

    // Validate import data structure
    validateImportData(data) {
        // Basic validation - check for expected structure
        return data && typeof data === 'object' && data.version;
    }

    // Clear all data
    clearAllData() {
        Object.values(this.storageKeys).forEach(key => {
            Utils.storage.remove(key);
        });
    }

    // Generate career recommendations based on user profile
    generateCareerRecommendations() {
        const psychometric = this.getPsychometricResults();
        const ikigai = this.getIkigaiAnalysis();
        
        if (!psychometric || !ikigai) {
            return [];
        }

        // This would typically involve complex matching algorithms
        // For now, we'll use a simplified approach
        const recommendations = [];
        
        // Load career data (assuming it's available globally)
        if (typeof careerPaths !== 'undefined') {
            careerPaths.forEach(career => {
                const match = Utils.calculateMatch({
                    personality: psychometric.personality,
                    workStyle: psychometric.workStyle,
                    values: psychometric.values,
                    skills: psychometric.skills
                }, career);

                if (match > 50) { // Only include careers with >50% match
                    recommendations.push({
                        ...career,
                        matchPercentage: match,
                        reasons: this.generateMatchReasons(psychometric, career)
                    });
                }
            });
        }

        // Sort by match percentage
        recommendations.sort((a, b) => b.matchPercentage - a.matchPercentage);
        
        return recommendations.slice(0, 5); // Return top 5 matches
    }

    // Generate reasons for career match
    generateMatchReasons(userProfile, career) {
        const reasons = [];
        
        // Check personality matches
        if (userProfile.personality) {
            Object.entries(career.personalityMatch || {}).forEach(([trait, required]) => {
                const userScore = userProfile.personality[trait] || 0;
                if (this.isGoodMatch(userScore, required)) {
                    reasons.push(`Your ${trait} aligns well with this career`);
                }
            });
        }

        // Check skill matches
        if (userProfile.skills && career.requiredSkills) {
            career.requiredSkills.forEach(skill => {
                const userSkillScore = userProfile.skills[skill] || 0;
                if (userSkillScore >= 60) {
                    reasons.push(`Strong ${skill} skills match requirements`);
                }
            });
        }

        return reasons.slice(0, 3); // Return top 3 reasons
    }

    // Check if user score matches required level
    isGoodMatch(userScore, requiredLevel) {
        switch(requiredLevel) {
            case 'high': return userScore >= 60;
            case 'medium': return userScore >= 40 && userScore < 80;
            case 'low': return userScore < 60;
            default: return false;
        }
    }
}

// Create global instance
const dataHandler = new DataHandler();

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DataHandler;
}