<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { api } from '../api'
const { t } = useI18n(); const data = ref<any>(null)
onMounted(async () => { data.value = await api('/dashboard/summary') })
</script>
<template><section><div class="page-title"><div><p class="eyebrow">OVERVIEW / LIVE STATUS</p><h1>{{ t('dashboard.title') }}</h1></div><span class="online-pill"><i></i>{{ t('dashboard.online') }}</span></div>
  <div class="metric-grid" v-if="data">
    <article class="metric glass-panel"><small>{{ t('dashboard.health') }}</small><strong>{{ data.device.health_score }}<em>%</em></strong><div class="progress"><span :style="{width: data.device.health_score + '%'}"></span></div></article>
    <article class="metric glass-panel"><small>{{ t('dashboard.speed') }}</small><strong>{{ data.telemetry.speed_rpm }}<em> rpm</em></strong></article>
    <article class="metric glass-panel"><small>{{ t('dashboard.load') }}</small><strong>{{ data.telemetry.load_n }}<em> N</em></strong></article>
    <article class="metric glass-panel"><small>{{ t('dashboard.channels') }}</small><strong>{{ data.telemetry.channels }}</strong></article>
  </div>
  <div class="dashboard-grid"><article class="hero-panel glass-panel"><div class="machine-line"><span class="motor"></span><span class="shaft"></span><span class="bearing"></span><span class="shaft"></span><span class="disk"></span></div><div><span class="tag">SDUST TEST BENCH</span><h2>{{ data?.device.name }}</h2><p>{{ t('dashboard.notice') }}</p></div></article>
  <article class="glass-panel engine-card"><p class="eyebrow">AI ENGINE</p><h2>{{ data?.model.id }}</h2><span class="warning-pill">{{ t('dashboard.unregistered') }}</span><code>runtime: {{ data?.model.runtime }}</code></article></div>
</section></template>

