import ena from "../../http";

///ENA portal API client service
///see https://www.ebi.ac.uk/ena/portal/api/#/
class ENAClientService {

  getEnaRecord(accession) {
    return ena.enaApi.get(`/ena/browser/api/xml/${accession}?download=true`)
  }
  getTaxon(taxid) {
    return ena.enaApi.get(`/ena/portal/api/links/taxon?accession=${taxid}&format=JSON&result=taxon`)
  }
  submitSamples(url, formData, auth){
    return ena.submitXML(url,formData,auth)
  }
  getENACheckLists(){
    return ena.enaApi.get('/ena/browser/api/summary/ERC000001-ERC999999?offset=0&limit=100')
  }
}

export default new ENAClientService();
