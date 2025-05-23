<template>
    <div class="professional-calendar">
        <div v-if="loading" class="loading">Cargando disponibilidad...</div>
        <div v-else-if="availableSlots.length === 0" class="no-slots">
            No hay horarios disponibles para mañana
        </div>
        <div v-else>
            <h4>Horarios disponibles para mañana</h4>
            <div class="calendar-grid">
                <div v-for="slot in filteredSlots" :key="slot.toISOString()" class="time-slot"
                    :class="{ selected: isSlotSelected(slot) }" @click="selectSlot(slot)">
                    {{ formatSlot(slot) }}
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { api } from 'boot/axios'


const availableSlots = ref([])
const loading = ref(false)
const selectedSlot = ref(null)
const props = defineProps({
    professionalId: {
        type: Number,
        required: true
    }
})
const emit = defineEmits(['slot-selected'])
onMounted(async () => {
    await fetchAvailability()
})

watch(() => props.professionalId, async () => {
    await fetchAvailability()
})

const filteredSlots = computed(() => {
  return availableSlots.value.filter(slot => {
    const hour = new Date(slot).getHours()
    return hour >= 9 && hour <= 20
  })
})

const fetchAvailability = async () => {
  try {
    loading.value = true
    const response = await api.get(`/api/availability/${props.professionalId}/`)
    availableSlots.value = response.data.available_slots
      .map(s => new Date(s))
      .sort((a, b) => a - b)
    
    selectedSlot.value = null
  } catch (error) {
    console.error('Error cargando disponibilidad:', error)
    alert('Error al cargar horarios disponibles')
  } finally {
    loading.value = false
  }
}

const formatSlot = (datetime) => {
  return datetime.toLocaleTimeString('es-ES', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  })
}

const selectSlot = (slot) => {
  selectedSlot.value = slot
  
  // Convertir a hora local correctamente
  const localDate = new Date(slot.getTime() - (slot.getTimezoneOffset() * 60000))
  
  // Formatear para input datetime-local (YYYY-MM-DDTHH:mm)
  const formattedDateTime = localDate.toISOString().slice(0, 16)
  
  emit('slot-selected', formattedDateTime)
}

const isSlotSelected = (slot) => {
  return selectedSlot.value?.getTime() === slot.getTime()
}
</script>

<style scoped>
.professional-calendar {
    margin: 20px 0;
    padding: 15px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.loading {
    text-align: center;
    padding: 20px;
    color: #666;
}

.no-slots {
  color: #666;
  padding: 15px;
  text-align: center;
}

.calendar-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
    gap: 10px;
    margin-top: 15px;
}

.time-slot {
    padding: 10px;
    border: 2px solid #2A5C8D;
    border-radius: 8px;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s ease;
    background: white;
    color: #2A5C8D;
}

.time-slot:hover {
    background: #2A5C8D;
    color: white;
}

.time-slot.selected {
    background: #2A5C8D;
    color: white;
    border-color: #1a3a5a;
}

h4 {
    color: #2A5C8D;
    margin-bottom: 15px;
    font-size: 1.1rem;
}
</style>