/// <reference types="../../node_modules/.vue-global-types/vue_3.5_0_0_0.d.ts" />
import { onMounted, ref } from 'vue';
import { api } from '../api';
import DiagnosisEvidence from '../components/DiagnosisEvidence.vue';
import { useDiagnosisStore } from '../stores/diagnosis';
const diagnosis = useDiagnosisStore();
const loading = ref(false);
const uploading = ref(false);
const error = ref('');
const result = ref(null);
const quality = ref(null);
const history = ref([]);
const tasks = ref([]);
const compute = ref(null);
const selectedTask = ref(null);
const selectedFile = ref(null);
function signal() {
    return Array.from({ length: 2048 }, (_, i) => 0.24 * Math.sin(i * 0.17) + (i % 137 === 0 ? 1.4 : 0));
}
async function loadHistory() {
    history.value = await api('/diagnosis/history?limit=8');
}
async function loadTasks() {
    tasks.value = await api('/tasks?limit=8');
}
async function loadCompute() {
    compute.value = await api('/compute/status');
}
async function refreshLists() {
    await Promise.all([loadHistory(), loadTasks(), loadCompute()]);
}
async function runDemoSignal() {
    loading.value = true;
    error.value = '';
    try {
        result.value = await api('/diagnosis/predict', {
            method: 'POST',
            body: JSON.stringify({ samples: signal(), sampling_rate: 25600, model_id: 'hpsu-dan-v1' }),
        });
        quality.value = null;
        diagnosis.applyResult(result.value);
        await refreshLists();
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
        await refreshLists();
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
        await refreshLists();
    }
    catch (exc) {
        error.value = exc?.message || 'RERUN_FAILED';
    }
    finally {
        loading.value = false;
    }
}
onMounted(() => refreshLists().catch(() => undefined));
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
__VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
    ...{ onClick: (__VLS_ctx.runDemoSignal) },
    ...{ class: "primary action" },
    disabled: (__VLS_ctx.loading),
});
(__VLS_ctx.loading ? 'Diagnosing...' : 'Run sample diagnosis');
if (__VLS_ctx.error) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
        ...{ class: "error-box" },
    });
    (__VLS_ctx.error);
}
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "result-grid" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.article, __VLS_intrinsicElements.article)({
    ...{ class: "glass-panel result-main" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
    ...{ class: "eyebrow" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.h2, __VLS_intrinsicElements.h2)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
    ...{ class: "warning-text" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.input)({
    ...{ onChange: (__VLS_ctx.chooseFile) },
    type: "file",
    accept: ".csv,.txt",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "score-row" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.small, __VLS_intrinsicElements.small)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
(__VLS_ctx.selectedFile?.name || 'None');
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.small, __VLS_intrinsicElements.small)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
(__VLS_ctx.quality?.score ?? '--');
__VLS_asFunctionalElement(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
    ...{ onClick: (__VLS_ctx.uploadAndDiagnose) },
    ...{ class: "primary action" },
    disabled: (__VLS_ctx.uploading || !__VLS_ctx.selectedFile),
});
(__VLS_ctx.uploading ? 'Uploading...' : 'Upload and diagnose');
__VLS_asFunctionalElement(__VLS_intrinsicElements.article, __VLS_intrinsicElements.article)({
    ...{ class: "glass-panel topk" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
    ...{ class: "eyebrow" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.h2, __VLS_intrinsicElements.h2)({});
(__VLS_ctx.diagnosis.current.labelEn);
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "score-row" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.small, __VLS_intrinsicElements.small)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
((__VLS_ctx.diagnosis.current.confidence * 100).toFixed(1));
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.small, __VLS_intrinsicElements.small)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
(__VLS_ctx.diagnosis.current.healthScore);
__VLS_asFunctionalElement(__VLS_intrinsicElements.code, __VLS_intrinsicElements.code)({});
(__VLS_ctx.diagnosis.current.twinTarget);
__VLS_asFunctionalElement(__VLS_intrinsicElements.code, __VLS_intrinsicElements.code)({});
(__VLS_ctx.diagnosis.current.engineMode);
__VLS_asFunctionalElement(__VLS_intrinsicElements.code, __VLS_intrinsicElements.code)({});
(__VLS_ctx.diagnosis.current.modelVersion);
__VLS_asFunctionalElement(__VLS_intrinsicElements.code, __VLS_intrinsicElements.code)({});
(__VLS_ctx.compute?.gpu_available ? 'available' : 'unavailable');
__VLS_asFunctionalElement(__VLS_intrinsicElements.code, __VLS_intrinsicElements.code)({});
(__VLS_ctx.compute?.queues?.gpu_inference_queue?.status || '--');
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
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "result-grid" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.article, __VLS_intrinsicElements.article)({
    ...{ class: "glass-panel history-card" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
    ...{ class: "eyebrow" },
});
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
                if (!(__VLS_ctx.selectedTask))
                    return;
                __VLS_ctx.rerunTask(__VLS_ctx.selectedTask);
            } },
        ...{ class: "ghost" },
        disabled: (!__VLS_ctx.selectedTask.input_file_id || __VLS_ctx.loading),
    });
}
__VLS_asFunctionalElement(__VLS_intrinsicElements.article, __VLS_intrinsicElements.article)({
    ...{ class: "glass-panel history-card" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
    ...{ class: "eyebrow" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "history-row history-head" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
for (const [item] of __VLS_getVForSourceType((__VLS_ctx.history))) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        key: (item.task_id),
        ...{ class: "history-row" },
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.code, __VLS_intrinsicElements.code)({});
    (item.task_id.slice(-10));
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
/** @type {__VLS_StyleScopedClasses['glass-panel']} */ ;
/** @type {__VLS_StyleScopedClasses['result-main']} */ ;
/** @type {__VLS_StyleScopedClasses['eyebrow']} */ ;
/** @type {__VLS_StyleScopedClasses['warning-text']} */ ;
/** @type {__VLS_StyleScopedClasses['score-row']} */ ;
/** @type {__VLS_StyleScopedClasses['primary']} */ ;
/** @type {__VLS_StyleScopedClasses['action']} */ ;
/** @type {__VLS_StyleScopedClasses['glass-panel']} */ ;
/** @type {__VLS_StyleScopedClasses['topk']} */ ;
/** @type {__VLS_StyleScopedClasses['eyebrow']} */ ;
/** @type {__VLS_StyleScopedClasses['score-row']} */ ;
/** @type {__VLS_StyleScopedClasses['result-grid']} */ ;
/** @type {__VLS_StyleScopedClasses['glass-panel']} */ ;
/** @type {__VLS_StyleScopedClasses['history-card']} */ ;
/** @type {__VLS_StyleScopedClasses['eyebrow']} */ ;
/** @type {__VLS_StyleScopedClasses['history-row']} */ ;
/** @type {__VLS_StyleScopedClasses['history-head']} */ ;
/** @type {__VLS_StyleScopedClasses['history-row']} */ ;
/** @type {__VLS_StyleScopedClasses['warning-text']} */ ;
/** @type {__VLS_StyleScopedClasses['ghost']} */ ;
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
            diagnosis: diagnosis,
            loading: loading,
            uploading: uploading,
            error: error,
            quality: quality,
            history: history,
            tasks: tasks,
            compute: compute,
            selectedTask: selectedTask,
            selectedFile: selectedFile,
            runDemoSignal: runDemoSignal,
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
