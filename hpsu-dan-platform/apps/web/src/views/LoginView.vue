<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '../stores/auth'

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref(false)
const auth = useAuthStore()
const router = useRouter()
const { t, locale } = useI18n()

async function submit() {
  loading.value = true; error.value = false
  try { await auth.login(username.value, password.value); await router.push('/dashboard') }
  catch { error.value = true }
  finally { loading.value = false }
}

function switchLanguage() { locale.value = locale.value === 'zh-CN' ? 'en-US' : 'zh-CN'; localStorage.setItem('locale', locale.value) }
</script>

<template>
  <main class="login-page">
    <button class="language-button" @click="switchLanguage">{{ t('common.language') }}</button>
    <div class="login-orbit orbit-a"></div><div class="login-orbit orbit-b"></div>
    <section class="login-card glass-panel">
      <div class="brand-mark"><span></span><span></span><span></span></div>
      <p class="eyebrow">STATE FEEDBACK · HIERARCHICAL ALIGNMENT</p>
      <h1>{{ t('auth.title') }}</h1><p class="subtitle">{{ t('auth.subtitle') }}</p>
      <form @submit.prevent="submit">
        <label>{{ t('auth.username') }}<input v-model="username" autocomplete="username" /></label>
        <label>{{ t('auth.password') }}<input v-model="password" type="password" autocomplete="current-password" /></label>
        <p v-if="error" class="error">{{ t('auth.failed') }}</p>
        <button class="primary" :disabled="loading">{{ loading ? '…' : t('auth.login') }}</button>
      </form>
      <p class="hint">{{ t('auth.hint') }}</p>
    </section>
  </main>
</template>

