<template>
  <div class="dashboard">
    <!-- <dashboard-charts />

    <dashboard-info-block /> -->

    <div class="row align-center row-equal">
      <div class="flex lg6 md6 sm12 xs12">
        <div class="row justify-space-between">
          <div v-for="model in models" :key="model.name" class="flex lg12 md12 sm12 xs12">
            <va-card  :color="model.color">
              <va-card-title>
                <div class="row justify-space-between align-center">
                  <div class="flex">
                    {{ model.name }}
                  </div>
                  <div class="flex">
                    <va-button size="small" :to="{name:model.db}">Create a new {{ model.name }}</va-button>
                  </div>
                </div>
              </va-card-title>
              <va-card-content>
                <va-data-table :items="DB[model.db]">
                  <template #cell(metadata)="data">
                    <va-button size="small" @click="showMetadata(data)" icon="search"/>
                  </template>
                  <template #cell(url)="data">
                    <a :href="data.value" icon="search">{{ data.value }}</a>
                  </template>
                </va-data-table>
              </va-card-content>
            </va-card>
          </div>
        </div>
      </div>
      <va-image :ratio="4/3"  class="flex lg6 md6 sm6 xs6" src="/model.svg"></va-image>

    </div>
  </div>
</template>

<script setup lang="ts">
  import { dbStore } from '../../../stores/schemas-store'



  const DB = dbStore()
  
  const models = [
    {
      name: 'Experiment',
      description: 'Sequencing data',
      db:'experiments',
      color: '#f6b26b'
    },    
    {
      name: 'BioSample',
      description: 'Sequenced biomaterial',
      db:'biosamples',
      color: '#6aa84f'
    },    
    {
      name: 'Analysis',
      description: 'Data generated from sequencing data processing',
      db:'analysis',
      color: '#76a5af'
    },     
    {
      name: 'File',
      description: 'Link to data files',
      db:'files',
      color: '#eeeeee'
    }, 
  ]

  function showMetadata(data){
    console.log(data.value)
  }

</script>

<style lang="scss">
  .row-equal .flex {
    .va-card {
      height: 100%;
    }
  }

  .dashboard {
    .va-card {
      margin-bottom: 0 !important;
      &__title {
        display: flex;
        justify-content: space-between;
      }
    }
  }
</style>
