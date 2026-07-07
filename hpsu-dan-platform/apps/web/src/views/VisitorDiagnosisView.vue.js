/// <reference types="../../node_modules/.vue-global-types/vue_3.5_0_0_0.d.ts" />
import { computed, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { api } from '../api';
import { useAuthStore } from '../stores/auth';
import DiagnosisEvidence from '../components/DiagnosisEvidence.vue';
import FaultProbabilityChart from '../components/FaultProbabilityChart.vue';
import HealthScoreGauge from '../components/HealthScoreGauge.vue';
import MaintenanceSuggestionCard from '../components/MaintenanceSuggestionCard.vue';
import VisitorDiagnosisFlow from '../components/VisitorDiagnosisFlow.vue';
import { useDiagnosisStore } from '../stores/diagnosis';
const auth = useAuthStore();
const router = useRouter();
const diagnosis = useDiagnosisStore();
const loading = ref(false);
const uploading = ref(false);
const error = ref('');
const result = ref(null);
const quality = ref(null);
const tasks = ref([]);
const selectedFile = ref(null);
const showAdvanced = ref(false);
const selectedTask = ref(null);
const navigating = ref(false);
const isAdmin = computed(() => auth.user?.role === 'admin');
const probabilities = computed(() => result.value?.topk || [
    { label: diagnosis.current.code, label_en: diagnosis.current.labelEn, probability: diagnosis.current.confidence },
]);
const flowActive = computed(() => Boolean(result.value));
function goTwinSoon() {
    navigating.value = true;
    window.setTimeout(() => router.push('/digital-twin'), 900);
}
function sampleSignal() {
    return Array.from({ length: 2048 }, (_, i) => 0.24 * Math.sin(i * 0.17) + (i % 137 === 0 ? 1.4 : 0));
}
async function loadTasks() {
    if (!isAdmin.value)
        return;
    tasks.value = await api('/tasks?limit=8');
}
async function runSampleDiagnosis() {
    loading.value = true;
    error.value = '';
    try {
        result.value = await api('/diagnosis/predict', {
            method: 'POST',
            body: JSON.stringify({ samples: sampleSignal(), sampling_rate: 25600, model_id: 'hpsu-dan-v1' }),
        });
        quality.value = null;
        diagnosis.applyResult(result.value);
        await loadTasks();
        goTwinSoon();
    }
    catch (exc) {
        error.value = exc?.message || 'DIAGNOSIS_FAILED';
    }
    finally {
        loading.value = false;
    }
}
function chooseFile(event) {
    const input = event.target;
    selectedFile.value = input.files?.[0] || null;
}
async function uploadAndDiagnose() {
    if (!selectedFile.value)
        return;
    uploading.value = true;
    error.value = '';
    try {
        const body = new FormData();
        body.set('file', selectedFile.value);
        body.set('sampling_rate', '25600');
        body.set('model_id', 'hpsu-dan-v1');
        const payload = await api('/diagnosis/upload', { method: 'POST', body });
        result.value = payload.result;
        quality.value = payload.quality;
        if (payload.result)
            diagnosis.applyResult(payload.result);
        await loadTasks();
        if (payload.result)
            goTwinSoon();
    }
    catch (exc) {
        error.value = exc?.message || 'UPLOAD_DIAGNOSIS_FAILED';
    }
    finally {
        uploading.value = false;
    }
}
async function openTask(task) {
    selectedTask.value = await api(`/tasks/${task.task_id}`);
    if (selectedTask.value?.result) {
        result.value = selectedTask.value.result;
        diagnosis.applyResult(selectedTask.value.result);
    }
}
async function rerunTask(task) {
    loading.value = true;
    error.value = '';
    try {
        const payload = await api(`/tasks/${task.task_id}/rerun`, { method: 'POST' });
        selectedTask.value = payload.task;
        result.value = payload.result;
        if (payload.result)
            diagnosis.applyResult(payload.result);
        await loadTasks();
    }
    catch (exc) {
        error.value = exc?.message || 'RERUN_FAILED';
    }
    finally {
        loading.value = false;
    }
}
onMounted(() => loadTasks().catch(() => undefined));
debugger; /* PartiallyEnd: #3632/scriptSetup.vue */
const __VLS_ctx = {};
let __VLS_components;
let __VLS_directives;
__VLS_asFunctionalElement(__VLS_intrinsicElements.section, __VLS_intrinsicElements.section)({
    ...{ class: "visitor-diagnosis" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "page-title" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
    ...{ class: "eyebrow" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.h1, __VLS_intrinsicElements.h1)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
    ...{ onClick: (__VLS_ctx.runSampleDiagnosis) },
    ...{ class: "primary action" },
    disabled: (__VLS_ctx.loading),
});
(__VLS_ctx.navigating ? 'Opening twin...' : __VLS_ctx.loading ? 'Diagnosing...' : 'Start live diagnosis');
if (__VLS_ctx.error) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
        ...{ class: "error-box" },
    });
    (__VLS_ctx.error);
}
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "visitor-layout" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.article, __VLS_intrinsicElements.article)({
    ...{ class: "signal-entry glass-panel" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
    ...{ class: "eyebrow" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.h2, __VLS_intrinsicElements.h2)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.input)({
    ...{ onChange: (__VLS_ctx.chooseFile) },
    type: "file",
    accept: ".csv,.txt",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "signal-file" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
(__VLS_ctx.selectedFile?.name || 'No uploaded file');
__VLS_asFunctionalElement(__VLS_intrinsicElements.b, __VLS_intrinsicElements.b)({});
(__VLS_ctx.quality?.score ? `Quality ${__VLS_ctx.quality.score}` : 'Ready');
__VLS_asFunctionalElement(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
    ...{ onClick: (__VLS_ctx.uploadAndDiagnose) },
    ...{ class: "primary action" },
    disabled: (__VLS_ctx.uploading || !__VLS_ctx.selectedFile),
});
(__VLS_ctx.uploading ? 'Analyzing...' : 'Upload and analyze');
/** @type {[typeof VisitorDiagnosisFlow, ]} */ ;
// @ts-ignore
const __VLS_0 = __VLS_asFunctionalComponent(VisitorDiagnosisFlow, new VisitorDiagnosisFlow({
    active: (__VLS_ctx.flowActive),
    severity: (__VLS_ctx.diagnosis.current.riskLevel),
}));
const __VLS_1 = __VLS_0({
    active: (__VLS_ctx.flowActive),
    severity: (__VLS_ctx.diagnosis.current.riskLevel),
}, ...__VLS_functionalComponentArgsRest(__VLS_0));
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "visitor-result-grid" },
});
/** @type {[typeof HealthScoreGauge, ]} */ ;
// @ts-ignore
const __VLS_3 = __VLS_asFunctionalComponent(HealthScoreGauge, new HealthScoreGauge({
    score: (__VLS_ctx.diagnosis.current.healthScore),
    confidence: (__VLS_ctx.diagnosis.current.confidence),
    risk: (__VLS_ctx.diagnosis.current.riskLevel),
}));
const __VLS_4 = __VLS_3({
    score: (__VLS_ctx.diagnosis.current.healthScore),
    confidence: (__VLS_ctx.diagnosis.current.confidence),
    risk: (__VLS_ctx.diagnosis.current.riskLevel),
}, ...__VLS_functionalComponentArgsRest(__VLS_3));
/** @type {[typeof FaultProbabilityChart, ]} */ ;
// @ts-ignore
const __VLS_6 = __VLS_asFunctionalComponent(FaultProbabilityChart, new FaultProbabilityChart({
    items: (__VLS_ctx.probabilities),
}));
const __VLS_7 = __VLS_6({
    items: (__VLS_ctx.probabilities),
}, ...__VLS_functionalComponentArgsRest(__VLS_6));
/** @type {[typeof MaintenanceSuggestionCard, ]} */ ;
// @ts-ignore
const __VLS_9 = __VLS_asFunctionalComponent(MaintenanceSuggestionCard, new MaintenanceSuggestionCard({
    target: (__VLS_ctx.diagnosis.current.twinTarget),
    suggestion: (__VLS_ctx.diagnosis.current.suggestionEn),
    quality: (__VLS_ctx.quality),
}));
const __VLS_10 = __VLS_9({
    target: (__VLS_ctx.diagnosis.current.twinTarget),
    suggestion: (__VLS_ctx.diagnosis.current.suggestionEn),
    quality: (__VLS_ctx.quality),
}, ...__VLS_functionalComponentArgsRest(__VLS_9));
/** @type {[typeof DiagnosisEvidence, ]} */ ;
// @ts-ignore
const __VLS_12 = __VLS_asFunctionalComponent(DiagnosisEvidence, new DiagnosisEvidence({
    waveformMode: (__VLS_ctx.diagnosis.current.waveformMode),
    markers: (__VLS_ctx.diagnosis.current.spectrumMarkers),
    waveform: (__VLS_ctx.diagnosis.current.waveformPoints),
    spectrum: (__VLS_ctx.diagnosis.current.spectrumPoints),
}));
const __VLS_13 = __VLS_12({
    waveformMode: (__VLS_ctx.diagnosis.current.waveformMode),
    markers: (__VLS_ctx.diagnosis.current.spectrumMarkers),
    waveform: (__VLS_ctx.diagnosis.current.waveformPoints),
    spectrum: (__VLS_ctx.diagnosis.current.spectrumPoints),
}, ...__VLS_functionalComponentArgsRest(__VLS_12));
if (__VLS_ctx.isAdmin) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.details, __VLS_intrinsicElements.details)({
        ...{ onToggle: (...[$event]) => {
                if (!(__VLS_ctx.isAdmin))
                    return;
                __VLS_ctx.showAdvanced = $event.target.open;
            } },
        ...{ class: "advanced-admin glass-panel" },
        open: (__VLS_ctx.showAdvanced),
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.summary, __VLS_intrinsicElements.summary)({});
    __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        ...{ class: "history-row history-head" },
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
    __VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
    __VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
    __VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
    for (const [task] of __VLS_getVForSourceType((__VLS_ctx.tasks))) {
        __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
            ...{ onClick: (...[$event]) => {
                    if (!(__VLS_ctx.isAdmin))
                        return;
                    __VLS_ctx.openTask(task);
                } },
            key: (task.task_id),
            ...{ class: "history-row" },
        });
        __VLS_asFunctionalElement(__VLS_intrinsicElements.code, __VLS_intrinsicElements.code)({});
        (task.task_id.slice(-10));
        __VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
        (task.task_type);
        __VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
        (task.status);
        __VLS_asFunctionalElement(__VLS_intrinsicElements.b, __VLS_intrinsicElements.b)({});
        (task.model_id || '--');
    }
    if (__VLS_ctx.selectedTask) {
        __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
            ...{ class: "warning-text" },
        });
        __VLS_asFunctionalElement(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
        (__VLS_ctx.selectedTask.task_id);
        (__VLS_ctx.selectedTask.status);
        __VLS_asFunctionalElement(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
            ...{ onClick: (...[$event]) => {
                    if (!(__VLS_ctx.isAdmin))
                        return;
                    if (!(__VLS_ctx.selectedTask))
                        return;
                    __VLS_ctx.rerunTask(__VLS_ctx.selectedTask);
                } },
            ...{ class: "ghost" },
            disabled: (!__VLS_ctx.selectedTask.input_file_id || __VLS_ctx.loading),
        });
    }
}
/** @type {__VLS_StyleScopedClasses['visitor-diagnosis']} */ ;
/** @type {__VLS_StyleScopedClasses['page-title']} */ ;
/** @type {__VLS_StyleScopedClasses['eyebrow']} */ ;
/** @type {__VLS_StyleScopedClasses['primary']} */ ;
/** @type {__VLS_StyleScopedClasses['action']} */ ;
/** @type {__VLS_StyleScopedClasses['error-box']} */ ;
/** @type {__VLS_StyleScopedClasses['visitor-layout']} */ ;
/** @type {__VLS_StyleScopedClasses['signal-entry']} */ ;
/** @type {__VLS_StyleScopedClasses['glass-panel']} */ ;
/** @type {__VLS_StyleScopedClasses['eyebrow']} */ ;
/** @type {__VLS_StyleScopedClasses['signal-file']} */ ;
/** @type {__VLS_StyleScopedClasses['primary']} */ ;
/** @type {__VLS_StyleScopedClasses['action']} */ ;
/** @type {__VLS_StyleScopedClasses['visitor-result-grid']} */ ;
/** @type {__VLS_StyleScopedClasses['advanced-admin']} */ ;
/** @type {__VLS_StyleScopedClasses['glass-panel']} */ ;
/** @type {__VLS_StyleScopedClasses['history-row']} */ ;
/** @type {__VLS_StyleScopedClasses['history-head']} */ ;
/** @type {__VLS_StyleScopedClasses['history-row']} */ ;
/** @type {__VLS_StyleScopedClasses['warning-text']} */ ;
/** @type {__VLS_StyleScopedClasses['ghost']} */ ;
var __VLS_dollars;
const __VLS_self = (await import('vue')).defineComponent({
    setup() {
        return {
            DiagnosisEvidence: DiagnosisEvidence,
            FaultProbabilityChart: FaultProbabilityChart,
            HealthScoreGauge: HealthScoreGauge,
            MaintenanceSuggestionCard: MaintenanceSuggestionCard,
            VisitorDiagnosisFlow: VisitorDiagnosisFlow,
            diagnosis: diagnosis,
            loading: loading,
            uploading: uploading,
            error: error,
            quality: quality,
            tasks: tasks,
            selectedFile: selectedFile,
            showAdvanced: showAdvanced,
            selectedTask: selectedTask,
            navigating: navigating,
            isAdmin: isAdmin,
            probabilities: probabilities,
            flowActive: flowActive,
            runSampleDiagnosis: runSampleDiagnosis,
            chooseFile: chooseFile,
            uploadAndDiagnose: uploadAndDiagnose,
            openTask: openTask,
            rerunTask: rerunTask,
        };
    },
});
export default (await import('vue')).defineComponent({
    setup() {
        return {};
    },
});
; /* PartiallyEnd: #4569/main.vue */
