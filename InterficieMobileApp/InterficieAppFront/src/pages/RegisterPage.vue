<template>
<div class="register-container">
    <div class="register-content">
      <!-- Encabezado -->
      <div class="text-center q-mb-xl">
        <img 
          src="FITCOREV2.2.png" 
          class="register-logo q-mb-md"
          alt="FITCORE Logo"
        />
        <div class="text-h4 text-weight-bold text-primary q-mb-sm">Registro de Cliente</div>
      </div>

      <!-- Formulario -->
      <q-form @submit.prevent="handleRegister" class="q-gutter-y-md">
        <!-- Sección Información Personal -->
        <div class="section-title text-h6 text-weight-medium">Información Personal</div>
        <div class="row q-col-gutter-md">
          <div class="col-6">
            <q-input
              v-model="formData.name"
              outlined
              label="Nombre *"
              :rules="[val => !!val || 'Campo obligatorio']"
            />
          </div>
          <div class="col-6">
            <q-input
              v-model="formData.surname"
              outlined
              label="Apellidos *"
              :rules="[val => !!val || 'Campo obligatorio']"
            />
          </div>
        </div>

        <div class="row q-col-gutter-md">
          <div class="col-6">
            <q-input
              v-model="formData.dni"
              outlined
              label="DNI *"
              mask="########X"
              :rules="[val => !!val || 'DNI requerido']"
            />
          </div>
          <div class="col-6">
            <q-input
              v-model="formData.phone"
              outlined
              label="Teléfono *"
              mask="##########"
              :rules="[val => val.length === 9 || 'Número inválido']"
            />
          </div>
        </div>

        <!-- Sección Dirección -->
        <div class="section-title text-h6 text-weight-medium">Dirección</div>
        <div class="row q-col-gutter-md">
          <div class="col-8">
            <q-input
              v-model="formData.address"
              outlined
              label="Dirección"
            />
          </div>
          <div class="col-4">
            <q-input
              v-model="formData.population"
              outlined
              label="Población"
            />
          </div>
        </div>

        <!-- Sección Credenciales -->
        <div class="section-title text-h6 text-weight-medium">Credenciales</div>
        <div class="row q-col-gutter-md">
          <div class="col-6">
            <q-input
              v-model="formData.username"
              outlined
              label="Nombre de usuario *"
              :rules="[val => !!val || 'Campo obligatorio']"
            />
          </div>
          <div class="col-6">
            <q-input
              v-model="formData.email"
              outlined
              label="Email"
              type="email"
            />
          </div>
        </div>

        <div class="row q-col-gutter-md">
          <div class="col-6">
            <q-input
              v-model="formData.password"
              outlined
              type="password"
              label="Contraseña *"
              :rules="[val => val.length >= 8 || 'Mínimo 8 caracteres']"
            />
          </div>
        </div>

        <!-- Sección Datos Físicos -->
        <div class="section-title text-h6 text-weight-medium">Datos Físicos</div>
        <div class="row q-col-gutter-md">
          <div class="col-4">
            <q-input
              v-model="formData.weight"
              outlined
              type="number"
              label="Peso (kg)"
              step="0.1"
            />
          </div>
          <div class="col-4">
            <q-input
              v-model="formData.stature"
              outlined
              type="number"
              label="Altura (m)"
              step="0.01"
            />
          </div>
          <div class="col-4">
            <q-input
              v-model="formData.muscle_mass"
              outlined
              type="number"
              label="Masa muscular (kg)"
              step="0.1"
            />
          </div>
        </div>

        <!-- Selectores de Profesionales -->
        <div class="section-title text-h6 text-weight-medium">Asignación de Profesionales</div>
        <div class="row q-col-gutter-md">
          <div class="col-6">
            <q-select
                v-model="formData.entrenador"
                :options="trainers"
                label="Seleccione su entrenador"
                option-label="full_name"
                option-value="id" 
                map-options
                emit-value 
                clearable
            >
              <template v-slot:option="scope">
                <q-item v-bind="scope.itemProps">
                  <q-item-section>
                    <q-item-label>{{ scope.opt.full_name }}</q-item-label>
                    <q-item-label caption>{{ scope.opt.email }}</q-item-label>
                  </q-item-section>
                </q-item>
              </template>
            </q-select>
          </div>
          
          <div class="col-6">
            <q-select
                v-model="formData.nutricionista"
                :options="nutritionists"
                label="Seleccione su nutricionista"
                option-label="full_name"
                option-value="id" 
                map-options
                emit-value 
                clearable
            >
              <template v-slot:option="scope">
                <q-item v-bind="scope.itemProps">
                  <q-item-section>
                    <q-item-label>{{ scope.opt.full_name }}</q-item-label>
                    <q-item-label caption>{{ scope.opt.email }}</q-item-label>
                  </q-item-section>
                </q-item>
              </template>
            </q-select>
          </div>
        </div>

        <!-- Sección Pago -->
        <div class="section-title text-h6 text-weight-medium">Plan de Pago</div>
        <div class="row q-col-gutter-md">
          <div class="col-6">
            <q-radio 
              v-model="formData.paymentType" 
              val="anual" 
              label="Pago Anual 1000€" 
            />
          </div>
          <div class="col-6">
            <q-radio 
              v-model="formData.paymentType" 
              val="mensual" 
              label="Pago Mensual 100€" 
            />
          </div>
        </div>

        <!-- Botón de Registro -->
        <q-btn 
          type="submit"
          label="Registrarse"
          class="full-width q-mt-lg"
          color="primary"
          size="lg"
        />

        <!-- Enlace a Login -->
        <div class="text-center q-mt-md">
          <q-btn 
            flat 
            color="primary" 
            label="¿Ya tienes cuenta? Inicia Sesión" 
            @click="$router.push('/login')" 
          />
        </div>
      </q-form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import { api } from 'boot/axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const $q = useQuasar()

