const { pipeline } = require('transformers');

async function test() {
    console.log("Loading model...");
    try {
        const generator = await pipeline('text-generation', './', {
            device: 'auto', // Will use Wasm or WebGPU if available
        });
        const output = await generator('Hello, I am', { max_new_tokens: 10 });
        console.log("Output:", JSON.stringify(output));
    } catch (e) {
        console.error("Error:", e);
    }
}

test();
