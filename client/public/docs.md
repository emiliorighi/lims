# Laboratory Information Management System (LIMS) Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [User Roles and Permissions](#user-roles-and-permissions)
3. [Project Management](#project-management)
    - [Creating a New Project](#creating-a-new-project)
    - [Defining Sample and Experiment Attributes](#defining-sample-and-experiment-attributes)
    - [Importing Project Information from TSV](#importing-project-information-from-tsv)
4. [Sample and Experiment Management](#sample-and-experiment-management)
    - [Creating Samples](#creating-samples)
    - [Creating Experiments](#creating-experiments)
    - [Importing Samples and Experiments from TSV](#importing-samples-and-experiments-from-tsv)
5. [Data Visualization](#data-visualization)
    - [Creating Custom Charts](#creating-custom-charts)
6. [Data Management](#data-management)
    - [Exporting Data](#exporting-data)
    - [Data Integrity and Validation](#data-integrity-and-validation)
7. [Future Enhancements](#future-enhancements)

## Introduction

The Laboratory Information Management System (LIMS) is a web-based application designed to streamline and manage the workflow of laboratory projects, samples, and experiments. The system enables project managers and researchers to define project details, manage samples and experiments, and visualize data through custom charts.

## User Roles and Permissions

- **Admin:** Can create, edit, and delete users, projects, samples and experiments. Can add project managers to projects
- **Project Managers:** Can create, edit, and delete samples and experiments.
- **Researchers:** Can view projects and generate visualizations.


## Project Management

### Creating a New Project
1. **Navigate to the "Create Project" page** from the main dashboard.
2. **Fill in the project details:**
   - **Project Name:** (Required)
   - **Description:** (Optional)
   - **Version:** (Required)
3. **Define Sample and Experiment Attributes:**
   - Choose attribute types (e.g., text input, select, range).
   - Optionally infer attributes by uploading some TSV files.
4. **Click "Create Project"** to save the project.

### Defining Sample and Experiment Attributes
Attributes can be defined during project creation. You can choose from various input types:
- **Text Input:** For free-text data.
- **Select:** For predefined options.
- **Range:** For numerical ranges.

### Importing Project Information from TSV
- **Upload a TSV file** during project creation to auto-populate project details and attributes.
- Map the TSV columns to the corresponding model attributes in the web app.

## Sample and Experiment Management

### Importing Samples and Experiments from TSV
- **Upload a TSV file** for samples or experiments.
- **Map the columns** to the corresponding attributes in the model.
- The system validates and imports the data.

## Data Visualization

### Creating Custom Charts
1. **Select a project** from the dashboard.
2. **Navigate to the "Data Visualization" section.**
3. **Choose a chart type:** (e.g., Line, Bar, Histogram)
4. **Map data fields** to the chart axes.
5. **Configure chart options** (e.g., labels, colors, sizes).
6. **Generate and view the chart.**
7. **Save the chart** for future reference or export it as an image.

## Data Management

### Exporting Data
- **Download experiment and sample data** as TSV or JSON format.
- **Download Project schema** as YAML.
- **Export charts** as PNG.

### Data Integrity and Validation
- The system ensures data integrity through validation rules during data entry.
- Any inconsistencies or errors are flagged for correction.

## Future Enhancements
- **Automated data analysis:** Integrate with data analysis tools for automated insights.
- **Advanced visualizations:** Support for more complex visualizations (e.g., 3D plots).
- **Real-time collaboration:** Multiple users can work on the same project simultaneously.
