document.addEventListener("DOMContentLoaded", () => { 
// Create the current date 
const today = new Date(); 

//Show HTML dates 
const dateElement = document.getElementById("currentDate"); 
const tomorrowElement = document.getElementById("tomorrowDate"); 

// Format the current date in order to Monday, January 27, 2025 
dateElement.textContent = today.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
 
// Date container for future's date 
const tomorrow = new Date(today); 
tomorrow.setDate(today.getDate() + 1) // the number 1 is adding onto the current date for tomorow
tomorrowElement.textContent = tomorrow.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });  

// Task input feilds, buttons 
const taskInput = document.getElementById("taskInput"); 
const descInput = document.getElementById("descInput"); 
const addButton = document.getElementById("addButton"); 
const taskList = document.getElementById("taskList"); 
let taskCount = 0; // for numbering the tasks in order 

// Add task button is clicked and placed in the list
addButton.addEventListener("click", () => {
const taskValue = taskInput.value.trim(); // recieve task
const descValue = descInput.value.trim(); //receive description

if (taskValue) {
taskCount++; // increase the task counting
const listItem = document.createElement("li");
listItem.draggable = true;
listItem.classList.add("low-priority");

listItem.innerHTML = `
<div class="task-wrapper">
<span class="task-title"><span class="task-number">${taskCount}.</span> ${taskValue}</span>
<span class="desc">${descValue}</span>
</div>
<div class="action-buttons" style="display:none;">  
<button class="delete-btn">Delete</button>
<button class="complete-btn">Complete</button>
<button class="incomplete-btn" style="display: none;">Incomplete</button> 
</div>
`;

taskList.appendChild(listItem);
taskInput.value = '';
descInput.value = '';

const actionButtons = listItem.querySelector('.action-buttons');

listItem.addEventListener('click', function() {  // action buttons will become visible when tasks are clicked 
const isActionButtonsVisible = actionButtons.style.display === 'inline-block'; 
actionButtons.style.display = isActionButtonsVisible ? 'none' : 'inline-block'; 
});

// Add delete button 
const deleteButton = listItem.querySelector('.delete-btn');
deleteButton.addEventListener('click', function() {
taskList.removeChild(listItem);

});

// This is the complete button 
const completeButton = listItem.querySelector('.complete-btn');
const incompleteButton = listItem.querySelector(' .incomplete-btn'); 


completeButton.addEventListener('click', function() {
listItem.classList.toggle('completed'); // should remove/add mark effect
completeButton.style.display = 'none'; 
incompleteButton.style.display = 'inline-block'; 
});

incompleteButton.addEventListener('click', function() { 
listItem.classList.remove('completed'); //removes the slash mark
completeButton.style.display = 'inline-block'; 
incompleteButton.style.display = 'none'; 
}); 
const descElement = listItem.querySelector('.desc'); 

descElement.addEventListener('click', function() { 
const currentDesc = descElement.textContent.trim(); 
const textarea = document.createElement('textarea'); 
textarea.value = currentDesc; 
textarea.style.width = '200px'; 
textarea.style.height = '40px'; 
descElement.replaceWith(textarea); 

textarea.addEventListener('keypress', function(e) { 
if (e.key === 'Enter') { 
e.preventDefault(); 
descElement.textContent = textarea.value; 
textarea.replaceWith(descElement); 
} 

}); 

textarea.addEventListener('blur', function() { 
descElement.textContent = textarea.value; 
textarea.replaceWith(descElement); 

});

function loadTasks() { 
function loadTasks() {
  const tasks = [
    { name: "Buy groceries", description: "Get milk, eggs, and bread" },
    { name: "Walk the dog", description: "" },
  ];

  tasks.forEach((task, index) => {
    const listItem = document.createElement("li");
    listItem.draggable = true;
    listItem.classList.add("low-priority");

    listItem.innerHTML = `
      <div class="task-wrapper">
        <span class="task-title"><span class="task-number">${index + 1}.</span> ${task.name}</span>
        <span class="desc">${task.description}</span>
      </div>
      <div class="action-buttons" style="display:none;">
        <button class="delete-btn">Delete</button>
        <button class="complete-btn">Complete</button>
        <button class="incomplete-btn" style="display: none;">Incomplete</button> 
      </div>
    `;
    taskList.appendChild(listItem);
  });
}


}); 

} 

}); 

}); 






