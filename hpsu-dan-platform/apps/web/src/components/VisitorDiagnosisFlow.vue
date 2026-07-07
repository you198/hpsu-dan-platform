<script setup lang="ts">
const props = defineProps<{
  active: boolean
  severity: string
}>()

const steps = [
  ['Data acquisition', 'Signal received'],
  ['Quality check', 'Signal window validated'],
  ['Time / frequency analysis', 'Waveform and FFT evidence'],
  ['AI state recognition', 'HPSU-DAN inference'],
  ['Fault localization', 'Digital twin target'],
  ['Confidence assessment', 'Risk and trust score'],
  ['Maintenance advice', 'Action suggestion'],
]

function state(index: number) {
  if (!props.active) return index === 0 ? 'running' : 'waiting'
  if (props.severity === 'severe' && index >= 4) return 'risk'
  return 'done'
}
</script>

<template>
  <div class="visitor-flow glass-panel">
    <div class="flow-step" v-for="(step, index) in steps" :key="step[0]" :class="state(index)">
      <span>{{ index + 1 }}</span>
      <div>
        <strong>{{ step[0] }}</strong>
        <small>{{ step[1] }}</small>
      </div>
    </div>
  </div>
</template>
