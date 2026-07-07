<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{ score: number; confidence: number; risk: string }>()

const rotation = computed(() => -120 + Math.max(0, Math.min(100, props.score)) * 2.4)
const riskLabel = computed(() => props.risk === 'normal' ? 'Stable' : props.risk === 'warning' ? 'Warning' : 'Critical')
</script>

<template>
  <article class="health-gauge glass-panel">
    <p class="eyebrow">HEALTH ASSESSMENT</p>
    <div class="gauge-dial">
      <div class="gauge-arc"></div>
      <i :style="{ transform: `rotate(${rotation}deg)` }"></i>
      <strong>{{ score }}</strong>
      <small>{{ riskLabel }}</small>
    </div>
    <div class="confidence-strip">
      <span>Diagnostic confidence</span>
      <b>{{ (confidence * 100).toFixed(1) }}%</b>
    </div>
  </article>
</template>
