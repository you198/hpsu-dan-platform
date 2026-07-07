<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { chatWithAssistant } from '../api'

const { t } = useI18n()
const prompt = ref('Explain how the HPSU-DAN platform should distinguish demo inference from real research inference.')
const answer = ref('')
const model = ref('')
const error = ref('')
const loading = ref(false)

async function send() {
  if (!prompt.value.trim() || loading.value) return
  loading.value = true
  error.value = ''
  try {
    const response = await chatWithAssistant(prompt.value.trim())
    answer.value = response.content
    model.value = response.model
  } catch (exc) {
    error.value = exc instanceof Error ? exc.message : 'ASSISTANT_REQUEST_FAILED'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section>
    <div class="page-title">
      <div>
        <p class="eyebrow">AI ANALYSIS CENTER</p>
        <h1>{{ t('analysis.title') }}</h1>
      </div>
    </div>

    <div class="assistant-grid">
      <article class="assistant-panel glass-panel">
        <div>
          <p class="eyebrow">TENCENT TOKENHUB</p>
          <h2>DeepSeek Assistant</h2>
          <p class="assistant-copy">
            Ask deployment, digital twin, diagnosis, model registry, or research workflow questions.
          </p>
        </div>
        <textarea v-model="prompt" maxlength="8000" />
        <div class="assistant-actions">
          <button class="primary" :disabled="loading || !prompt.trim()" @click="send">
            {{ loading ? 'Thinking...' : 'Send' }}
          </button>
          <span>{{ prompt.length }}/8000</span>
        </div>
        <p v-if="error" class="error-box">{{ error }}</p>
      </article>

      <article class="assistant-result glass-panel">
        <div class="assistant-result-head">
          <div>
            <p class="eyebrow">MODEL RESPONSE</p>
            <h2>{{ model || 'deepseek-v4-pro' }}</h2>
          </div>
        </div>
        <pre v-if="answer">{{ answer }}</pre>
        <div v-else class="wave-placeholder">
          <i v-for="n in 48" :key="n" :style="{ height: (20 + Math.sin(n * .7) * 16 + Math.random() * 22) + 'px' }"></i>
        </div>
      </article>
    </div>
  </section>
</template>
