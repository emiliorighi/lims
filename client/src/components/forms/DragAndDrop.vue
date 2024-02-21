<template>
    <div class="drag-drop-container">
        <div class="container-one" v-on:dragover.prevent v-on:drop="handleDrop($event, containerOne)">
            <div class="item" v-for="item in containerOne" :key="item.id" draggable="true"
                v-on:dragstart="handleDragStart($event, item)">
                <va-chip>{{ item.text }}</va-chip>
            </div>
        </div>
        <div class="container-two" v-on:dragover.prevent v-on:drop="handleDrop($event, containerTwo)">
            <div class="item" v-for="item in containerTwo" :key="item.id" draggable="true"
                v-on:dragstart="handleDragStart($event, item)">
                <va-chip>{{ item.text }}</va-chip>
            </div>
        </div>
    </div>
</template>
<script setup>
import { ref } from 'vue';

const item1 = {
    id: 1,
    text: 'Item 1'
};
const item2 = {
    id: 2,
    text: 'Item 2'
};

let containerOne = ref([item1, item2])
let containerTwo = ref([])

const handleDragStart = (event, itemData) => {
    event.dataTransfer.setData('application/json', JSON.stringify(itemData));
};

const handleDrop = (event, targetContainer) => {
    const itemData = JSON.parse(event.dataTransfer.getData('application/json'));

    if (targetContainer === containerOne.value) {
        containerTwo.value = containerTwo.value.filter(i => i.id !== itemData.id);
    } else if (targetContainer === containerTwo.value) {
        containerOne.value = containerOne.value.filter(i => i.id !== itemData.id);
    }
    targetContainer.push(itemData);
};
</script>



<style scoped>
.drag-drop-container {
    display: flex;
}

.container-one,
.container-two {
    border: 1px solid #1a1a1a;
    width: 600px;
    height: 800px;
    padding: 10px;
}

.item {
    padding: 10px;
    background-color: black;
    color: white;
    cursor: pointer;
    width: 90%;
}
</style>