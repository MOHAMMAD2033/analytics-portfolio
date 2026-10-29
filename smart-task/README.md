# Smart Task
### Daily tasks, priorities, and goals in one place.

[← All four projects](../README.md) · [Application files](index.html) · [JavaScript](js/app.js)

![Smart Task feature overview](assets/workflow.svg)

*Feature overview illustration; not a screenshot.*

## The idea
A university website that helps users turn a busy day into an organized task list. Users can record what they need to do, choose a priority, and track completion.

**HTML · CSS · JavaScript · localStorage**

## What I built

| Part | Work included |
|---|---|
| Page structure | Home, Tasks, About, and Support pages |
| Task management | Add, edit, delete, and complete tasks |
| Planning fields | Manual priority, due-date preferences, goal, and reason |
| Browser storage | Save tasks between visits using localStorage |
| Interface | Styled navigation, task forms, cards, and completion states |

## Inside the task planner

The task page contains a task-entry form and a list of saved tasks. Each task supports a priority, planning details, and completion controls.

**Workflow:** Add a task → choose its priority → record the goal → track completion.

## What this project demonstrates
- Turning a simple user need into a multi-page interface.
- Connecting form inputs to JavaScript interactions.
- Keeping task records in local browser storage.
- Separating page structure, styling, and behavior into clear files.

## Explore the files

| Location | Purpose |
|---|---|
| [index.html](index.html) | Home page and introduction |
| [tasks.html](tasks.html) | Task-entry form and task list |
| [js/app.js](js/app.js) | Task interactions and browser storage |
| [css/](css/) | Page layouts and styling |
| [about.html](about.html) | Project introduction |
| [support.html](support.html) | Demonstration support form |
| [assets/](assets/) | Project overview illustration |

## Try it locally
Download the repository, open `smart-task/index.html` in a browser, and select **Start Planning**. GitHub displays HTML source files; download them to run the website.

## Scope
This is a front-end university prototype. Priorities are selected manually; AI ranking, background notifications, recurring-task automation, and account synchronization are not implemented. The support form is a demonstration and does not send a message. Task data stays in the same browser.

<details>
<summary><b>نبذة بالعربي</b></summary>

موقع جامعي لتنظيم المهام اليومية وتحديد الأولويات ومتابعة الإنجاز. يشمل صفحات الموقع، ونموذج إضافة المهام، وتعديلها وحذفها، وحفظ البيانات داخل المتصفح باستخدام JavaScript. الأولوية يحددها المستخدم بنفسه، ولا توجد تنبيهات تعمل في الخلفية.

</details>

---
[← Back to the portfolio](../README.md)
