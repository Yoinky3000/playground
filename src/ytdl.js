const ytdl = require('@distube/ytdl-core');
const fs = require('fs');
const videoId = '';
// Get video info from YouTube
ytdl.getInfo(videoId).then((info) => {
  // Create a write stream to save the video file
  const outputFilePath = `./ytdl-result/${info.videoDetails.title}.mp4`;
  ytdl(videoId).pipe(fs.createWriteStream(outputFilePath));
}).catch((err) => {
  console.error(err);
});