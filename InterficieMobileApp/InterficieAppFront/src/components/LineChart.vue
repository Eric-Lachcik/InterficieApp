<template>
  <canvas ref="canvas"></canvas>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

const props = defineProps({
  data: {
    type: Object,
    required: true,
    validator: (value) => {
      return !!value.labels && !!value.datasets; // Validación estricta
    }
  },
  options: Object
});

const canvas = ref(null);
let chartInstance = null;

// Destruir gráfico existente
const destroyChart = () => {
  if (chartInstance) {
    chartInstance.destroy();
    chartInstance = null;
  }
};

// Inicializar gráfico
const initChart = () => {
  destroyChart();
  if (canvas.value && props.data.labels?.length) {
    chartInstance = new Chart(canvas.value.getContext('2d'), {
      type: 'line',
      data: props.data,
      options: props.options
    });
  }
};

onMounted(initChart);

// Watcher optimizado para cambios
watch(
  () => props.data,
  (newData) => {
    if (newData.labels?.length) initChart();
  },
  { deep: true }
);

onBeforeUnmount(destroyChart);

</script>

<style scoped>
canvas {
  width: 100% !important;
  height: 100% !important;
}
</style>