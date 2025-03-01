const fs = require('fs/promises');
const path = require('path');
const {getFolderSize} = require("./getSize")
let imagemin
let imageminJpegtran
let imageminJpegRecompress

async function processSource(directoryPath) {
    const oldSize = await getFolderSize(directoryPath) / (1024**2)
    await imagemin([`${directoryPath}/obj_train_data/*.{jpg,png}`], {
        destination: `${directoryPath}/obj_train_data`,
        plugins: [
            imageminJpegtran(),
            imageminJpegRecompress()
        ]
    });
    const newSize = await getFolderSize(directoryPath) / (1024**2)
    console.log(directoryPath, oldSize, newSize)
}

async function processSources(directoryPath) {
    const files = await fs.readdir(directoryPath);
    // const p = []
    for (let f of files) {
        // p.push(processSource(path.join('ai_source/new', f)))
        await processSource(path.join('ai_source/new', f))
    }
    // await Promise.all(p)
}

// Specify the directory containing the text files
const directoryPath = 'ai_source/new'; // Change this to your directory path
(async () => {
    imagemin = (await import('imagemin')).default;
    imageminJpegtran = (await import("imagemin-jpegtran")).default
    imageminJpegRecompress = (await import("imagemin-jpeg-recompress")).default
    await processSources(directoryPath);
})()