
export interface Breadcrumb {
    label:string,
    route:string
}

export interface Taxon {
    scientific_name:string,
    taxid:number
}

export interface BioSample extends Taxon {
    name:string
    schemaId:string
    metadata:object
}

export interface Experiment {
    title:string,
    description:number,
    schemaId:string,
    metadata:object
}
export interface Analysis {
    title:string,
    description:number,
    schemaId:string,
    metadata:object
}
export interface File {
    url:string,
    type:number,
    name:string,
    metadata:object
}