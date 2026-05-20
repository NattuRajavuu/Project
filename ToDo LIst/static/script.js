const taskInput = document.getElementById("task-input");
const addButton = document.getElementById("add-button");
const taskList = document.getElementById("task-list");
const emptyState = document.getElementById("empty-state");
const totalCount = document.getElementById("total-count");
const completedCount = document.getElementById("completed-count");

let tasks = Array.isArray(window.initialTasks) ? window.initialTasks : [];

function renderTasks() {
  taskList.innerHTML = "";
  const completed = tasks.filter((task) => task.completed).length;
  totalCount.textContent = tasks.length;
  completedCount.textContent = completed;

  if (tasks.length === 0) {
    emptyState.style.display = "block";
    return;
  }

  emptyState.style.display = "none";

  tasks.forEach((task) => {
    const taskItem = document.createElement("div");
    taskItem.className = "task-item";

    const left = document.createElement("div");
    left.className = "task-left";

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.className = "task-checkbox";
    checkbox.checked = task.completed;
    checkbox.addEventListener("change", () => toggleCompleted(task.id));

    const text = document.createElement("span");
    text.className = `task-text${task.completed ? " completed" : ""}`;
    text.textContent = task.title;

    left.appendChild(checkbox);
    left.appendChild(text);

    const actions = document.createElement("div");
    actions.className = "task-actions";

    const deleteButton = document.createElement("button");
    deleteButton.textContent = "Delete";
    deleteButton.addEventListener("click", () => deleteTask(task.id));

    actions.appendChild(deleteButton);
    taskItem.appendChild(left);
    taskItem.appendChild(actions);
    taskList.appendChild(taskItem);
  });
}

function showError(message) {
  alert(message);
}

async function addTask() {
  const title = taskInput.value.trim();
  if (!title) {
    return;
  }

  const response = await fetch("/add", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ title }),
  });

  if (!response.ok) {
    const data = await response.json();
    showError(data.message || "Unable to add task.");
    return;
  }

  const data = await response.json();
  tasks = data.tasks;
  taskInput.value = "";
  renderTasks();
}

async function toggleCompleted(taskId) {
  const response = await fetch(`/complete/${taskId}`, { method: "POST" });
  if (!response.ok) {
    showError("Unable to update task.");
    return;
  }
  const data = await response.json();
  tasks = data.tasks;
  renderTasks();
}

async function deleteTask(taskId) {
  const response = await fetch(`/delete/${taskId}`, { method: "POST" });
  if (!response.ok) {
    showError("Unable to delete task.");
    return;
  }
  const data = await response.json();
  tasks = data.tasks;
  renderTasks();
}

addButton.addEventListener("click", addTask);

taskInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    addTask();
  }
});

renderTasks();
