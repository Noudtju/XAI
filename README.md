# XAI – PIP-Net Bird Classification XAI Study

This project is an interactive Dash-based web application designed to evaluate the effectiveness of PIP-Net explanations (Patch and Rectangle visualizations) for bird species classification. It collects user response data across multiple phases to analyze how visual explanations from PIP-Net influence human understanding and decision-making.

---

## 🎯 Goal

To support research in eXplainable AI (XAI) by collecting structured user feedback on model interpretability. This application enables comparison of human prediction accuracy before and after exposure to PIP-Net-generated visual explanations.

---

## 🧪 Study Design: Phases

The app operates in three main phases:

### 1. **Guessing Phase (Phase 1)**
- The user is shown one image per bird class from a prepared dataset.
- The user selects the bird species using a dropdown.
- Responses are logged for baseline analysis.

### 2. **Teaching Phase (Phase 2)**
- After the guessing phase, users are shown model explanations:
  - **Control**: Reference images.
  - **Treatment 1 – Patch**: Patch-based saliency explanations.
  - **Treatment 2 – Rectangle**: Bounding-box-based visual cues.
- The selected explanation phase is logged for each user.

### 3. **Testing Phase (Phase 3)**
- Users again classify bird images randomly chosen from a separate set.
- This tests whether explanations helped improve user accuracy or understanding.
- Class name shown and user answers are recorded.

---
## 🛠 Setup Instructions

Follow the steps below to set up and run the application:

**Step 1**: Download the final curated dataset for user testing from: _[provide download link]_

**Step 2**: Create a directory named `data` inside the project root (`XAI_Dash_App`).

**Step 3**: Place the downloaded dataset inside the `data` directory (e.g., `data/dataset`).

**Step 4**: Open a terminal in the `XAI_Dash_App` folder and run:

```bash
python app.py
```

**Step 5**: Open the app in your browser by visiting the URL printed in the terminal (e.g., http://127.0.0.1:8050/).

---


## 💾 Data Logging

All user interactions are stored in a unified file: `user_guesses.csv`. Each entry includes:

- `user_name`
- `class_name` (ground truth class for Phase 1)
- `image_name` (image shown in Phase 1)
- `user_selection` (Phase 1 guess)
- `teaching_phase` (user-chosen explanation type)
- `testing_phase_class_shown` (class shown in Phase 3)
- `testing_phase_user_answer` (Phase 3 guess)

The application appends new entries or updates existing ones while preserving all data across sessions.

---

## 🔧 Technical Highlights

- Developed with **Plotly Dash** (Python).
- Persistent storage via CSV with in-memory and file sync.
- Handles dynamic component rendering for a guided multi-phase experience.
- Robust across refreshes or restarts.

---

## 📊 Next Steps

- Analyze the CSV to compare Phase 1 vs Phase 3 user accuracy.
- Evaluate explanation effectiveness across different user selections.
- Use results to guide future improvements in PIP-Net and XAI methods.

---

## 📁 Directory Structure

```
XAI_Dash_App/
│
├── app.py
├── README.md
├── data/
│   └── Final_Dataset/
│       └── train/
│           └── [class_name]/image.jpg
├── user_guesses.csv
```