const taskForm = document.getElementById("taskForm");
const taskList = document.getElementById("taskList");

if (taskForm && taskList) {
  const dueOptions = document.querySelectorAll('input[name="due"]');
  const customDateField = document.getElementById("customDateField");
  const excludedDaysField = document.getElementById("excludedDaysField");

  const taskTitle = document.getElementById("taskTitle");
  const taskDescription = document.getElementById("taskDescription");
  const taskDate = document.getElementById("taskDate");
  const taskTime = document.getElementById("taskTime");
  const taskGoal = document.getElementById("taskGoal");
  const taskReason = document.getElementById("taskReason");

  const priorityOptions = document.querySelectorAll('input[name="priority"]');

  let tasks = JSON.parse(localStorage.getItem("tasks")) || [];

  function saveTasks() {
    localStorage.setItem("tasks", JSON.stringify(tasks));
  }

  function updateDueFields(value) {
    if (value === "Custom") {
      customDateField.classList.add("show");
      excludedDaysField.classList.remove("show");
    } else if (value === "Daily") {
      customDateField.classList.remove("show");
      excludedDaysField.classList.add("show");
    } else {
      customDateField.classList.remove("show");
      excludedDaysField.classList.remove("show");
    }
  }

  function formatTime(time) {
    if (time === "") {
      return "";
    }

    const timeParts = time.split(":");
    let hours = Number(timeParts[0]);
    const minutes = timeParts[1];

    const period = hours >= 12 ? "PM" : "AM";

    hours = hours % 12;

    if (hours === 0) {
      hours = 12;
    }

    return hours + ":" + minutes + " " + period;
  }

  function renderTasks() {
    taskList.innerHTML = "";

    tasks.forEach(function(task, index) {
      const taskCard = document.createElement("div");
      taskCard.classList.add("task-card");

      if (task.completed) {
        taskCard.classList.add("completed");
      }

      taskCard.innerHTML = `
        <span class="priority-badge ${task.priority.toLowerCase()}">
          ${task.priority}
        </span>

        <h3>${task.title}</h3>

        <p>${task.description || "No description added."}</p>

        <p><strong>Due:</strong> ${task.dueText}</p>

        <p><strong>Goal:</strong> ${task.goal || "Not linked"}</p>

        <p><strong>Why important:</strong> ${task.reason || "Not specified"}</p>

        ${task.excludedText}

        <div class="task-actions">
          <button class="complete-btn" type="button">
            ${task.completed ? "Completed" : "Complete"}
          </button>

          <button class="edit-btn" type="button">Edit</button>

          <button class="delete-btn" type="button">Delete</button>
        </div>
      `;

      const completeBtn = taskCard.querySelector(".complete-btn");
      const editBtn = taskCard.querySelector(".edit-btn");
      const deleteBtn = taskCard.querySelector(".delete-btn");

      completeBtn.addEventListener("click", function() {
        tasks[index].completed = !tasks[index].completed;
        saveTasks();
        renderTasks();
      });

      deleteBtn.addEventListener("click", function() {
        const confirmDelete = confirm("Are you sure you want to delete this task?");

        if (confirmDelete) {
          tasks.splice(index, 1);
          saveTasks();
          renderTasks();
        }
      });

      editBtn.addEventListener("click", function() {
        taskTitle.value = task.title;
        taskDescription.value = task.description;
        taskDate.value = task.date;
        taskTime.value = task.time;
        taskGoal.value = task.goal;
        taskReason.value = task.reason;

        priorityOptions.forEach(function(option) {
          option.checked = option.value === task.priority;
        });

        dueOptions.forEach(function(option) {
          option.checked = option.value === task.due;
        });

        updateDueFields(task.due);

        tasks.splice(index, 1);
        saveTasks();
        renderTasks();

        window.scrollTo({
          top: taskForm.offsetTop - 120,
          behavior: "smooth"
        });
      });

      taskList.appendChild(taskCard);
    });
  }

  dueOptions.forEach(function(option) {
    option.addEventListener("change", function() {
      updateDueFields(option.value);
    });
  });

  taskForm.addEventListener("submit", function(e) {
    e.preventDefault();

    const title = taskTitle.value.trim();
    const description = taskDescription.value.trim();
    const date = taskDate.value;
    const time = taskTime.value;
    const goal = taskGoal.value.trim();
    const reason = taskReason.value.trim();

    if (title === "") {
      alert("Please enter a task title.");
      return;
    }

    let selectedPriority = "Low";

    priorityOptions.forEach(function(option) {
      if (option.checked) {
        selectedPriority = option.value;
      }
    });

    let selectedDue = "Today";

    dueOptions.forEach(function(option) {
      if (option.checked) {
        selectedDue = option.value;
      }
    });

    let dueText = "";

    if (selectedDue === "Today") {
      dueText = "Today";
    } else if (selectedDue === "Tomorrow") {
      dueText = "Tomorrow";
    } else if (selectedDue === "Daily") {
      dueText = "Daily";
    } else if (selectedDue === "Custom") {
      if (date === "") {
        alert("Please select a custom date.");
        return;
      }

      const dateYear = new Date(date).getFullYear();

      if (dateYear < 2025 || dateYear > 2050) {
        alert("Please select a valid date between 2025 and 2050.");
        return;
      }

      dueText = date;
    }

    const formattedTime = formatTime(time);

    if (formattedTime !== "") {
      dueText += " at " + formattedTime;
    }

    const checkedDays = document.querySelectorAll("#excludedDaysField input:checked");
    const excludedDays = [];

    checkedDays.forEach(function(day) {
      excludedDays.push(day.value);
    });

    let excludedText = "";

    if (selectedDue === "Daily") {
      if (excludedDays.length > 0) {
        excludedText = `<p><strong>Excluded:</strong> ${excludedDays.join(" × ")} ×</p>`;
      } else {
        excludedText = `<p><strong>Excluded:</strong> None</p>`;
      }
    }

    const newTask = {
      title: title,
      description: description,
      priority: selectedPriority,
      due: selectedDue,
      dueText: dueText,
      date: date,
      time: time,
      goal: goal,
      reason: reason,
      excludedText: excludedText,
      completed: false
    };

    tasks.push(newTask);
    saveTasks();
    renderTasks();

    taskForm.reset();
    updateDueFields("Today");
  });

  renderTasks();
}

const supportForm = document.getElementById("supportForm");

if (supportForm) {
  supportForm.addEventListener("submit", function(e) {
    e.preventDefault();

    const name = document.getElementById("supportName").value.trim();
    const email = document.getElementById("supportEmail").value.trim();
    const topic = document.getElementById("supportTopic").value.trim();
    const message = document.getElementById("supportMessage").value.trim();

    if (
      name === "" ||
      email === "" ||
      topic === "" ||
      message === ""
    ) {
      alert("Please fill in all fields.");
      return;
    }

    alert("Your message has been submitted. We will respond within 24 hours.");

    supportForm.reset();
  });
}