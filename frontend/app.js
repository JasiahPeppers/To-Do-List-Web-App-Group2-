document.addEventListener("DOMContentLoaded", () => {
    // Create the current date
    const today = new Date();
    const dateElement = document.getElementById("currentDate");
    const tomorrowElement = document.getElementById("tomorrowDate");

    dateElement.textContent = today.toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });

    const tomorrow = new Date(today);
    tomorrow.setDate(today.getDate() + 1);
    tomorrowElement.textContent = tomorrow.toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });

    // Task input fields, buttons
    const taskInput = document.getElementById("taskInput");
    const descInput = document.getElementById("descInput");
    const addButton = document.getElementById("addButton");
    const taskList = document.getElementById("taskList");
    let taskCount = 0;

    // Add task button is clicked and placed in the list
    addButton.addEventListener("click", () => {
        const taskValue = taskInput.value.trim();
        const descValue = descInput.value.trim();

        if (taskValue) {
            taskCount++; // Increase the task count
            const task = {
                title: taskValue,
                description: descValue,
                done: false
            };

            // POST request to add task to the backend
            fetch('http://localhost:5000/tasks', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(task)
            })
            .then(response => response.json())
            .then(newTask => {
                addTaskToList(newTask); // Add the task to the UI list after successful POST
                taskInput.value = ''; // Clear the input fields
                descInput.value = '';
            })
            .catch(error => {
                console.error('Error adding task:', error);
            });
        }
    });

    // Function to display tasks on the UI
    function addTaskToList(task) {
        const listItem = document.createElement("li");
        listItem.draggable = true;

        listItem.innerHTML = `
            <div class="task-wrapper">
                <span class="task-title">
                    <span class="task-number">${taskCount}.</span> ${task.title}
                </span>
                <span class="desc">${task.description}</span>
            </div>
            <div class="action-buttons" style="display:none;">
                <button class="delete-btn">Delete</button>
                <button class="complete-btn">Complete</button>
                <button class="incomplete-btn" style="display: none;">Incomplete</button>
            </div>
        `;

        taskList.appendChild(listItem);

        // Toggle the visibility of action buttons
        const actionButtons = listItem.querySelector('.action-buttons');
        listItem.addEventListener('click', function () {
            const isActionButtonsVisible = actionButtons.style.display === 'inline-block';
            actionButtons.style.display = isActionButtonsVisible ? 'none' : 'inline-block';
        });

        // Delete button
        const deleteButton = listItem.querySelector('.delete-btn');
        deleteButton.addEventListener('click', function () {
            // DELETE request to backend to remove task
            fetch(`http://localhost:5000/tasks/${task.id}`, {
                method: 'DELETE'
            })
            .then(() => {
                taskList.removeChild(listItem);
            })
            .catch(error => {
                console.error('Error deleting task:', error);
            });
        });

        // Complete button
        const completeButton = listItem.querySelector('.complete-btn');
        const incompleteButton = listItem.querySelector('.incomplete-btn');
        completeButton.addEventListener('click', function () {
            listItem.classList.toggle('completed');
            completeButton.style.display = 'none';
            incompleteButton.style.display = 'inline-block';
        });

        // Incomplete button
        incompleteButton.addEventListener('click', function () {
            listItem.classList.remove('completed');
            completeButton.style.display = 'inline-block';
            incompleteButton.style.display = 'none';
        });

        // Description editing functionality
        const descElement = listItem.querySelector('.desc');
        descElement.addEventListener('click', function () {
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
            textarea.addEventListener('keypress', function (e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    descElement.textContent = textarea.value;
                    textarea.replaceWith(descElement);
                    descElement.style.display = 'block';

                    // PUT request to update description on the backend
                    fetch(`http://localhost:5000/tasks/${task.id}`, {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            description: textarea.value
                        })
                    })
                    .then(response => response.json())
                    .then(updatedTask => {
                        console.log('Task updated:', updatedTask);
                    })
                    .catch(error => {
                        console.error('Error updating task:', error);
                    });
                }
            });

            textarea.addEventListener('blur', function () {
                descElement.textContent = textarea.value;
                textarea.replaceWith(descElement);
                descElement.style.display = 'block';

                // PUT request to update description on the backend
                fetch(`http://localhost:5000/tasks/${task.id}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        description: textarea.value
                    })
                })
                .then(response => response.json())
                .then(updatedTask => {
                    console.log('Task updated:', updatedTask);
                })
                .catch(error => {
                    console.error('Error updating task:', error);
                });
            });
        });
    }
});
