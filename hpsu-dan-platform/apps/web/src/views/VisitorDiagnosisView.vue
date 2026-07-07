<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../api'
import { useAuthStore } from '../stores/auth'
import DiagnosisEvidence from '../components/DiagnosisEvidence.vue'
import FaultProbabilityChart from '../components/FaultProbabilityChart.vue'
import HealthScoreGauge from '../components/HealthScoreGauge.vue'
import MaintenanceSuggestionCard from '../components/MaintenanceSuggestionCard.vue'
import VisitorDiagnosisFlow from '../components/VisitorDiagnosisFlow.vue'
import { useDiagnosisStore } from '../stores/diagnosis'

const auth = useAuthStore()
const router = useRouter()
const diagnosis = useDiagnosisStore()
const loading = ref(false)
const uploading = ref(false)
const error = ref('')
const result = ref<any>(null)
const quality = ref<any>(null)
const tasks = ref<any[]>([])
const selectedFile = ref<File | null>(null)
const showAdvanced = ref(false)
const selectedTask = ref<any>(null)
const navigating = ref(false)

const isAdmin = computed(() => auth.user?.role === 'admin')
const probabilities = computed(() => result.value?.topk || [
  { label: diagnosis.current.code, label_en: diagnosis.current.labelEn, probability: diagnosis.current.confidence },
])
const flowActive = computed(() => Boolean(result.value))

function goTwinSoon() {
  navigating.value = true
  window.setTimeout(() => router.push('/digital-twin'), 900)
}

function sampleSignal() {
  return Array.from({ length: 2048 }, (_, i) => 0.24 * Math.sin(i * 0.17) + (i % 137 === 0 ? 1.4 : 0))
}

async function loadTasks() {
  if (!isAdmin.value) return
  tasks.value = await api('/tasks?limit=8')
}

async function runSampleDiagnosis() {
  loading.value = true
  error.value = ''
  try {
    result.value = await api('/diagnosis/predict', {
      method: 'POST',
      body: JSON.stringify({ samples: sampleSignal(), sampling_rate: 25600, model_id: 'hpsu-dan-v1' }),
    })
    quality.value = null
    diagnosis.applyResult(result.value)
    await loadTasks()
    goTwinSoon()
  } catch (exc: any) {
    error.value = exc?.message || 'DIAGNOSIS_FAILED'
  } finally {
    loading.value = false
  }
}

function chooseFile(event: Event) {
  const input = event.target as HTMLInputElement
  selectedFile.value = input.files?.[0] || null
}

async function uploadAndDiagnose() {
  if (!selectedFile.value) return
  uploading.value = true
  error.value = ''
  try {
    const body = new FormData()
    body.set('file', selectedFile.value)
    body.set('sampling_rate', '25600')
    body.set('model_id', 'hpsu-dan-v1')
    const payload = await api<any>('/diagnosis/upload', { method: 'POST', body })
    result.value = payload.result
    quality.value = payload.quality
    if (payload.result) diagnosis.applyResult(payload.result)
    await loadTasks()
    if (payload.result) goTwinSoon()
  } catch (exc: any) {
    error.value = exc?.message || 'UPLOAD_DIAGNOSIS_FAILED'
  } finally {
    uploading.value = false
  }
}

async function openTask(task: any) {
  selectedTask.value = await api(`/tasks/${task.task_id}`)
  if (selectedTask.value?.result) {
    result.value = selectedTask.value.result
    diagnosis.applyResult(selectedTask.value.result)
  }
}

async function rerunTask(task: any) {
  loading.value = true
  error.value = ''
  try {
    const payload = await api<any>(`/tasks/${task.task_id}/rerun`, { method: 'POST' })
    selectedTask.value = payload.task
    result.value = payload.result
    if (payload.result) diagnosis.applyResult(payload.result)
    await loadTasks()
  } catch (exc: any) {
    error.value = exc?.message || 'RERUN_FAILED'
  } finally {
    loading.value = false
  }
}

onMounted(() => loadTasks().catch(() => undefined))
</script>

<template>
  <section class="visitor-diagnosis">
    <div class="page-title">
      <div>
        <p class="eyebrow">INTELLIGENT FAULT DIAGNOSIS</p>
        <h1>Industrial Diagnosis Workflow</h1>
        <p>Upload vibration data or run a built-in signal. The system checks quality, analyzes evidence, identifies the fault and gives maintenance advice.</p>
      </div>
      <button class="primary action" :disabled="loading" @click="runSampleDiagnosis">
        {{ navigating ? 'Opening twin...' : loading ? 'Diagnosing...' : 'Start live diagnosis' }}
      </button>
    </div>

    <p v-if="error" class="error-box">{{ error }}</p>

    <div class="visitor-layout">
      <article class="signal-entry glass-panel">
        <p class="eyebrow">SIGNAL INPUT</p>
        <h2>Vibration signal</h2>
        <input type="file" accept=".csv,.txt" @change="chooseFile" />
        <div class="signal-file">
          <span>{{ selectedFile?.name || 'No uploaded file' }}</span>
          <b>{{ quality?.score ? `Quality ${quality.score}` : 'Ready' }}</b>
        </div>
        <button class="primary action" :disabled="uploading || !selectedFile" @click="uploadAndDiagnose">
          {{ uploading ? 'Analyzing...' : 'Upload and analyze' }}
        </button>
      </article>

      <VisitorDiagnosisFlow :active="flowActive" :severity="diagnosis.current.riskLevel" />
    </div>

    <div class="visitor-result-grid">
      <HealthScoreGauge :score="diagnosis.current.healthScore" :confidence="diagnosis.current.confidence" :risk="diagnosis.current.riskLevel" />
      <FaultProbabilityChart :items="probabilities" />
      <MaintenanceSuggestionCard :target="diagnosis.current.twinTarget" :suggestion="diagnosis.current.suggestionEn" :quality="quality" />
    </div>

    <DiagnosisEvidence
      :waveform-mode="diagnosis.current.waveformMode"
      :markers="diagnosis.current.spectrumMarkers"
      :waveform="diagnosis.current.waveformPoints"
      :spectrum="diagnosis.current.spectrumPoints"
    />

    <details v-if="isAdmin" class="advanced-admin glass-panel" :open="showAdvanced" @toggle="showAdvanced = ($event.target as HTMLDetailsElement).open">
      <summary>Advanced task trace</summary>
      <div class="history-row history-head"><span>ID</span><span>TYPE</span><span>STATUS</span><span>MODEL</span></div>
      <div v-for="task in tasks" :key="task.task_id" class="history-row" @click="openTask(task)">
        <code>{{ task.task_id.slice(-10) }}</code>
        <span>{{ task.task_type }}</span>
        <span>{{ task.status }}</span>
        <b>{{ task.model_id || '--' }}</b>
      </div>
      <div v-if="selectedTask" class="warning-text">
        <strong>Selected:</strong> {{ selectedTask.task_id }} / {{ selectedTask.status }}
        <button class="ghost" :disabled="!selectedTask.input_file_id || loading" @click="rerunTask(selectedTask)">Rerun</button>
      </div>
    </details>
  </section>
</template>
