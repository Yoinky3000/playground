import sys
import time
import multiprocessing

def process_file(file, queue):
    for i in range(3):  # Simulate processing steps
        time.sleep(1)  # Simulate time-consuming task
        queue.put((file, f"Processing {file}: step {i + 1}..."))  # Send progress update
    queue.put((file, f"Finished processing {file}."))  # Final status update

def progress_print(queue, total_items):
    completed = 0
    log_lines = []
    while completed < total_items:
        file, msg = queue.get()  # Get the progress message from the queue
        if "Finished" in msg:
            completed += 1  # Increment completed count when a file is finished
        
        # Update the log for the current file
        if len(log_lines) < total_items:
            log_lines.append(msg)
        else:
            log_lines[completed - 1] = msg  # Edit the line of the finished file
        
        # Clear console and print all log lines
        sys.stdout.write('\033[F' * len(log_lines))  # Move the cursor up
        for line in log_lines:
            print(line)  # Print each log line

if __name__ == '__main__':
    files = ['file1.txt', 'file2.txt', 'file3.txt']  # Example files
    total_items = len(files)
    
    queue = multiprocessing.Queue()
    progress_process = multiprocessing.Process(target=progress_print, args=(queue, total_items))
    progress_process.start()

    processes = []
    for file in files:
        p = multiprocessing.Process(target=process_file, args=(file, queue))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    queue.put((None, "All files processed."))  # Send final message
    progress_process.join()  # Wait for the progress print process to finish