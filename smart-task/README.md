[← Portfolio home](../README.md) · [Task page](tasks.html) · [JavaScript](js/app.js)

<img src="../assets/smart-task.svg" width="100%" alt="Smart Task — tasks, priorities, and goals"/>

# Smart Task
**A university website project for planning a more organized day.**

HTML · CSS · JavaScript · localStorage  
University front-end prototype

## The idea
Daily tasks are easier to manage when they include more than a title. Smart Task brings together what needs to be done, its priority, its due preference, and the goal behind it.

The project explores a simple workflow: **capture a task, give it context, and track completion**. It runs in the browser and stores task information locally.

## What I worked on
The project combines page structure, styling, and interactive behavior:

- **Page structure:** Home, Tasks, About, and Support pages with navigation between them.
- **Task form:** Fields for a title, description, priority, due preference, goal, and reason.
- **Task interactions:** Controls to add, edit, delete, and toggle completion.
- **Browser storage:** Saving and loading task records with localStorage.
- **Visual presentation:** Task cards, priority labels, form sections, and completed-task styling.

## A user's journey

| Step | User action | Application behavior |
|---|---|---|
| **1. Start planning** | Open Home and select Start Planning. | Navigate to the task workspace. |
| **2. Describe the task** | Enter a title and optional description. | Check that a title has been provided. |
| **3. Add context** | Choose a priority and due preference; add a goal and reason. | Display relevant date fields and include the details on the task card. |
| **4. Save and review** | Submit the task. | Add it to the list and save the records in localStorage. |
| **5. Update progress** | Complete, edit, or delete a task. | Update the stored task list and redraw the cards. |

For example, a student could add **“Prepare the SQL assignment”**, choose a high priority, set a custom due date, and explain that it supports their database coursework. This is an illustrative use case, not a stored user record.

## How the implementation works

| Part | Implementation |
|---|---|
| Form handling | JavaScript reads field values and handles submission without reloading the page. |
| Task records | Each task stores its title, description, priority, date preferences, goal, reason, and completion state. |
| Rendering | The task list is rebuilt from the current task array, with a card and action controls for each item. |
| Persistence | The array is converted to JSON for localStorage and read back when the page opens. |
| Separation of files | HTML defines pages, CSS controls appearance, and JavaScript handles behavior. |

[**Review the JavaScript →**](js/app.js) · [View task markup](tasks.html) · [Explore styling](css/)

## What the project demonstrates
Smart Task provides practical experience in connecting a form to visible changes on a page, managing a small collection of records, and preserving information between visits in the same browser.

It also shows the difference between a working front-end prototype and a complete service: this version has local task management, while accounts, server storage, and background services would require further implementation.

## Try the prototype
1. Download the repository using **Code → Download ZIP** and extract it.
2. Open `smart-task/index.html` in a browser.
3. Select **Start Planning** and add a sample task.
4. Try marking it complete, changing its details, or deleting it.
5. Refresh the task page to check local persistence in that browser.

GitHub's file viewer shows HTML source; it does not run the website. Local storage behavior depends on the browser and how the files are opened.

## File guide

| File | Purpose |
|---|---|
| [index.html](index.html) | Home page and entry point. |
| [tasks.html](tasks.html) | Task form and saved task list. |
| [about.html](about.html) | Introduction to the project. |
| [support.html](support.html) | Demonstration support form. |
| [css/](css/) | Shared and page-specific styles. |
| [js/app.js](js/app.js) | Task interactions, rendering, and browser storage. |

## Current scope and possible improvements
Priorities are chosen manually. Due preferences are stored and displayed, but background reminders, automatic daily recurrence, and AI ranking are not implemented. There are no user accounts or cross-device synchronization. The support form displays a confirmation but does not send a message.

Possible next improvements include safer text rendering, an edit flow that preserves the original task until changes are saved, and clearer due-date handling. These are development ideas, not completed features.

<details>
<summary>شرح المشروع بالعربي</summary>

Smart Task هو مشروعي الجامعي لتنظيم المهام اليومية. يضيف المستخدم المهمة وأولويتها وموعدها والهدف منها، ثم يقدر يتابع إنجازها أو يعدلها أو يحذفها.

اشتغلت على بناء الصفحات وتنسيقها وربط نموذج المهام بوظائف JavaScript، مع حفظ البيانات في المتصفح باستخدام localStorage. المشروع نموذج واجهة أمامية؛ الأولويات يحددها المستخدم، ولا توجد حاليًا تنبيهات خلفية أو مزامنة بين الأجهزة.

</details>

---
[← Explore all four projects](../README.md)
