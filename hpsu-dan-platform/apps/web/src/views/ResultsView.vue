<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../api'
import { useDiagnosisStore } from '../stores/diagnosis'

type ResearchOptions = {
  datasets: Record<string, any>
  transfer_tasks: Record<string, Record<string, any>>
  methods: Record<string, any>
  results: any[]
  summary?: any
}

const loading = ref(false)
const error = ref('')
const options = ref<ResearchOptions | null>(null)
const selectedDataset = ref('PU')
const selectedTask = ref('S3_to_N15M01F10')
const selectedMethod = ref('HPSU-DAN')
const selectedResultId = ref('')
const selectedDetail = ref<any>(null)
const router = useRouter()
const diagnosis = useDiagnosisStore()

const datasets = computed(() => Object.keys(options.value?.datasets || {}))
const tasks = computed(() => Object.keys(options.value?.transfer_tasks?.[selectedDataset.value] || {}))
const methods = computed(() => Object.keys(options.value?.methods || {}))
const filteredResults = computed(() => (options.value?.results || []).filter((item) => {
  return item.dataset === selectedDataset.value && item.task_id === selectedTask.value && item.method === selectedMethod.value
}))
const methodsForTask = computed(() => {
  const names = (options.value?.results || [])
    .filter((item) => item.dataset === selectedDataset.value && item.task_id === selectedTask.value)
    .map((item) => item.method)
  return [...new Set(names)]
})
const currentTask = computed(() => options.value?.transfer_tasks?.[selectedDataset.value]?.[selectedTask.value])
const currentDataset = computed(() => options.value?.datasets?.[selectedDataset.value])
const currentResult = computed(() => selectedDetail.value || filteredResults.value[0])
const summary = computed(() => options.value?.summary || {})
const resultAssets = computed(() => currentResult.value?.assets || {})
const diagnosisExample = computed(() => currentResult.value?.diagnosis_example || {})
const reportSummary = computed(() => [
  `数据集 ${currentResult.value?.dataset}，迁移任务 ${currentResult.value?.task_id}`,
  `方法 ${currentResult.value?.method} / ${currentResult.value?.implementation}`,
  `诊断示例 ${diagnosisExample.value?.label_zh || diagnosisExample.value?.label_en}`,
  `3D twin 定位 ${diagnosisExample.value?.twin_target}`,
  `频谱 marker ${diagnosisExample.value?.markers?.join(', ') || '--'}`,
])

function syncDefaults() {
  if (!datasets.value.includes(selectedDataset.value)) selectedDataset.value = datasets.value[0] || ''
  if (!tasks.value.includes(selectedTask.value)) selectedTask.value = tasks.value[0] || ''
  if (!methodsForTask.value.includes(selectedMethod.value)) selectedMethod.value = methodsForTask.value[0] || methods.value[0] || ''
  const first = filteredResults.value[0]
  selectedResultId.value = first?.result_id || ''
  selectedDetail.value = first || null
}

async function syncDefaultsAndLoad() {
  syncDefaults()
  if (selectedResultId.value) await loadResult(selectedResultId.value)
}

async function loadOptions() {
  loading.value = true
  error.value = ''
  try {
    options.value = await api<ResearchOptions>('/research/options')
    await syncDefaultsAndLoad()
  } catch (exc: any) {
    error.value = exc?.message || 'RESEARCH_OPTIONS_FAILED'
  } finally {
    loading.value = false
  }
}

async function loadResult(resultId = selectedResultId.value) {
  if (!resultId) return
  error.value = ''
  try {
    selectedResultId.value = resultId
    selectedDetail.value = await api(`/research/results/${resultId}`)
  } catch (exc: any) {
    error.value = exc?.message || 'RESEARCH_RESULT_FAILED'
  }
}

function onDatasetChange() {
  selectedTask.value = Object.keys(options.value?.transfer_tasks?.[selectedDataset.value] || {})[0] || ''
  selectedDetail.value = null
  syncDefaultsAndLoad()
}

function onTaskOrMethodChange() {
  selectedDetail.value = null
  syncDefaultsAndLoad()
}

async function openTwinWithResult() {
  if (!currentResult.value) return
  let detail = currentResult.value
  if (!detail.diagnosis_result && selectedResultId.value) {
    detail = await api(`/research/results/${selectedResultId.value}`)
  }
  diagnosis.applyResult(detail.diagnosis_result)
  router.push('/digital-twin')
}

onMounted(loadOptions)
</script>

