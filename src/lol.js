const blessed = require('blessed');

// Create a screen object
const screen = blessed.screen();

// Create a text element for displaying process information
const processInfo = blessed.text({
  top: 'center',
  left: 'center',
  width: '50%',
  height: '50%',
  content: 'processA: task XXX, done: XXX',
  tags: true,
  style: {
    fg: 'white',
    bg: 'black'
  }
});

// Append the text element to the screen
screen.append(processInfo);

// Function to update the process information
function updateProcessInfo(task, doneCount) {
  processInfo.setContent(`processA: task ${task}, done: ${doneCount}`);
  screen.render();
}

// Simulating a process with tasks and progress
function simulateProcess() {
  const tasks = ['Task 1', 'Task 2', 'Task 3'];
  let doneCount = 0;

  setInterval(() => {
    // Simulating task completion
    const taskIndex = Math.floor(Math.random() * tasks.length);
    const completedTask = tasks[taskIndex];
    tasks.splice(taskIndex, 1);
    doneCount++;

    // Update the process information
    updateProcessInfo(completedTask, doneCount);

    if (tasks.length === 0) {
      clearInterval(interval);
    }
  }, 2000);
}

// Start the process simulation
simulateProcess();

// Handle key presses and exit the program on Esc
screen.key(['escape', 'q', 'C-c'], () => process.exit(0));

// Render the screen
screen.render();