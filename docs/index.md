# Project Tracker

**Project Tracker** is a desktop application for tracking progress across multiple online courses. Add courses, tick off chapters as you complete them, take rich-text notes, and collect screenshots — all in one place.

---

## Features

<div class="grid cards" markdown>

-   :material-book-open-page-variant: **Course management**

    ---

    Add courses with a title, provider, link, banner image, and category. Set a chapter count and track each one individually.

-   :material-progress-check: **Progress tracking**

    ---

    Every course displays a live progress bar that updates the moment you tick a chapter as complete.

-   :material-notebook-edit: **Workbook**

    ---

    Each course has its own rich-text workbook. Write notes with bold, italic, bullet lists, and numbered lists. Notes are auto-saved per course.

-   :material-image-multiple: **Gallery**

    ---

    Attach reference images or screenshots to any course. Images are stored locally and displayed in a scrollable gallery.

-   :material-view-dashboard: **Three views**

    ---

    Switch between **Overview** (in-progress), **Browse** (to-do), and **Archived** (completed) courses from the toolbar.

</div>

---

## Getting started
Go to "Packages" on the main page https://github.com/MikloCO/ProjectTracker and download the bin for you operating system. 


## Adding your first course

1. Click **New → Add new course** in the menu bar.
2. Fill in the course details:

    | Field | Description |
    |-------|-------------|
    | Title | Name of the course |
    | Provider | Platform (e.g. Udemy, YouTube) |
    | Link | Optional URL to the course |
    | Number of chapters | How many chapters to create |
    | Banner image | Cover image shown on the card |
    | Category | `art`, `programming`, `ai`, or a custom label |
    | In progress | Check to add directly to the Overview |

3. Click **OK** — the course card appears immediately.

---

## Tracking progress

### Completing chapters

Open a course by clicking its card in **Overview** or **Browse**. The left panel lists all chapters as checkboxes.

!!! tip
    Checking a chapter updates the progress bar on the course card in real time — no need to restart or switch tabs.

### Course status flow

```
todo  ──►  in_progress  ──►  completed
Browse        Overview          Archived
```

Change a course's status from within the course detail view to move it between sections.

---

## Workbook

The right panel of every course detail view is a full rich-text editor.

| Action | Toolbar button |
|--------|---------------|
| Bold | **B** |
| Italic | *I* |
| Underline | U&#x0332; |
| Bullet list | :material-format-list-bulleted: |
| Numbered list | :material-format-list-numbered: |
| Undo / Redo | :material-undo: / :material-redo: |
| Clear formatting | :material-eraser: |

!!! info "Auto-save"
    Notes are saved automatically as you type. Each course stores its workbook in `~/.course_tracker/workbooks/course_<id>.html`.

---

## Gallery

Click the **+** button in the middle panel to pick one or more images from your filesystem. Images are copied into `~/.course_tracker/images/course_<id>/` so the originals can be moved or deleted safely.

---

## Keyboard navigation

| Action | How |
|--------|-----|
| Switch to Overview | Toolbar → *Overview* |
| Switch to Browse | Toolbar → *Browse* |
| Switch to Archived | Toolbar → *Archived* |
| Add a course | Menu → *New → Add new course* |
| Open a course | Click the course card |

---

## Data storage

All course data is persisted to `data/courses.json` in the project directory. Workbook notes and gallery images live in `~/.course_tracker/`.

!!! warning
    Do not manually edit `courses.json` while the application is running — changes will be overwritten on the next save.
