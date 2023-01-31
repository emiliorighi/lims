<template>
    <div class="dashboard">
      <!-- <dashboard-charts />
  
      <dashboard-info-block /> -->
  
      <div class="row align-center row-equal">
        <div class="flex lg6 md6 sm6 xs6">
          <div class="row justify-space-between">
            <div v-for="model in models" :key="model.name" class="flex lg6 md6 sm6 xs6">
              <va-card  :color="model.color">
                <va-card-title>{{ model.name }}</va-card-title>
                <va-card-content>
                  <div class="row justify-space-between">
                    <div class="flex">
                      {{ model.description }}
                    </div>
                    <div class="flex">
                      <va-button>Create a new {{ model.name }}</va-button>
                    </div>
                  </div>
                </va-card-content>
              </va-card>
            </div>
          </div>
        </div>
        <va-image :ratio="4/3"  class="flex lg6 md6 sm6 xs6" src="/model.svg"></va-image>
  
        <div class="flex xs12 lg6">
          <!-- <dashboard-tabs @submit="addAddressToMap" /> -->
        </div>
  
        <div class="flex xs12 lg6">
          <!-- <DashboardMap ref="dashboardMap" /> -->
        </div>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
    import { dbStore } from '../../../stores/schemas-store'
  
  
  
    const DB = dbStore()
    
    const models = [
      // {
      //   name: 'Schema',
      //   description: 'Metadata schema',
      //   db:'schemas',
      //   color: 'info'
      // },
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
  