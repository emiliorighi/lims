type ValidationError = {
    field: string;
    message: string;
};

export function validateSchemaForm(data: any): ValidationError[] {
    const errors: ValidationError[] = [];

    if (typeof data.project_id !== 'string') {
        errors.push({ field: 'project_id', message: 'project_id must be a string' });
    }

    if (typeof data.name !== 'string') {
        errors.push({ field: 'name', message: 'name must be a string' });
    }

    if (typeof data.version !== 'string') {
        errors.push({ field: 'version', message: 'version must be a string' });
    }

    if (data.description && typeof data.description !== 'string') {
        errors.push({ field: 'description', message: 'description must be a string if provided' });
    }

    if (!validateProjectModel(data.sample)) {
        errors.push({ field: 'sample', message: 'sample must be a valid ProjectModel' });
    }

    if (!validateProjectModel(data.experiment)) {
        errors.push({ field: 'experiment', message: 'experiment must be a valid ProjectModel' });
    }

    return errors;
}

function validateProjectModel(data: any): boolean {
    if (!data || typeof data !== 'object' || !Array.isArray(data.fields) || !Array.isArray(data.id_format)) {
        return false;
    }

    for (const field of data.fields) {
        if (!validateFilter(field)) {
            return false;
        }
    }

    for (const id of data.id_format) {
        if (typeof id !== 'string') {
            return false;
        }
    }

    return true;
}

function validateFilter(data: any): boolean {
    if (typeof data.label !== 'string' ||
        (data.description && typeof data.description !== 'string') ||
        !validateFilterType(data.filter) ||
        typeof data.key !== 'string' ||
        typeof data.required !== 'boolean' ||
        (data.value && typeof data.value !== 'string') ||
        (data.model && !['sample', 'experiment'].includes(data.model))) {
        return false;
    }

    return true;
}

function validateFilterType(filter: any): boolean {
    if (typeof filter !== 'object') {
        return false;
    }
    switch (filter.type) {
        case 'input':
            return typeof filter.inputType === 'string';
        case 'select':
            return Array.isArray(filter.options) && filter.options.every((option: any) => typeof option === 'string');
        case 'range':
            return typeof filter.min === 'number' && typeof filter.max === 'number';
        default:
            return false;
    }
}
