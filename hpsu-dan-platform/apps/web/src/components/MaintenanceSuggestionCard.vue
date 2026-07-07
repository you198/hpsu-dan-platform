<script setup lang="ts">
defineProps<{ target: string; suggestion: string; quality?: any }>()
</script>

<template>
  <article class="maintenance-card glass-panel">
    <p class="eyebrow">MAINTENANCE DECISION</p>
    <h2>{{ target }}</h2>
    <p>{{ suggestion }}</p>
    <div class="decision-grid">
      <span><small>Signal quality</small><strong>{{ quality?.score ?? '--' }}</strong></span>
      <span><small>Window</small><strong>{{ quality?.has_required_window === false ? 'Invalid' : 'Valid' }}</strong></span>
      <span><small>Action</small><strong>{{ target.includes('bearing') ? 'Inspect bearing' : 'Monitor' }}</strong></span>
    </div>
  </article>
</template>
