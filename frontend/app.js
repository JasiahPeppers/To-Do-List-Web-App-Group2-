document.addEventListener("DOMContentLoaded", () => { 

// Create the current date 
    const today = new Date(); 

// Show HTML dates
const dateElement = document.getElementById("currentDate"); 
const tomorrowElement = document.getElementById("tomorrowDate"); 

// Format the current date in order to Monday, January 27, 2025
dateElement.textContent = today.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });

// Date container for tomorrow's date  
const tomorrow = new Date(today); 
tomorrow.setDate(today.getDate() + 1); // Adding 1 day to today for tomorrow
tomorrowElement.textContent = tomorrow.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });  

// Task input fields, buttons 
const taskInput = document.getElementById("taskInput"); 
const descInput = document.getElementById("descInput"); 
const addButton = document.getElementById("addButton"); 
const taskList = document.getElementById("taskList"); 
let taskCount = 0; // For numbering the tasks

// GET request to fetch tasks from server    
// Fetch tasks for today/tomorrow
fetch('http://your-backend-url/tasks')
.then(response => response.json())
.then(tasks => {
tasks.forEach(task => {
const listItem = document.createElement("li");
listItem.draggable = true;
listItem.innerHTML = `
<div class="task-wrapper">
<span class="task-title">
<span class="task-number">${task.id}.</span> ${task.task}
</span>
<span class="desc">${task.desc}</span>
</div>
<div class="action-buttons" style="display:none;">  
<button class="delete-btn">Delete</button>
<button class="complete-btn">Complete</button>
<button class="incomplete-btn" style="display: none;">Incomplete</button> 
</div>
`;
taskList.appendChild(listItem); // Add tasks to UI
});
})
.catch((error) => {
console.error('Error fetching tasks:', error); // Handle fetch error
});

// POST request to handle task input via the "Add Task" button 
addButton.addEventListener("click", () => {
const taskValue = taskInput.value.trim(); // receive task
const descValue = descInput.value.trim(); // receive description

if (taskValue) {
taskCount++; // Increase the task count
const listItem = document.createElement("li");
listItem.draggable = true;

listItem.innerHTML = `
<div class="task-wrapper">
<span class="task-title">
<span class="task-number">${taskCount}.</span> ${taskValue}
</span>

<span class="desc">${descValue}</span>
</div>
<div class="action-buttons" style="display:none;">  
<button class="delete-btn">Delete</button>
<button class="complete-btn">Complete</button>
<button class="incomplete-btn" style="display: none;">Incomplete</button> 
</div>
`;

// POST: Send new task to the server
fetch('http://your-backend-url/tasks', {
method: 'POST',
headers: {
'Content-Type': 'application/json',
},
body: JSON.stringify({
task: taskValue,
desc: descValue,
priority: 'Medium', // Example priority field
task_date: new Date().toLocaleDateString(), // Current date
})
})
.then(response => response.json())
.then(data => {
console.log('Task added successfully:', data); // Handle successful addition
})
.catch((error) => {
console.error('Error adding task:', error); // Handle POST failure
});

 taskList.appendChild(listItem); // Add to the task list UI
taskInput.value = ''; // Clear input fields
descInput.value = ''; 

const actionButtons = listItem.querySelector('.action-buttons');

listItem.addEventListener('click', function() {
const isActionButtonsVisible = actionButtons.style.display === 'inline-block'; 
actionButtons.style.display = isActionButtonsVisible ? 'none' : 'inline-block'; 
});

       
// DELETE request to remove a task (and delete from the server)
           
const deleteButton = listItem.querySelector('.delete-btn');
deleteButton.addEventListener('click', function() {
// DELETE: Send request to delete task from the server
fetch(`http://your-backend-url/tasks/${taskCount}`, {
method: 'DELETE',
})
.then(response => response.json())
.then(data => {
console.log('Task deleted:', data); // Task deleted successfully
taskList.removeChild(listItem); // Remove from UI
 })
.catch((error) => {
console.error('Error deleting task:', error); // Handle DELETE failure
});
});

// PUT to update mark a task as complete
const completeButton = listItem.querySelector('.complete-btn');
const incompleteButton = listItem.querySelector('.incomplete-btn');
completeButton.addEventListener('click', function() {
listItem.classList.toggle('completed');
completeButton.style.display = 'none'; 
incompleteButton.style.display = 'inline-block'; 

// PUT request to update task status to 'completed' on the server
fetch(`http://your-backend-url/tasks/${taskCount}`, {
method: 'PUT',
headers: {
'Content-Type': 'application/json',
},
body: JSON.stringify({
status: 'completed', // Update task status
})
})
.then(response => response.json())
.then(data => {
console.log('Task status updated:', data); // Task status updated
})
.catch((error) => {
console.error('Error updating task status:', error); // Handle PUT failure
});
});

// Incomplete button (marks task as incomplete)
incompleteButton.addEventListener('click', function() { 
listItem.classList.remove('completed');
completeButton.style.display = 'inline-block'; 
incompleteButton.style.display = 'none';
});

// PUT request to update the edit task dec 
const descElement = listItem.querySelector('.desc'); 
descElement.addEventListener('click', function() { 
const currentDesc = descElement.textContent.trim(); 
const textarea = document.createElement('textarea'); 
textarea.value = currentDesc; 
textarea.style.width = '100%'; 
textarea.style.height = '40px';

// Insert the textarea directly below the task title
const taskWrapper = listItem.querySelector('.task-wrapper');
taskWrapper.appendChild(textarea)

// Hide the original description text while editing
descElement.style.display = 'none'; 

// Focus the textarea so user can edit right away
textarea.focus();
textarea.addEventListener('keypress', function(e) { 
if (e.key === 'Enter') { 
e.preventDefault(); 
descElement.textContent = textarea.value; 
textarea.replaceWith(descElement); // Replace textarea with updated description
descElement.style.display = 'block'; // Show the updated description again
}
}); 

textarea.addEventListener('blur', function() { 
descElement.textContent = textarea.value; 
textarea.replaceWith(descElement); // Replace textarea with updated description
                    descElement.style.display = 'block'; // Show the updated description again
                });

            });

        }
    });
});
