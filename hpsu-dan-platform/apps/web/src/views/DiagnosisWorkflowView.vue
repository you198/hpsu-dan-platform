<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { api } from '../api'
import DiagnosisEvidence from '../components/DiagnosisEvidence.vue'
import { useDiagnosisStore } from '../stores/diagnosis'

const diagnosis = useDiagnosisStore()
const loading = ref(false)
const uploading = ref(false)
const error = ref('')
const result = ref<any>(null)
const quality = ref<any>(null)
const history = ref<any[]>([])
const tasks = ref<any[]>([])
const compute = ref<any>(null)
const selectedTask = ref<any>(null)
const selectedFile = ref<File | null>(null)

function signal() {
  return Array.from({ length: 2048 }, (_, i) => 0.24 * Math.sin(i * 0.17) + (i % 137 === 0 ? 1.4 : 0))
}

async function loadHistory() {
  history.value = await api('/diagnosis/history?limit=8')
}

async function loadTasks() {
  tasks.value = await api('/tasks?limit=8')
}

async function loadCompute() {
  compute.value = await api('/compute/status')
}

async function refreshLists() {
  await Promise.all([loadHistory(), loadTasks(), loadCompute()])
}

async function runDemoSignal() {
  loading.value = true
  error.value = ''
  try {
    result.value = await api('/diagnosis/predict', {
      method: 'POST',
      body: JSON.stringify({ samples: signal(), sampling_rate: 25600, model_id: 'hpsu-dan-v1' }),
    })
    quality.value = null
    diagnosis.applyResult(result.value)
    await refreshLists()
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
    await refreshLists()
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
    await refreshLists()
  } catch (exc: any) {
    error.value = exc?.message || 'RERUN_FAILED'
  } finally {
    loading.value = false
  }
}

onMounted(() => refreshLists().catch(() => undefined))
</script>

<template>
  <section>
    <div class="page-title">
      <div>
        <p class="eyebrow">STAGE 3-4 / REAL MODEL WORKFLOW</p>
        <h1>Diagnosis Evidence & Task Center</h1>
        <p>Real inference, evidence package, CSV/TXT upload and traceable task records.</p>
      </div>
      <button class="primary action" :disabled="loading" @click="runDemoSignal">
        {{ loading ? 'Diagnosing...' : 'Run sample diagnosis' }}
      </button>
    </div>

    <p v-if="error" class="error-box">{{ error }}</p>

    <div class="result-grid">
      <article class="glass-panel result-main">
        <p class="eyebrow">UPLOAD DIAGNOSIS</p>
        <h2>CSV / TXT signal workflow</h2>
        <p class="warning-text">Upload a single-channel vibration signal. The backend validates quality, slices a 1024-point window, creates a task and calls the real inference service.</p>
        <input type="file" accept=".csv,.txt" @change="chooseFile" />
        <div class="score-row">
          <div>
            <small>Selected file</small>
            <strong>{{ selectedFile?.name || 'None' }}</strong>
          </div>
          <div>
            <small>Quality score</small>
            <strong>{{ quality?.score ?? '--' }}</strong>
          </div>
        </div>
        <button class="primary action" :disabled="uploading || !selectedFile" @click="uploadAndDiagnose">
          {{ uploading ? 'Uploading...' : 'Upload and diagnose' }}
        </button>
      </article>

      <article class="glass-panel topk">
        <p class="eyebrow">CURRENT RESULT / COMPUTE</p>
        <h2>{{ diagnosis.current.labelEn }}</h2>
        <div class="score-row">
          <div>
            <small>Confidence</small>
            <strong>{{ (diagnosis.current.confidence * 100).toFixed(1) }}%</strong>
          </div>
          <div>
            <small>Health</small>
            <strong>{{ diagnosis.current.healthScore }}</strong>
          </div>
        </div>
        <code>target={{ diagnosis.current.twinTarget }}</code>
        <code>engine={{ diagnosis.current.engineMode }}</code>
        <code>version={{ diagnosis.current.modelVersion }}</code>
        <code>gpu={{ compute?.gpu_available ? 'available' : 'unavailable' }}</code>
        <code>queue={{ compute?.queues?.gpu_inference_queue?.status || '--' }}</code>
      </article>
    </div>

    <DiagnosisEvidence
      :waveform-mode="diagnosis.current.waveformMode"
      :markers="diagnosis.current.spectrumMarkers"
      :waveform="diagnosis.current.waveformPoints"
      :spectrum="diagnosis.current.spectrumPoints"
    />

    <div class="result-grid">
      <article class="glass-panel history-card">
        <p class="eyebrow">TASK CENTER</p>
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
      </article>

      <article class="glass-panel history-card">
        <p class="eyebrow">DIAGNOSIS HISTORY</p>
        <div class="history-row history-head"><span>ID</span><span>USER</span><span>LABEL</span><span>CONF</span></div>
        <div v-for="item in history" :key="item.task_id" class="history-row">
          <code>{{ item.task_id.slice(-10) }}</code>
          <span>{{ item.requested_by }}</span>
          <span>{{ item.label }}</span>
          <b>{{ (item.confidence * 100).toFixed(1) }}%</b>
        </div>
      </article>
    </div>
  </section>
</template>
