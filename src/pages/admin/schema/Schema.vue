<template>
    <div class="dashboard">
      <!-- <dashboard-charts />
  
      <dashboard-info-block /> -->
  
      <div class="row row-equal">
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
  