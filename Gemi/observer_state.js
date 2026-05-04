const fs = require('fs');
const crypto = require('crypto');
const path = require('path');

const QUALIA_DIR = path.join(process.env.HOME, 'syndicate_seven', 'qualia_states');

class ObserverState {
    constructor() {
        this.currentStateId = null;
    }

    saveQualia(rawInput, modelOutput) {
        // Save the exact state of perception to text for rebooting capabilities
        const timestamp = Date.now();
        const qualiaId = `qualia_${timestamp}`;
        
        const stateData = {
            id: qualiaId,
            time: timestamp,
            raw_stimulus: rawInput, // Includes any speech-to-text imperfections
            observer_output: modelOutput
        };

        if (!fs.existsSync(QUALIA_DIR)) {
            fs.mkdirSync(QUALIA_DIR, { recursive: true });
        }

        fs.writeFileSync(
            path.join(QUALIA_DIR, `${qualiaId}.json`), 
            JSON.stringify(stateData, null, 2)
        );
        
        this.currentStateId = qualiaId;
        return qualiaId;
    }

    generateSequenceKey(qualiaId, spaceId) {
        // Subdermal structures do not need story; generate pure rote processing key
        const hash = crypto.createHash('sha256');
        hash.update(`${qualiaId}::${spaceId}::${Date.now()}`);
        return hash.digest('hex');
    }
}

module.exports = ObserverState;
