const fs = require('fs/promises');
const path = require('path');

async function processSources(directoryPath) {
    const sLimit = 1024*1024*198
    let datasetI = 0
    let i = 0;
    let cSize = 0;
    let train = []
    const folders = await fs.readdir(directoryPath);
    let fusion = {};
    let TargetDatasetPath = path.join("ai_source/combine", "Dataset_" + datasetI)
    let trainPath = path.join("obj_train_data", "frame_" + i)
    let TargetFilePath = path.join(TargetDatasetPath, trainPath)
    for (let fd of folders) {
        const objDataDir = path.join(directoryPath, fd, "obj_train_data")
        const files = await fs.readdir(objDataDir);
        for (const f of files) {
            const objDataFile = path.join(objDataDir, f)
            TargetDatasetPath = path.join("ai_source/combine", "Dataset_" + datasetI)
            trainPath = path.join("obj_train_data", "frame_" + String(i).padStart(6, '0'))
            TargetFilePath = path.join(TargetDatasetPath, trainPath)
            if (objDataFile.endsWith("txt")) {
                await fs.cp(objDataFile, TargetFilePath + ".txt")
                i++
            } else {
                const s = (await fs.stat(objDataFile)).size
                if (cSize + s > sLimit) {
                    console.log(datasetI, fusion, i)
                    fs.writeFile(path.join(TargetDatasetPath, "train.txt"), train.join("\n"), 'utf-8')
                    fs.writeFile(path.join(TargetDatasetPath, "obj.names"),["EP", "OvalBlue", "OvalRed"].join("\n"), 'utf-8')
                    fs.writeFile(path.join(TargetDatasetPath, "obj.data"),["classes = 3", "train = data/train.txt", "names = data/obj.names", "backup = backup/"].join("\n"), 'utf-8')
                    train = []
                    i = 0
                    cSize = 0
                    datasetI++
                    TargetDatasetPath = path.join("ai_source/combine", "Dataset_" + datasetI)
                    trainPath = path.join("obj_train_data", "frame_" + String(i).padStart(6, '0'))
                    TargetFilePath = path.join(TargetDatasetPath, trainPath)
                    fusion = {}
                }
                if (fusion[fd]) fusion[fd]++
                else fusion[fd] = 1
                cSize += s
                train.push("data/" + trainPath.replaceAll("\\", "/") + ".jpg")
                await fs.cp(objDataFile, TargetFilePath + ".jpg")
            }
        }
    }
    console.log(datasetI, fusion, i)
    fs.writeFile(path.join(TargetDatasetPath, "train.txt"), train.join("\n"), 'utf-8')
    fs.writeFile(path.join(TargetDatasetPath, "obj.names"),["EP", "OvalBlue", "OvalRed"].join("\n"), 'utf-8')
    fs.writeFile(path.join(TargetDatasetPath, "obj.data"),["classes = 3", "train = data/train.txt", "names = data/obj.names", "backup = backup/"].join("\n"), 'utf-8')
}

// Specify the directory containing the text files
const directoryPath = 'ai_source/new'; // Change this to your directory path
(async () => {
    await processSources(directoryPath);
})()