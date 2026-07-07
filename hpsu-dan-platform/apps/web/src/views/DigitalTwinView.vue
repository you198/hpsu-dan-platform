<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import DeviceTwin from '../components/DeviceTwin.vue'
import DiagnosisEvidence from '../components/DiagnosisEvidence.vue'
import { useDiagnosisStore, type FaultFamily } from '../stores/diagnosis'
const { t } = useI18n(); const diagnosis = useDiagnosisStore()
const selectedPart = ref('')
const partLabels: Record<string, string> = {
  motor: '驱动电机 | Drive Motor',
  coupling: '弹性联轴器 | Elastic Coupling',
  shaft: '传动转轴 | Drive Shaft',
  bearing: '测试轴承 6205 | Test Bearing 6205',
  bearing_outer_race: '轴承外圈 | Outer Race',
  bearing_inner_race: '轴承内圈 | Inner Race',
  rolling_element: '滚动体 | Rolling Element',
  gearbox: '行星齿轮箱 | Planetary Gearbox',
  load_disk: '负载盘/制动器 | Load Disk / Brake',
  sensor_x: 'X向振动传感器 | X-Axis Sensor',
  sensor_y: 'Y向振动传感器 | Y-Axis Sensor',
  sensor_z: 'Z向振动传感器 | Z-Axis Sensor',
  speed_controller: '转速控制器 | Speed Controller',
}
const states: [FaultFamily, string][] = [['normal','twin.normal'],['inner_race_fault','twin.inner'],['outer_race_fault','twin.outer'],['rolling_element_fault','twin.rolling'],['compound_fault','twin.compound']]
function onPartClick(name: string) { selectedPart.value = name }
</script>
<template>
<section class="twin-page">
  <div class="page-title">
    <div><p class="eyebrow">DIGITAL TWIN / DEVICE 01</p><h1>{{ t('twin.title') }}</h1><p>{{ t('twin.hint') }}</p></div>
    <span class="online-pill"><i></i>{{ diagnosis.current.engineMode }} / {{ diagnosis.current.modelVersion }}</span>
  </div>
  <div class="twin-stage glass-panel">
    <DeviceTwin :fault="diagnosis.current.faultKey" :twin-target="diagnosis.current.twinTarget" @click="onPartClick"/>
    <div class="twin-overlay">
      <span>{{ diagnosis.current.code }}</span>
      <strong>{{ diagnosis.current.labelEn }}</strong>
      <small>{{ diagnosis.current.twinTarget }}</small>
    </div>
    <div class="part-info-panel" v-if="selectedPart">
      <div class="part-info-content">
        <button class="part-info-close" @click="selectedPart=''">×</button>
        <h4>{{ partLabels[selectedPart] || selectedPart }}</h4>
        <div class="part-status">
          <span class="status-dot" :class="diagnosis.current.faultKey"></span>
          <span>{{ diagnosis.current.labelZh }} | {{ diagnosis.current.labelEn }}</span>
        </div>
        <div class="part-metrics">
          <span><small>{{t('diagnosis.confidence')}}</small><b>{{ (diagnosis.current.confidence * 100).toFixed(1) }}%</b></span>
          <span><small>{{t('diagnosis.health')}}</small><b>{{ diagnosis.current.healthScore }}</b></span>
        </div>
      </div>
    </div>
    <div class="fault-controls">
      <button v-for="s in states" :key="s[0]" :class="{active:diagnosis.current.faultKey===s[0]}" @click="diagnosis.setFault(s[0])">{{ t(s[1]) }}</button>
    </div>
  </div>
  <DiagnosisEvidence :waveform-mode="diagnosis.current.waveformMode" :markers="diagnosis.current.spectrumMarkers" :waveform="diagnosis.current.waveformPoints" :spectrum="diagnosis.current.spectrumPoints"/>
  <p class="demo-caption">{{ diagnosis.current.suggestionZh }}</p>
</section>
</template>

<style scoped>
.part-info-panel {
  position: absolute; top: 10px; left: 10px; z-index: 10;
  background: rgba(8, 22, 34, 0.92);
  border: 1px solid rgba(111, 205, 244, 0.25);
  border-radius: 12px; padding: 16px; min-width: 200px;
  backdrop-filter: blur(12px);
  animation: fadeIn 0.25s ease;
}
.part-info-content h4 {
  margin: 0 0 8px; font-size: 13px; color: #eaf6ff;
}
.part-info-close {
  float: right; background: none; border: none;
  color: #6f8d9f; cursor: pointer; font-size: 18px; padding: 0 4px;
}
.part-info-close:hover { color: #ff4868; }
.part-status {
  display: flex; align-items: center; gap: 8px;
  margin-top: 8px; font-size: 12px; color: #bcd1df;
}
.status-dot {
  display: inline-block; width: 10px; height: 10px; border-radius: 50%;
  background: #35d08b; box-shadow: 0 0 8px rgba(53, 208, 139, 0.5);
}
.status-dot.inner_race_fault { background: #ff4868; box-shadow: 0 0 8px rgba(255, 72, 104, 0.6); }
.status-dot.outer_race_fault { background: #ff9b42; box-shadow: 0 0 8px rgba(255, 155, 66, 0.6); }
.status-dot.rolling_element_fault { background: #a879ff; box-shadow: 0 0 8px rgba(168, 121, 255, 0.6); }
.status-dot.compound_fault { background: #d46bff; box-shadow: 0 0 8px rgba(212, 107, 255, 0.6); }
.part-metrics { display: flex; gap: 16px; margin-top: 10px; }
.part-metrics span { display: flex; flex-direction: column; gap: 2px; }
.part-metrics small { font-size: 10px; color: #6f8d9f; }
.part-metrics b { font-size: 16px; color: #55c8f4; font-family: 'Space Mono', monospace; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(-8px); } to { opacity: 1; transform: translateY(0); } }
</style>
