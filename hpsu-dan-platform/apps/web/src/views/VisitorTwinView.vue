<script setup lang="ts">
import { computed } from 'vue'
import DeviceTwin from '../components/DeviceTwin.vue'
import DiagnosisEvidence from '../components/DiagnosisEvidence.vue'
import FaultProbabilityChart from '../components/FaultProbabilityChart.vue'
import HealthScoreGauge from '../components/HealthScoreGauge.vue'
import MaintenanceSuggestionCard from '../components/MaintenanceSuggestionCard.vue'
import { useDiagnosisStore } from '../stores/diagnosis'

const diagnosis = useDiagnosisStore()

const stages = [
  ['电机驱动', '1500 rpm 稳定输入'],
  ['联轴器传动', '转轴扭矩已传递'],
  ['轴承测试区', '故障部位已定位'],
  ['传感器采集', 'X/Y/Z 三向振动通道'],
  ['频谱证据', 'BPFI/BPFO/BSF marker'],
  ['维护决策', '检修建议已生成'],
]

const faultLabel = computed(() => {
  if (diagnosis.current.twinTarget.includes('inner')) return '轴承内圈故障'
  if (diagnosis.current.twinTarget.includes('outer')) return '轴承外圈故障'
  if (diagnosis.current.twinTarget.includes('rolling')) return '滚动体故障'
  if (diagnosis.current.faultKey === 'normal') return '设备运行稳定'
  return '状态需要复核'
})

const markerText = computed(() => diagnosis.current.spectrumMarkers.length ? diagnosis.current.spectrumMarkers.join(' / ') : '1X')
const isInnerRace = computed(() => diagnosis.current.twinTarget.includes('inner') || diagnosis.current.faultKey === 'inner_race_fault')
const recognitionText = computed(() => {
  if (isInnerRace.value) return '三维轴承内圈已红色闪烁，高亮点随转轴周期运动；FFT 区域同步显示 BPFI 与 2xBPFI 证据。'
  if (diagnosis.current.faultKey === 'normal') return '设备处于稳定状态，轴承区域保持绿色，波形和频谱无明显冲击特征。'
  return '三维模型已根据诊断结果定位对应部件，并同步更新波形、频谱和维护建议。'
})
</script>

<template>
  <section class="visitor-twin-page">
    <div class="page-title">
      <div>
        <p class="eyebrow">DEVICE STATE RECOGNITION</p>
        <h1>设备状态智能识别</h1>
        <p>诊断结果已映射到旋转机械实验台。红色闪烁部位表示系统识别到的故障位置，频谱 marker 和维护建议会同步更新。</p>
      </div>
      <span class="online-pill"><i></i>{{ diagnosis.current.code }} / {{ faultLabel }}</span>
    </div>

    <div class="state-summary-grid">
      <article class="glass-panel state-summary-card severe">
        <small>识别结果</small>
        <strong>{{ faultLabel }}</strong>
        <span>{{ diagnosis.current.labelEn }}</span>
      </article>
      <article class="glass-panel state-summary-card">
        <small>故障位置</small>
        <strong>{{ diagnosis.current.twinTarget }}</strong>
        <span>已同步到 3D twin 高亮区域</span>
      </article>
      <article class="glass-panel state-summary-card">
        <small>频谱证据</small>
        <strong>{{ markerText }}</strong>
        <span>FFT marker 已同步显示</span>
      </article>
      <article class="glass-panel state-summary-card">
        <small>推理模式</small>
        <strong>{{ diagnosis.current.engineMode }}</strong>
        <span>{{ diagnosis.current.modelVersion }}</span>
      </article>
    </div>

    <div class="visitor-twin-layout">
      <div class="twin-stage glass-panel visitor-twin-stage">
        <DeviceTwin :fault="diagnosis.current.faultKey" :twin-target="diagnosis.current.twinTarget" />
        <div class="twin-overlay visitor-overlay">
          <span>{{ diagnosis.current.code }}</span>
          <strong>{{ faultLabel }}</strong>
          <small>{{ diagnosis.current.twinTarget }}</small>
        </div>
        <div class="twin-device-hints">
          <span class="hint-pill motor">电机驱动</span>
          <span class="hint-pill bearing" :class="{ active: diagnosis.current.twinTarget.includes('bearing') }">6205 轴承测试区</span>
          <span class="hint-pill sensor">X/Y/Z 传感器采集</span>
          <span class="hint-pill marker" :class="{ active: markerText.includes('BPFI') }">BPFI marker</span>
        </div>
      </div>

      <aside class="twin-status-stack">
        <HealthScoreGauge :score="diagnosis.current.healthScore" :confidence="diagnosis.current.confidence" :risk="diagnosis.current.riskLevel" />
        <MaintenanceSuggestionCard :target="diagnosis.current.twinTarget" :suggestion="diagnosis.current.suggestionEn" />
        <article class="glass-panel state-explain-card">
          <p class="eyebrow">VISITOR EXPLANATION</p>
          <h2>系统正在说明什么？</h2>
          <p>{{ recognitionText }}</p>
        </article>
      </aside>
    </div>

    <div class="recognition-strip glass-panel">
      <div v-for="stage in stages" :key="stage[0]">
        <b>{{ stage[0] }}</b>
        <span>{{ stage[1] }}</span>
      </div>
    </div>

    <div class="visitor-result-grid twin-evidence-row">
      <FaultProbabilityChart :items="diagnosis.current.rawResult?.topk || [{ label: diagnosis.current.code, label_en: diagnosis.current.labelEn, probability: diagnosis.current.confidence }]" />
      <article class="maintenance-card glass-panel">
        <p class="eyebrow">BEARING 6205 PARAMETERS</p>
        <div class="decision-grid">
          <span><small>Inner diameter</small><strong>25 mm</strong></span>
          <span><small>Outer diameter</small><strong>52 mm</strong></span>
          <span><small>Rolling balls</small><strong>9</strong></span>
          <span><small>Ball diameter</small><strong>7.938 mm</strong></span>
          <span><small>Contact angle</small><strong>0 deg</strong></span>
          <span><small>Fault marker</small><strong>{{ diagnosis.current.spectrumMarkers.join(', ') }}</strong></span>
        </div>
      </article>
      <article class="maintenance-card glass-panel">
        <p class="eyebrow">STATE EXPLANATION</p>
        <h2>{{ faultLabel }}</h2>
        <p v-if="diagnosis.current.twinTarget.includes('inner')">诊断结果指向轴承内圈，系统已将内圈滚道设为红色周期闪烁，并在 FFT 中标注 BPFI。建议检查内圈滚道、装配间隙和润滑状态。</p>
        <p v-else-if="diagnosis.current.twinTarget.includes('outer')">诊断结果指向轴承外圈固定承载区。建议检查外圈接触区、轴承座紧固状态和润滑状态。</p>
        <p v-else-if="diagnosis.current.twinTarget.includes('rolling')">诊断结果指向滚动体路径。建议检查滚珠表面、保持架状态和污染情况。</p>
        <p v-else>当前设备映射为稳定或待复核状态。建议继续观察信号质量、振动趋势和后续诊断结果。</p>
      </article>
    </div>

    <DiagnosisEvidence
      :waveform-mode="diagnosis.current.waveformMode"
      :markers="diagnosis.current.spectrumMarkers"
      :waveform="diagnosis.current.waveformPoints"
      :spectrum="diagnosis.current.spectrumPoints"
    />
  </section>
</template>
