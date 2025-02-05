// Base URL for the API
const API_URL = 'http://127.0.0.1:5000/tasks';

// Helper function to handle errors
function handleError(response) {
  if (!response.ok) {
    throw new Error(`HTTP error! Status: ${response.status}`);
  }
  return response.json();
}

// GET: Fetch tasks for today or tomorrow
export async function fetchTasks(date) {
  try {
    // Fetching tasks from the server by appending the date parameter to the full API URL
    const response = await fetch(`http://127.0.0.1:5000/tasks?date=${date}`);
    return await handleError(response);
  } catch (error) {
    console.error("Error fetching tasks:", error);
    throw error;
  }
}

// POST: Add a new task
export async function addTask(task) {
  try {
    // Sending a POST request to the full API URL to add a new task
    const response = await fetch('http://127.0.0.1:5000/tasks', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(task),
    });
    return await handleError(response);
  } catch (error) {
    console.error("Error adding task:", error);
    throw error;
  }
}

// DELETE: Delete a task
export async function deleteTask(taskId) {
  try {
    // Sending a DELETE request to remove a task by its ID using the full API URL
    const response = await fetch(`http://127.0.0.1:5000/tasks/${taskId}`, {
      method: 'DELETE',
    });
    return await handleError(response);
  } catch (error) {
    console.error("Error deleting task:", error);
    throw error;
  }
}

// PUT: Mark a task as complete
export async function updateTaskStatus(taskId, status) {
  try {
    // Sending a PUT request to the full API URL to update the task's completion status
    const response = await fetch(`http://127.0.0.1:5000/tasks/${taskId}/status`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ completed: status }),
    });
    return await handleError(response);
  } catch (error) {
    console.error("Error updating task status:", error);
    throw error;
  }
}

// PUT: Edit task descriptions inline
export async function updateTaskDescription(taskId, newDescription) {
  try {
    // Sending a PUT request to the full API URL to update the task's description
    const response = await fetch(`http://127.0.0.1:5000/tasks/${taskId}/description`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ description: newDescription }),
    });
    return await handleError(response);
  } catch (error) {
    console.error("Error updating task description:", error);
    throw error;
  }
}
