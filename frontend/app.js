document.addEventListener("DOMContentLoaded", () => { 
    // Create the current date 
    const today = new Date(); 

    // Show HTML dates
    const dateElement = document.getElementById("currentDate"); 
    const tomorrowElement = document.getElementById("tomorrowDate"); 

    // Format the current date
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

    // Add task button is clicked and placed in the list
    addButton.addEventListener("click", () => {
        const taskValue = taskInput.value.trim(); // receive task
        const descValue = descInput.value.trim(); // receive description

        if (taskValue) {
            taskCount++; // Increase the task count
            const task = {
                task: taskValue,  // Add task from input
                desc: descValue,  // Add description from input
            };

            // Directly add the task to the list (no backend calls)
            addTaskToList(task);
            taskInput.value = ''; // Clear the input fields
            descInput.value = '';
        }
    });

    // Function to display tasks on the UI
    function addTaskToList(task) {
        const listItem = document.createElement("li");
        listItem.draggable = true;
        taskCount++; // To increment task number
        listItem.innerHTML = `
            <div class="task-wrapper">
                <span class="task-title">
                    <span class="task-number">${taskCount}.</span> ${task.task}
                </span>
                <span class="desc">${task.desc}</span>
            </div>
            <div class="action-buttons" style="display:none;">  
                <button class="delete-btn">Delete</button>
                <button class="complete-btn">Complete</button>
                <button class="incomplete-btn" style="display: none;">Incomplete</button> 
            </div>
        `;

        taskList.appendChild(listItem);

        const actionButtons = listItem.querySelector('.action-buttons');

        listItem.addEventListener('click', function() {
            const isActionButtonsVisible = actionButtons.style.display === 'inline-block'; 
            actionButtons.style.display = isActionButtonsVisible ? 'none' : 'inline-block'; 
        });

        // Delete button functionality (no backend)
        const deleteButton = listItem.querySelector('.delete-btn');
        deleteButton.addEventListener('click', function() {
            taskList.removeChild(listItem); // Remove the task from UI
        });

        // Complete task button
        const completeButton = listItem.querySelector('.complete-btn');
        const incompleteButton = listItem.querySelector('.incomplete-btn'); 
        completeButton.addEventListener('click', function() {
            listItem.classList.toggle('completed');
            completeButton.style.display = 'none'; 
            incompleteButton.style.display = 'inline-block'; 
        });

        // Incomplete task button
        incompleteButton.addEventListener('click', function() { 
            listItem.classList.remove('completed');
            completeButton.style.display = 'inline-block'; 
            incompleteButton.style.display = 'none'; 
        });

        // Description editing functionality
        const descElement = listItem.querySelector('.desc'); 
        descElement.addEventListener('click', function() { 
            const currentDesc = descElement.textContent.trim(); 
            const textarea = document.createElement('textarea'); 
            textarea.value = currentDesc; 
            textarea.style.width = '100%'; 
            textarea.style.height = '40px';

            // Insert the textarea directly below the task title
            const taskWrapper = listItem.querySelector('.task-wrapper');
            taskWrapper.appendChild(textarea);

            // Hide the original description text while editing
            descElement.style.display = 'none'; 

            // Focus the textarea so user can edit
            textarea.focus();
            textarea.addEventListener('keypress', function(e) { 
                if (e.key === 'Enter') { 
                    e.preventDefault(); 
                    descElement.textContent = textarea.value; 
                    textarea.replaceWith(descElement); 
                    descElement.style.display = 'block'; 
                }
            });

            textarea.addEventListener('blur', function() { 
                descElement.textContent = textarea.value; 
                textarea.replaceWith(descElement); 
                descElement.style.display = 'block'; 
            });
        });
    }
});