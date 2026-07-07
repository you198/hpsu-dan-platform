<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()
const { t, locale } = useI18n()
const links = computed(() => [
  ['/dashboard', 'nav.dashboard', 'D'], ['/digital-twin', 'nav.twin', 'T'], ['/diagnosis', 'nav.diagnosis', 'AI'], ['/results', '已完成结果', 'R'], ['/analysis', 'nav.analysis', 'A'],
  ...(auth.user?.role === 'admin' ? [['/system', 'nav.system', 'S']] : []),
])
function linkText(key: string) { return key.startsWith('nav.') ? t(key) : key }
function logout() { auth.logout(); router.push('/login') }
function switchLanguage() { locale.value = locale.value === 'zh-CN' ? 'en-US' : 'zh-CN'; localStorage.setItem('locale', locale.value) }
</script>

<template>
  <div class="app-shell">
    <aside class="sidebar">
      <div class="logo"><div class="logo-icon">H</div><div><strong>HPSU-DAN</strong><small>DIGITAL TWIN</small></div></div>
      <nav><RouterLink v-for="link in links" :key="link[0]" :to="link[0]"><b>{{ link[2] }}</b><span>{{ linkText(link[1]) }}</span></RouterLink></nav>
      <div class="sidebar-user"><span class="status-dot"></span><div><strong>{{ auth.user?.username }}</strong><small>{{ auth.user?.role }}</small></div></div>
    </aside>
    <section class="workspace">
      <header><h2>{{ t('common.platform') }}</h2><div><button class="ghost" @click="switchLanguage">{{ t('common.language') }}</button><button class="ghost" @click="logout">{{ t('common.logout') }}</button></div></header>
      <main class="page"><RouterView /></main>
    </section>
  </div>
</template>
