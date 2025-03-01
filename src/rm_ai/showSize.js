const fs = require('fs/promises');
const path = require('path');

const {getFolderSize} = require("./getSize");

// Specify the directory containing the text files
const directoryPath = 'ai_source/new'; // Change this to your directory path
(async () => {
    let totalSize = 0;
    const files = await fs.readdir(directoryPath);
    for (let f of files) {
        const p = path.join('ai_source/new', f)
        const s = await getFolderSize(p) / 1024 / 1024
        totalSize += s
        console.log(p, s)
    }
    console.log(totalSize)
})()

