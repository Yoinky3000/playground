const fs = require('fs/promises');
const path = require('path');

let EP;
let OvalBlue;
let OvalRed;

// Function to process all text files in a directory
async function loopTxt(directoryPath) {
    const files = await fs.readdir(directoryPath);
    const textFiles = files.filter(file => path.extname(file) === '.txt');

    const p = []

    for (const file of textFiles) {
        p.push((async () => {
            const filePath = path.join(directoryPath, file);
            const data = await fs.readFile(filePath, 'utf8')
            const newData = [];
            for (const l of data.split("\n")) {
                if (l.startsWith(EP)) {
                    newData.push(l.replace(/^./, "0"))
                }
                if (l.startsWith(OvalBlue)) {
                    newData.push(l.replace(/^./, "1"))
                }
                if (l.startsWith(OvalRed)) {
                    newData.push(l.replace(/^./, "2"))
                }
            }
            fs.writeFile(filePath, newData.join("\n"), 'utf8');
        })())
    }
    Promise.all(p)
}

async function processSource(directoryPath) {
    const objDataPath = path.join(directoryPath, "obj.data")
    const objNamesPath = path.join(directoryPath, "obj.names")
    const objNames = (await fs.readFile(objNamesPath, 'utf-8')).split("\n")
    const objData = (await fs.readFile(objDataPath, 'utf-8')).split("\n")

    EP = objNames.indexOf("RoboMaster")
    if (EP === -1) EP = objNames.indexOf("Robomaster")
    OvalBlue = objNames.indexOf("OvalArmorBlue")
    OvalRed = objNames.indexOf("OvalArmorRed")
    objData[0] = "classes = 3"

    await loopTxt(path.join(directoryPath,"obj_train_data"))

    fs.writeFile(objNamesPath,["EP", "OvalBlue", "OvalRed"].join("\n"), 'utf-8')
    fs.writeFile(objDataPath,objData.join("\n"), 'utf-8')
}

async function processSources(directoryPath) {
    const files = await fs.readdir(directoryPath);
    const p = []
    for (let f of files) {
        p.push((async () => {
            await fs.cp(path.join(directoryPath, f), path.join('ai_source/new', f), {recursive: true})
            await processSource(path.join('ai_source/new', f))
        })())
    }
    await Promise.all(p)
}

// Specify the directory containing the text files
const directoryPath = 'ai_source/old'; // Change this to your directory path
(async () => {
    await processSources(directoryPath);
})()