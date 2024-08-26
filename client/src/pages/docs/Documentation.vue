<template>
    <h1 class="va-h1">Documentation</h1>
    <VaCard>
        <VaCardContent>
            The Laboratory Information Management System (LIMS) is a web-based application designed to streamline and
            manage
            the workflow of laboratory projects, samples, and experiments. The system enables project managers and
            researchers to define project details, manage samples and experiments, and visualize data through custom
            charts.
        </VaCardContent>
        <VaCardContent>
            <VaAccordion stateful>
                <VaCollapse icon="group" header="User Roles and Permissions">
                    <template #content>
                        <ul class="va-unordered">
                            <li>Admin: Can create, edit, and delete users, projects, samples and
                                experiments. Can add
                                project managers to projects</li>
                            <li>Project Managers: Can create, edit, and delete samples and experiments.
                            </li>
                            <li>Researchers: Can view projects and generate visualizations.</li>
                        </ul>
                    </template>
                </VaCollapse>
                <VaCollapse icon="edit" header="Creating a New Project">
                    <template #content>
                        <ol class="va-ordered">
                            <li>Login</li>
                            <li>Navigate to the "Project Form" page from the main dashboard.</li>
                            <li>Fill in the project details:
                                <ul class="va-unordered">
                                    <li>Project Name: (Required)</li>
                                    <li>Version: (Required)</li>
                                    <li>Description: (Optional)</li>
                                </ul>
                            </li>
                            <li>Define Sample and Experiment Attributes:
                                <ul class="va-unordered">
                                    <li>Choose attribute types (e.g., text input, select, range).</li>
                                    <li>Optionally infer attributes by uploading some TSV files.</li>
                                </ul>
                            </li>
                            <li>Review and save the project</li>
                        </ol>
                    </template>
                </VaCollapse>
                <VaCollapse icon="table_eye" header="Defining Sample and Experiment Attributes">
                    <template #content>
                        <p>Attributes can be defined during project creation. You can choose from various input types:
                        </p>
                        <ul class="va-unordered">
                            <li>Text Input: For free-text data.</li>
                            <li>Select: For predefined options.</li>
                            <li>Range: For numerical ranges.</li>
                        </ul>
                    </template>
                </VaCollapse>
                <VaCollapse icon="upload_file" header="Importing Project Information from TSV">
                    <template #content>
                        <ul class="va-unordered">
                            <li>Upload one or more TSV file during project creation to auto-populate
                                project
                                details and attributes.
                            </li>
                            <li>Map the TSV columns to the corresponding model attributes in the web app.</li>
                        </ul>
                    </template>
                </VaCollapse>
                <VaCollapse icon="upload_file" header="Importing Samples and Experiments from TSV">
                    <template #content>
                        <ul class="va-unordered">
                            <li>Upload a TSV file for samples or experiments.</li>
                            <li>Map the columns to the corresponding attributes in the model.</li>
                            <li>The system validates and imports the data.</li>
                        </ul>
                    </template>
                </VaCollapse>
                <VaCollapse icon="leaderboard" header="Data Visualization">
                    <template #content>
                        <ol class="va-ordered">
                            <li>Select a project from the dashboard.</li>
                            <li>Navigate to the "Data Visualization" section.</li>
                            <li>Choose a chart type: (e.g., Line, Bar, Histogram)</li>
                            <li>Map data fields to the chart axes.</li>
                            <li>Configure chart options (e.g., labels, colors, sizes).</li>
                            <li>Generate and view the chart.</li>
                            <li>Save the chart for future reference or export it as an image.</li>
                        </ol>
                    </template>
                </VaCollapse>
                <VaCollapse icon="description" header="Data Management">
                    <template #content>
                        <ul class="va-unordered">
                            <li>Download experiment and sample data as TSV.</li>
                            <li>Download Project schema as YAML.</li>
                            <li>Export charts as PNG.</li>
                        </ul>
                    </template>
                </VaCollapse>
            </VaAccordion>
        </VaCardContent>
    </VaCard>
</template>
<style scoped>
li {
    line-height: 24px;
}
</style>