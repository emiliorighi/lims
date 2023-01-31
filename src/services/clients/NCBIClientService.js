import {ncbi} from "../../http";

///ENA portal API client service
///see https://www.ebi.ac.uk/ena/portal/api/#/
class NCBIClientService {


  getTaxon(taxid) {
    return ncbi.get(`/taxonomy/taxon/${taxid}`)
  }

}

export default new NCBIClientService();
