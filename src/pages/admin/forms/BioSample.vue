<template>
    <div class="form-elements">
      <div class="row">
        <va-breadcrumbs>
            <va-breadcrumbs-item v-for="(br,index) in breadcrumbs" :key="index" label="One" />        
        </va-breadcrumbs>
        <div class="flex xs12">
            <va-inner-loading :loading="taxonInputLoading">
                <va-card :color="validTaxon?'success':'background-secondary'">
                    <va-card-title>
                        Taxonomy Form
                    </va-card-title>
                    <va-card-content>
                        <va-form @validation="validTaxon = $event" ref="taxonForm">
                            <va-input :disabled="validTaxon" class="mt-3" v-model="newBioSample.taxid" label="NCBI Taxonomy Identifier">
                                <template #append>
                                    <va-button :disabled="!newBioSample.taxid" @click="getTaxon(newBioSample.taxid)">Search Taxon</va-button>
                                </template>
                            </va-input>
                            <va-input class="mt-3" disabled v-model="newBioSample.scientific_name" :rules="[value =>  Boolean(value) || 'Field is mandatory']" label="Scientific name"/>
                            <va-input class="mt-3" :disabled="validTaxon" v-model="newBioSample.name" :rules="[value => Boolean(value) || 'Field is mandatory']" label="BioSample name"/>
                        </va-form>
                    </va-card-content>
                    <va-card-actions align="between">
                        <va-button @click="$refs.taxonForm.validate()">Validate Taxon</va-button>
                        <va-button color="danger" :disabled="!newBioSample.scientific_name" @click="resetTaxon()">Reset Taxon</va-button>
                    </va-card-actions>
                </va-card>
            </va-inner-loading>
        </div>
        <div class="flex xs12">
            <SchemaSelector @on-validation="validateMetadata"/>
        </div>
        <div class="flex lg12 md12 sm12 xs12">
            <va-button :disabled="!validation || !validTaxon" @click="createBioSample()">Create BioSample</va-button>
        </div>
      </div>
      <va-modal v-model="showModal">
        <div v-for="taxon in taxons" :key="taxon.taxid">
            <div class="row justify-space-between align-center">
                <div class="flex">
                    {{ `${taxon.scientific_name} (${taxon.taxid})` }}
                </div>
                <div class="flex">
                    <va-button @click="selectTaxon(taxon)">select</va-button>
                </div>
            </div>
            <va-divider/>
        </div>
      </va-modal>
    </div>
  </template>
  
  <script setup lang="ts">
    import { reactive, ref } from 'vue'
    import { useI18n } from 'vue-i18n'
    import {Breadcrumb,BioSample,Taxon} from './types'
    import {dbStore} from '../../../stores/schemas-store'
    import NCBIClientService from '../../../services/clients/NCBIClientService'
    import SchemaSelector from '../../../components/forms/SchemaSelector.vue'
    import {useRouter} from 'vue-router'

    const steps = ['organism_selection','schema_selection','metadata_form','submission']

    const validation = ref(null)
    
    const validTaxon = ref(null)

    const router = useRouter()

    const selectedSchema = ref({})

    const taxonInputLoading = ref(false)

    const taxons = ref<Taxon[]>([])
    //if 2 request are done we wait 1 second before the next
    const counter = ref(0)

    const showModal = ref(false)

    const SchemaStore = dbStore()

    const newBioSample = ref<BioSample>({
        name:'',
        taxid:9606,
        scientific_name:'',
        schemaId:'',
        metadata:{}
    })
    function createBioSample(){
        console.log(newBioSample)
        SchemaStore.biosamples.push(newBioSample.value)
        router.push({name:'dashboard'})
    }

    function validateMetadata(event, metadata){
        validation.value = event
        if(validation){
            newBioSample.value.metadata = {...metadata}
        }
    }

    async function getTaxon(taxid:number){
        if(counter.value >= 2){
            setTimeout(()=>{},3000)
            counter.value = 0
        }
        try{
            taxonInputLoading.value = true           
            const {data, status} = await NCBIClientService.getTaxon(taxid)
            counter.value++
            if(status == 200){
                const taxonNodes = data.taxonomy_nodes.map(node => {
                    console.log(node)
                    return {
                        taxid: node.taxonomy.tax_id,
                        scientific_name : node.taxonomy.organism_name
                    }
                })
                taxons.value = taxons.value.concat(taxonNodes)
                console.log(taxons.value)
                taxonInputLoading.value = false           
                showModal.value = true
            }

        }
        catch (error){

            console.log(error)
            taxonInputLoading.value = false           

        }
    }
    function selectTaxon(taxon:Taxon){
        const {taxid, scientific_name} = taxon
        newBioSample.value.scientific_name = scientific_name
        newBioSample.value.taxid = taxid
        showModal.value = false
    }
    function resetTaxon(){
        newBioSample.value.scientific_name=''
        newBioSample.value.taxid=0
        validTaxon.value = null
    }
  </script>
  
  <style lang="scss" scoped>
    fieldset {
      margin-bottom: 0.5rem;
    }
    .slide-fade-enter-active {
    transition: all 0.3s ease-out;
    }

    .slide-fade-leave-active {
    transition: all 0.8s cubic-bezier(1, 0.5, 0.8, 1);
    }

    .slide-fade-enter-from,
    .slide-fade-leave-to {
    transform: translateX(20px);
    opacity: 0;
    }
  </style>
  