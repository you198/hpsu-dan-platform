<script setup lang="ts">
defineProps<{ items: any[] }>()
</script>

<template>
  <article class="probability-panel glass-panel">
    <p class="eyebrow">FAULT PROBABILITY</p>
    <div v-for="item in items" :key="item.label" class="prob-row">
      <span>{{ item.label_en || item.label }}</span>
      <div><i :style="{ width: `${Math.round((item.probability || 0) * 100)}%` }"></i></div>
      <b>{{ ((item.probability || 0) * 100).toFixed(1) }}%</b>
    </div>
  </article>
</template>
