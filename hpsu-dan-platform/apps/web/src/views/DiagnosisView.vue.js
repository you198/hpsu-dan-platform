/// <reference types="../../node_modules/.vue-global-types/vue_3.5_0_0_0.d.ts" />
import { onMounted, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { api } from '../api';
import DiagnosisEvidence from '../components/DiagnosisEvidence.vue';
import { useDiagnosisStore } from '../stores/diagnosis';
const { t } = useI18n();
const diagnosis = useDiagnosisStore();
const loading = ref(false);
const result = ref(null);
const error = ref(false);
const history = ref([]);
function signal() { return Array.from({ length: 2048 }, (_, i) => .24 * Math.sin(i * .17) + (i % 137 === 0 ? 1.4 : 0)); }
async function loadHistory() { history.value = await api('/diagnosis/history?limit=8'); }
async function run() { loading.value = true; error.value = false; try {
    result.value = await api('/diagnosis/predict', { method: 'POST', body: JSON.stringify({ samples: signal(), sampling_rate: 25600, model_id: 'hpsu-dan-v1' }) });
    diagnosis.applyResult(result.value);
    await loadHistory();
}
catch {
    error.value = true;
}
finally {
    loading.value = false;
} }
onMounted(() => loadHistory().catch(() => undefined));
debugger; /* PartiallyEnd: #3632/scriptSetup.vue */
const __VLS_ctx = {};
let __VLS_components;
let __VLS_directives;
__VLS_asFunctionalElement(__VLS_intrinsicElements.section, __VLS_intrinsicElements.section)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "page-title" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
    ...{ class: "eyebrow" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.h1, __VLS_intrinsicElements.h1)({});
(__VLS_ctx.t('diagnosis.title'));
__VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({});
(__VLS_ctx.t('diagnosis.description'));
__VLS_asFunctionalElement(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
    ...{ onClick: (__VLS_ctx.run) },
    ...{ class: "primary action" },
    disabled: (__VLS_ctx.loading),
});
(__VLS_ctx.loading ? __VLS_ctx.t('diagnosis.running') : __VLS_ctx.t('diagnosis.run'));
if (__VLS_ctx.error) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
        ...{ class: "error-box" },
    });
    (__VLS_ctx.t('diagnosis.unavailable'));
}
if (__VLS_ctx.result) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        ...{ class: "result-grid" },
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.article, __VLS_intrinsicElements.article)({
        ...{ class: "result-main glass-panel" },
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
        ...{ class: "eyebrow" },
    });
    (__VLS_ctx.t('diagnosis.result'));
    __VLS_asFunctionalElement(__VLS_intrinsicElements.h2, __VLS_intrinsicElements.h2)({});
    (__VLS_ctx.$i18n.locale === 'zh-CN' ? __VLS_ctx.diagnosis.current.labelZh : __VLS_ctx.diagnosis.current.labelEn);
    __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        ...{ class: "score-row" },
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({});
    __VLS_asFunctionalElement(__VLS_intrinsicElements.small, __VLS_intrinsicElements.small)({});
    (__VLS_ctx.t('diagnosis.confidence'));
    __VLS_asFunctionalElement(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
    ((__VLS_ctx.diagnosis.current.confidence * 100).toFixed(1));
    __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({});
    __VLS_asFunctionalElement(__VLS_intrinsicElements.small, __VLS_intrinsicElements.small)({});
    (__VLS_ctx.t('diagnosis.health'));
    __VLS_asFunctionalElement(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
    (__VLS_ctx.diagnosis.current.healthScore);
    __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
        ...{ class: "warning-text" },
    });
    (__VLS_ctx.$i18n.locale === 'zh-CN' ? __VLS_ctx.diagnosis.current.suggestionZh : __VLS_ctx.diagnosis.current.suggestionEn);
    __VLS_asFunctionalElement(__VLS_intrinsicElements.article, __VLS_intrinsicElements.article)({
        ...{ class: "glass-panel topk" },
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
        ...{ class: "eyebrow" },
    });
    for (const [item] of __VLS_getVForSourceType((__VLS_ctx.result.topk))) {
        __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
            key: (item.label),
        });
        __VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
        (__VLS_ctx.$i18n.locale === 'zh-CN' ? item.label_zh : item.label_en);
        __VLS_asFunctionalElement(__VLS_intrinsicElements.b, __VLS_intrinsicElements.b)({});
        ((item.probability * 100).toFixed(1));
    }
    __VLS_asFunctionalElement(__VLS_intrinsicElements.code, __VLS_intrinsicElements.code)({});
    (__VLS_ctx.diagnosis.current.twinTarget);
    __VLS_asFunctionalElement(__VLS_intrinsicElements.code, __VLS_intrinsicElements.code)({});
    (__VLS_ctx.result.engine_mode);
}
/** @type {[typeof DiagnosisEvidence, ]} */ ;
// @ts-ignore
const __VLS_0 = __VLS_asFunctionalComponent(DiagnosisEvidence, new DiagnosisEvidence({
    waveformMode: (__VLS_ctx.diagnosis.current.waveformMode),
    markers: (__VLS_ctx.diagnosis.current.spectrumMarkers),
    waveform: (__VLS_ctx.diagnosis.current.waveformPoints),
    spectrum: (__VLS_ctx.diagnosis.current.spectrumPoints),
}));
const __VLS_1 = __VLS_0({
    waveformMode: (__VLS_ctx.diagnosis.current.waveformMode),
    markers: (__VLS_ctx.diagnosis.current.spectrumMarkers),
    waveform: (__VLS_ctx.diagnosis.current.waveformPoints),
    spectrum: (__VLS_ctx.diagnosis.current.spectrumPoints),
}, ...__VLS_functionalComponentArgsRest(__VLS_0));
__VLS_asFunctionalElement(__VLS_intrinsicElements.article, __VLS_intrinsicElements.article)({
    ...{ class: "glass-panel history-card" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
    ...{ class: "eyebrow" },
});
(__VLS_ctx.t('diagnosis.history'));
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "history-row history-head" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
(__VLS_ctx.t('diagnosis.operator'));
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
(__VLS_ctx.t('diagnosis.confidence'));
for (const [item] of __VLS_getVForSourceType((__VLS_ctx.history))) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        key: (item.task_id),
        ...{ class: "history-row" },
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.code, __VLS_intrinsicElements.code)({});
    (item.task_id.slice(-12));
    __VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
    (item.requested_by);
    __VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
    (item.label);
    __VLS_asFunctionalElement(__VLS_intrinsicElements.b, __VLS_intrinsicElements.b)({});
    ((item.confidence * 100).toFixed(1));
}
/** @type {__VLS_StyleScopedClasses['page-title']} */ ;
/** @type {__VLS_StyleScopedClasses['eyebrow']} */ ;
/** @type {__VLS_StyleScopedClasses['primary']} */ ;
/** @type {__VLS_StyleScopedClasses['action']} */ ;
/** @type {__VLS_StyleScopedClasses['error-box']} */ ;
/** @type {__VLS_StyleScopedClasses['result-grid']} */ ;
/** @type {__VLS_StyleScopedClasses['result-main']} */ ;
/** @type {__VLS_StyleScopedClasses['glass-panel']} */ ;
/** @type {__VLS_StyleScopedClasses['eyebrow']} */ ;
/** @type {__VLS_StyleScopedClasses['score-row']} */ ;
/** @type {__VLS_StyleScopedClasses['warning-text']} */ ;
/** @type {__VLS_StyleScopedClasses['glass-panel']} */ ;
/** @type {__VLS_StyleScopedClasses['topk']} */ ;
/** @type {__VLS_StyleScopedClasses['eyebrow']} */ ;
/** @type {__VLS_StyleScopedClasses['glass-panel']} */ ;
/** @type {__VLS_StyleScopedClasses['history-card']} */ ;
/** @type {__VLS_StyleScopedClasses['eyebrow']} */ ;
/** @type {__VLS_StyleScopedClasses['history-row']} */ ;
/** @type {__VLS_StyleScopedClasses['history-head']} */ ;
/** @type {__VLS_StyleScopedClasses['history-row']} */ ;
var __VLS_dollars;
const __VLS_self = (await import('vue')).defineComponent({
    setup() {
        return {
            DiagnosisEvidence: DiagnosisEvidence,
            t: t,
            diagnosis: diagnosis,
            loading: loading,
            result: result,
            error: error,
            history: history,
            run: run,
        };
    },
});
export default (await import('vue')).defineComponent({
    setup() {
        return {};
    },
});
; /* PartiallyEnd: #4569/main.vue */
