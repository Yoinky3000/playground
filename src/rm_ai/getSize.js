const fs = require('fs/promises');
const path = require('path');

async function getFolderSize(dir) {
    let totalSize = 0;

    // Read all files and directories in the given directory
    const items = await fs.readdir(dir);

    for (const item of items) {
        const itemPath = path.join(dir, item);
        const stats = await fs.stat(itemPath);

        if (stats.isDirectory()) {
            // Recursively get size of subdirectory
            totalSize += await getFolderSize(itemPath);
        } else {
            // Accumulate file size
            totalSize += stats.size;
        }
    }

    return totalSize;
}

module.exports.getFolderSize = getFolderSize;