const formData = ref({
  name: '',
  surname: '',
  dni: '',
  phone: '',
  address: '',
  population: '',
  username: '',
  password: '',
  email: '',
  weight: null,
  stature: null,
  muscle_mass: null,
  role: 'cliente',
  paymentType: 'mensual',
  entrenador: null,
  nutricionista: null
})

const trainers = ref([])
const nutritionists = ref([])

onMounted(async () => {
  try {
    const [trainersRes, nutritionistsRes] = await Promise.all([
      api.get('/api/trainers/'),
      api.get('/api/nutritionists/')
    ])
    
    trainers.value = trainersRes.data.map(t => ({
      ...t,
      full_name: `${t.name} ${t.surname}`
    }))
    
    nutritionists.value = nutritionistsRes.data.map(n => ({
      ...n,
      full_name: `${n.name} ${n.surname}`
    }))
    
  } catch {
    $q.notify({
      type: 'negative',
      message: 'Error cargando profesionales disponibles',
      position: 'top'
    })
  }
})

const handleRegister = async () => {
  try {
    // Validación básica
    if (!formData.value.password) {
      throw new Error('La contraseña es obligatoria')
    }

    const payload = {
      ...formData.value,
      staff: false,
      // Asegurar que solo enviamos los IDs
      entrenador: formData.value.entrenador?.id || formData.value.entrenador,
      nutricionista: formData.value.nutricionista?.id || formData.value.nutricionista
    }

    await api.post('/api/auth/register/', payload)
    
    $q.notify({
      type: 'positive',
      message: 'Registro exitoso! Redirigiendo...',
      position: 'top'
    })
    
    setTimeout(() => {
      router.push('/login')
    }, 2000)
    
  } catch (error) {
    const errorMessage = error.response?.data?.detail || 
                        error.response?.data?.message || 
                        'Error en el registro'
    
    $q.notify({
      type: 'negative',
      message: errorMessage,
      position: 'top'
    })
  }
}
</script>
<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #F0EEF8;
  padding: 16px;
}

.register-content {
  width: 100%;
  max-width: 800px;
  background: #F0EEF8;
  border-radius: 15px;
  padding: 40px;
}

.section-title {
  color: #2A5C8D;
  margin: 25px 0 15px;
  padding-bottom: 8px;
  border-bottom: 2px solid #eee;
}

.register-logo {
  height: 180px;
  max-width: 80%;
}

@media (max-width: 600px) {
  .register-content {
    padding: 20px;
  }
  
  .register-logo {
    height: 140px;
  }
  
  .section-title {
    font-size: 1.1rem;
  }
}
</style>