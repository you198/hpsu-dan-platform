<script setup lang="ts">
import { onMounted, ref } from 'vue'; import { useI18n } from 'vue-i18n'; import { api } from '../api'; import { useAuthStore } from '../stores/auth'
const { t }=useI18n(); const auth=useAuthStore(); const status=ref<any>(null); onMounted(async()=>{status.value=await api('/system/status')})
</script>
<template><section><div class="page-title"><div><p class="eyebrow">PLATFORM CONTROL</p><h1>{{ t('system.title') }}</h1></div></div><div class="settings-grid"><article class="glass-panel"><small>{{ t('system.role') }}</small><strong>{{ auth.user?.role }}</strong></article><article class="glass-panel"><small>{{ t('system.database') }}</small><strong>{{ status?.database }}</strong></article><article class="glass-panel"><small>{{ t('system.inference') }}</small><strong>{{ status?.inference_url_configured?t('system.enabled'):t('system.disabled') }}</strong></article><article class="glass-panel"><small>{{ t('system.assistant') }}</small><strong>{{ status?.assistant_enabled?t('system.enabled'):t('system.disabled') }}</strong></article></div></section></template>

