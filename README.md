# SCIENTRY – Scientific Entry System 🧬📊

**SCIENTRY** is a flexible, spreadsheet-inspired data management system designed to help researchers manage experimental data with structure, traceability, and collaboration in mind. Whether you're migrating from traditional spreadsheets or setting up a new project from scratch, SCIENTRY provides a user-friendly and robust environment to manage complex scientific datasets, protocols, and visualizations.

---

## 🚀 Features

- **Project-Based Organization**  
  Create project containers that hold one or more *models* (like spreadsheets).

- **Flexible Data Models**  
  Each model:
  - Defines its own **attributes** (column-like fields) with types:  
    `input`, `number`, `select`, or `date`.
  - Contains **records** (rows) with validation rules tied to attribute types.
  - Supports **foreign key–like links** between models.
  - Stores related **protocol files** (e.g., SOPs, PDFs, DOCs) and **image files**.

- **Spreadsheet-Like Usability**  
  - Inline table editing of records  
  - Validation at entry based on attribute types

- **Powerful Role-Based Access Control**  
  - `Admin`: Full permissions  
  - `Project Manager`: Full access within assigned projects  
  - `Data Manager`: Create/update data for assigned models  
  - `Researcher`: Read-only access

- **Visual Reporting and Export**  
  - Download charts and reports per model  
  - Visualize distributions and summaries directly in the app

---

## 🔍 Use Cases

- Replace error-prone spreadsheets with structured and validated data entry
- Manage lab protocols and experimental files per dataset
- Coordinate multi-user collaboration with defined roles
- Maintain links between datasets via model references
- Generate quick visual insights and downloadable reports

---

## 🧑‍🔬 Who Is It For?

- Research labs and institutions
- Bioinformatics and life science teams
- Environmental monitoring projects
- Any group needing structured scientific data management

---

## 📦 Installation

> You’ll be able to deploy SCIENTRY via docker compose
---

## 📸 Screenshots

Coming soon...

---

## 🛠 Tech Stack (Tentative)

- Backend: Python (Flask/FastAPI)
- Frontend: Vue 3 / Vite
- Database: PostgreSQL / MongoDB
- Charting: Chart.js / D3

---

## 📄 License

MIT License — see `LICENSE` file for details.

---

## 🤝 Contributing

Contributions, feature suggestions, and feedback are welcome!  
Please open an issue or submit a pull request.

---

## 📬 Contact

Developer: [Emilio Righi]  
Email: [emilio.righi@crg.eu]  
Lab: Roderic Guigó Lab – CRG Barcelona

---