<template>
  <section class="results-page">
    <div class="page-title">
      <div>
        <p class="eyebrow">COMPLETED EXPERIMENT RESULTS</p>
        <h1>已完成模型结果</h1>
        <p>普通用户在这里选择数据集、迁移任务和方法，加载真实实验目录中的已完成模型结果，不重新训练、不占用 GPU。</p>
      </div>
      <span class="online-pill"><i></i>{{ options?.results?.length || 0 }} real runs</span>
    </div>

    <p v-if="error" class="error-box">{{ error }}</p>

    <div class="research-stats">
      <span><small>真实实验结果</small><strong>{{ summary.result_count || 0 }}</strong></span>
      <span><small>HPSU-DAN 主模型</small><strong>{{ summary.methods?.['HPSU-DAN'] || 0 }}</strong></span>
      <span><small>PU / SDUST</small><strong>{{ summary.datasets?.PU || 0 }} / {{ summary.datasets?.SDUST || 0 }}</strong></span>
      <span><small>当前组合 run</small><strong>{{ filteredResults.length }}</strong></span>
    </div>

    <div class="research-selector glass-panel">
      <label>
        <span>数据集</span>
        <select v-model="selectedDataset" @change="onDatasetChange">
          <option v-for="item in datasets" :key="item" :value="item">{{ item }}</option>
        </select>
      </label>
      <label>
        <span>迁移任务</span>
        <select v-model="selectedTask" @change="onTaskOrMethodChange">
          <option v-for="item in tasks" :key="item" :value="item">{{ item }}</option>
        </select>
      </label>
      <label>
        <span>方法</span>
        <select v-model="selectedMethod" @change="onTaskOrMethodChange">
          <option v-for="item in methodsForTask" :key="item" :value="item">{{ item }}</option>
        </select>
      </label>
      <label>
        <span>已完成运行</span>
        <select v-model="selectedResultId" @change="loadResult()">
          <option v-for="item in filteredResults" :key="item.result_id" :value="item.result_id">{{ item.run_id }}</option>
        </select>
      </label>
    </div>

    <div v-if="loading" class="empty-panel glass-panel">Loading research registry...</div>

    <div v-else-if="currentResult" class="research-result-layout">
      <article class="research-card glass-panel result-hero-card">
        <p class="eyebrow">RESULT SNAPSHOT</p>
        <h2>{{ currentResult.title }}</h2>
        <div class="result-meta-grid">
          <span><small>Dataset</small><strong>{{ currentResult.dataset }}</strong></span>
          <span><small>Task</small><strong>{{ currentResult.task_id }}</strong></span>
          <span><small>Method</small><strong>{{ currentResult.method }}</strong></span>
          <span><small>Run</small><strong>{{ currentResult.run_id }}</strong></span>
          <span><small>Source</small><strong>{{ currentResult.source || 'registry' }}</strong></span>
          <span><small>Implementation</small><strong>{{ currentResult.implementation }}</strong></span>
        </div>
        <p class="result-note">该页面加载已完成实验资产，适合访客与评委查看稳定结果；重新训练、参数调节和算法细节后续放入科研实验中心。</p>
        <button class="primary action" @click="openTwinWithResult">进入 3D twin 联动展示</button>
      </article>

      <article class="research-card glass-panel">
        <p class="eyebrow">TRANSFER TASK</p>
        <h3>{{ selectedTask }}</h3>
        <div class="domain-row">
          <div>
            <small>Source domains</small>
            <b>{{ currentTask?.source_domains?.join(' + ') }}</b>
          </div>
          <strong>→</strong>
          <div>
            <small>Target domain</small>
            <b>{{ currentTask?.target_domain }}</b>
          </div>
        </div>
        <p>{{ currentDataset?.name }}</p>
      </article>

      <article class="research-card glass-panel">
        <p class="eyebrow">MODEL PERFORMANCE</p>
        <div class="metric-line">
          <span>Accuracy</span>
          <b>{{ currentResult.metrics?.accuracy ?? 'Pending asset' }}</b>
        </div>
        <div class="metric-line">
          <span>Macro F1</span>
          <b>{{ currentResult.metrics?.macro_f1 ?? 'Pending asset' }}</b>
        </div>
        <div class="metric-line">
          <span>Model version</span>
          <b>{{ currentResult.model_version }}</b>
        </div>
        <div class="metric-line">
          <span>Precision</span>
          <b>{{ currentResult.metrics?.precision_macro ?? '--' }}</b>
        </div>
        <div class="metric-line">
          <span>Recall</span>
          <b>{{ currentResult.metrics?.recall_macro ?? '--' }}</b>
        </div>
      </article>

      <article class="research-card glass-panel diagnosis-example-card">
        <p class="eyebrow">DIAGNOSIS EXAMPLE</p>
        <h3>{{ diagnosisExample?.label_zh || diagnosisExample?.label_en }}</h3>
        <div class="result-meta-grid compact">
          <span><small>Code</small><strong>{{ diagnosisExample?.code }}</strong></span>
          <span><small>Twin target</small><strong>{{ diagnosisExample?.twin_target }}</strong></span>
          <span><small>Markers</small><strong>{{ diagnosisExample?.markers?.join(', ') }}</strong></span>
          <span><small>Health</small><strong>{{ diagnosisExample?.health_score }}</strong></span>
        </div>
      </article>

      <article class="research-card glass-panel diagnosis-evidence-card">
        <p class="eyebrow">DIAGNOSIS EVIDENCE CHAIN</p>
        <h3>结果概览 -> 诊断证据 -> 数字孪生 -> 维护建议</h3>
        <div class="evidence-chain">
          <span>结果概览</span>
          <b>-></b>
          <span>混淆矩阵</span>
          <b>-></b>
          <span>训练曲线</span>
          <b>-></b>
          <span>特征投影</span>
          <b>-></b>
          <span>3D 高亮</span>
          <b>-></b>
          <span>报告摘要</span>
        </div>
        <div class="report-summary">
          <p v-for="line in reportSummary" :key="line">{{ line }}</p>
        </div>
      </article>

      <article class="research-card glass-panel asset-card">
        <p class="eyebrow">CONFUSION MATRIX</p>
        <img v-if="resultAssets.confusion_matrix_image" :src="resultAssets.confusion_matrix_image" alt="Confusion matrix" />
      </article>

      <article class="research-card glass-panel asset-card">
        <p class="eyebrow">TRAINING CURVE</p>
        <img v-if="resultAssets.training_curve_image" :src="resultAssets.training_curve_image" alt="Training curve" />
      </article>

      <article class="research-card glass-panel asset-card wide">
        <p class="eyebrow">FEATURE PROJECTION</p>
        <img v-if="resultAssets.feature_projection_image" :src="resultAssets.feature_projection_image" alt="Feature projection" />
      </article>
    </div>

    <div v-else class="empty-panel glass-panel">当前组合还没有注册公开完成结果。</div>
  </section>
</template>
