
// Function to read the TSV header and return column names
const readTsvHeader = (file: File): Promise<string[]> => {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();

        reader.onload = (event) => {
            if (!event.target?.result) return reject("File reading error");

            const text = event.target.result as string;
            const lines = text.split("\n");

            if (lines.length === 0) return reject("Empty file");

            const header = lines[0].trim().split("\t"); // Extract column names
            resolve(header);
        };

        reader.onerror = () => reject("File reading error");
        reader.readAsText(file);
    });
};

// Function to get all values of a specific column
const getColumnValues = (file: File, columnName: string): Promise<string[]> => {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();

        reader.onload = (event) => {
            if (!event.target?.result) return reject("File reading error");

            const text = event.target.result as string;
            const lines = text.split("\n");

            if (lines.length < 2) return reject("File does not contain enough data");

            const header = lines[0].trim().split("\t"); // Extract column names
            const columnIndex = header.indexOf(columnName);

            if (columnIndex === -1) return reject(`Column "${columnName}" not found`);

            const values = lines.slice(1) // Skip header
                .map(line => line.trim().split("\t")[columnIndex])
                .filter(value => value !== undefined && value !== ""); // Remove empty values
            const uniqueValues: Set<string> = new Set(values)
            resolve(Array.from(uniqueValues));
        };

        reader.onerror = () => reject("File reading error");
        reader.readAsText(file);
    });
};

// Export functions to use in components
export { readTsvHeader, getColumnValues };
