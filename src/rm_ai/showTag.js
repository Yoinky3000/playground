const fs = require('fs/promises');
const path = require('path');

const s = new Set()

async function processSource(directoryPath) {
    const objNamesPath = path.join(directoryPath, "obj.names")
    const objNames = (await fs.readFile(objNamesPath, 'utf-8')).split("\n")
    for (const n of objNames) {
        s.add(n)
    }
}

// Specify the directory containing the text files
const directoryPath = 'ai_source/old'; // Change this to your directory path
(async () => {
    const files = await fs.readdir(directoryPath);
    for (let f of files) {
        await processSource(path.join('ai_source/old', f))
    }
    console.log(s)
})()