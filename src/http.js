import axios from "axios";

export const ena =  axios.create({
    baseURL: "https://www.ebi.ac.uk"
})


export const ncbi = axios.create({
    baseURL: "https://api.ncbi.nlm.nih.gov/datasets/v1"
})