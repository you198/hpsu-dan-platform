/// <reference types="../../node_modules/.vue-global-types/vue_3.5_0_0_0.d.ts" />
import { computed } from 'vue';
import DeviceTwin from '../components/DeviceTwin.vue';
import DiagnosisEvidence from '../components/DiagnosisEvidence.vue';
import FaultProbabilityChart from '../components/FaultProbabilityChart.vue';
import HealthScoreGauge from '../components/HealthScoreGauge.vue';
import MaintenanceSuggestionCard from '../components/MaintenanceSuggestionCard.vue';
import { useDiagnosisStore } from '../stores/diagnosis';
const diagnosis = useDiagnosisStore();
const stages = [
    ['电机驱动', '1500 rpm 稳定输入'],
    ['联轴器传动', '转轴扭矩已传递'],
    ['轴承测试区', '故障部位已定位'],
    ['传感器采集', 'X/Y/Z 三向振动通道'],
    ['频谱证据', 'BPFI/BPFO/BSF marker'],
    ['维护决策', '检修建议已生成'],
];
const faultLabel = computed(() => {
    if (diagnosis.current.twinTarget.includes('inner'))
        return '轴承内圈故障';
    if (diagnosis.current.twinTarget.includes('outer'))
        return '轴承外圈故障';
    if (diagnosis.current.twinTarget.includes('rolling'))
        return '滚动体故障';
    if (diagnosis.current.faultKey === 'normal')
        return '设备运行稳定';
    return '状态需要复核';
});
const markerText = computed(() => diagnosis.current.spectrumMarkers.length ? diagnosis.current.spectrumMarkers.join(' / ') : '1X');
const isInnerRace = computed(() => diagnosis.current.twinTarget.includes('inner') || diagnosis.current.faultKey === 'inner_race_fault');
const recognitionText = computed(() => {
    if (isInnerRace.value)
        return '三维轴承内圈已红色闪烁，高亮点随转轴周期运动；FFT 区域同步显示 BPFI 与 2xBPFI 证据。';
    if (diagnosis.current.faultKey === 'normal')
        return '设备处于稳定状态，轴承区域保持绿色，波形和频谱无明显冲击特征。';
    return '三维模型已根据诊断结果定位对应部件，并同步更新波形、频谱和维护建议。';
});
debugger; /* PartiallyEnd: #3632/scriptSetup.vue */
const __VLS_ctx = {};
let __VLS_components;
let __VLS_directives;
__VLS_asFunctionalElement(__VLS_intrinsicElements.section, __VLS_intrinsicElements.section)({
    ...{ class: "visitor-twin-page" },
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
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({
    ...{ class: "online-pill" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.i, __VLS_intrinsicElements.i)({});
(__VLS_ctx.diagnosis.current.code);
(__VLS_ctx.faultLabel);
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "state-summary-grid" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.article, __VLS_intrinsicElements.article)({
    ...{ class: "glass-panel state-summary-card severe" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.small, __VLS_intrinsicElements.small)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
(__VLS_ctx.faultLabel);
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
(__VLS_ctx.diagnosis.current.labelEn);
__VLS_asFunctionalElement(__VLS_intrinsicElements.article, __VLS_intrinsicElements.article)({
    ...{ class: "glass-panel state-summary-card" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.small, __VLS_intrinsicElements.small)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
(__VLS_ctx.diagnosis.current.twinTarget);
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.article, __VLS_intrinsicElements.article)({
    ...{ class: "glass-panel state-summary-card" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.small, __VLS_intrinsicElements.small)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
(__VLS_ctx.markerText);
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.article, __VLS_intrinsicElements.article)({
    ...{ class: "glass-panel state-summary-card" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.small, __VLS_intrinsicElements.small)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
(__VLS_ctx.diagnosis.current.engineMode);
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
(__VLS_ctx.diagnosis.current.modelVersion);
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "visitor-twin-layout" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "twin-stage glass-panel visitor-twin-stage" },
});
/** @type {[typeof DeviceTwin, ]} */ ;
// @ts-ignore
const __VLS_0 = __VLS_asFunctionalComponent(DeviceTwin, new DeviceTwin({
    fault: (__VLS_ctx.diagnosis.current.faultKey),
    twinTarget: (__VLS_ctx.diagnosis.current.twinTarget),
}));
const __VLS_1 = __VLS_0({
    fault: (__VLS_ctx.diagnosis.current.faultKey),
    twinTarget: (__VLS_ctx.diagnosis.current.twinTarget),
}, ...__VLS_functionalComponentArgsRest(__VLS_0));
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "twin-overlay visitor-overlay" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
(__VLS_ctx.diagnosis.current.code);
__VLS_asFunctionalElement(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
(__VLS_ctx.faultLabel);
__VLS_asFunctionalElement(__VLS_intrinsicElements.small, __VLS_intrinsicElements.small)({});
(__VLS_ctx.diagnosis.current.twinTarget);
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "twin-device-hints" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({
    ...{ class: "hint-pill motor" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({
    ...{ class: "hint-pill bearing" },
    ...{ class: ({ active: __VLS_ctx.diagnosis.current.twinTarget.includes('bearing') }) },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({
    ...{ class: "hint-pill sensor" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({
    ...{ class: "hint-pill marker" },
    ...{ class: ({ active: __VLS_ctx.markerText.includes('BPFI') }) },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.aside, __VLS_intrinsicElements.aside)({
    ...{ class: "twin-status-stack" },
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
/** @type {[typeof MaintenanceSuggestionCard, ]} */ ;
// @ts-ignore
const __VLS_6 = __VLS_asFunctionalComponent(MaintenanceSuggestionCard, new MaintenanceSuggestionCard({
    target: (__VLS_ctx.diagnosis.current.twinTarget),
    suggestion: (__VLS_ctx.diagnosis.current.suggestionEn),
}));
const __VLS_7 = __VLS_6({
    target: (__VLS_ctx.diagnosis.current.twinTarget),
    suggestion: (__VLS_ctx.diagnosis.current.suggestionEn),
}, ...__VLS_functionalComponentArgsRest(__VLS_6));
__VLS_asFunctionalElement(__VLS_intrinsicElements.article, __VLS_intrinsicElements.article)({
    ...{ class: "glass-panel state-explain-card" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
    ...{ class: "eyebrow" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.h2, __VLS_intrinsicElements.h2)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({});
(__VLS_ctx.recognitionText);
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "recognition-strip glass-panel" },
});
for (const [stage] of __VLS_getVForSourceType((__VLS_ctx.stages))) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        key: (stage[0]),
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.b, __VLS_intrinsicElements.b)({});
    (stage[0]);
    __VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
    (stage[1]);
}
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "visitor-result-grid twin-evidence-row" },
});
/** @type {[typeof FaultProbabilityChart, ]} */ ;
// @ts-ignore
const __VLS_9 = __VLS_asFunctionalComponent(FaultProbabilityChart, new FaultProbabilityChart({
    items: (__VLS_ctx.diagnosis.current.rawResult?.topk || [{ label: __VLS_ctx.diagnosis.current.code, label_en: __VLS_ctx.diagnosis.current.labelEn, probability: __VLS_ctx.diagnosis.current.confidence }]),
}));
const __VLS_10 = __VLS_9({
    items: (__VLS_ctx.diagnosis.current.rawResult?.topk || [{ label: __VLS_ctx.diagnosis.current.code, label_en: __VLS_ctx.diagnosis.current.labelEn, probability: __VLS_ctx.diagnosis.current.confidence }]),
}, ...__VLS_functionalComponentArgsRest(__VLS_9));
__VLS_asFunctionalElement(__VLS_intrinsicElements.article, __VLS_intrinsicElements.article)({
    ...{ class: "maintenance-card glass-panel" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
    ...{ class: "eyebrow" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "decision-grid" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.small, __VLS_intrinsicElements.small)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.small, __VLS_intrinsicElements.small)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.small, __VLS_intrinsicElements.small)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.small, __VLS_intrinsicElements.small)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.small, __VLS_intrinsicElements.small)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.small, __VLS_intrinsicElements.small)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
(__VLS_ctx.diagnosis.current.spectrumMarkers.join(', '));
__VLS_asFunctionalElement(__VLS_intrinsicElements.article, __VLS_intrinsicElements.article)({
    ...{ class: "maintenance-card glass-panel" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
    ...{ class: "eyebrow" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.h2, __VLS_intrinsicElements.h2)({});
(__VLS_ctx.faultLabel);
if (__VLS_ctx.diagnosis.current.twinTarget.includes('inner')) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({});
}
else if (__VLS_ctx.diagnosis.current.twinTarget.includes('outer')) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({});
}
else if (__VLS_ctx.diagnosis.current.twinTarget.includes('rolling')) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({});
}
else {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({});
}
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
/** @type {__VLS_StyleScopedClasses['visitor-twin-page']} */ ;
/** @type {__VLS_StyleScopedClasses['page-title']} */ ;
/** @type {__VLS_StyleScopedClasses['eyebrow']} */ ;
/** @type {__VLS_StyleScopedClasses['online-pill']} */ ;
/** @type {__VLS_StyleScopedClasses['state-summary-grid']} */ ;
/** @type {__VLS_StyleScopedClasses['glass-panel']} */ ;
/** @type {__VLS_StyleScopedClasses['state-summary-card']} */ ;
/** @type {__VLS_StyleScopedClasses['severe']} */ ;
/** @type {__VLS_StyleScopedClasses['glass-panel']} */ ;
/** @type {__VLS_StyleScopedClasses['state-summary-card']} */ ;
/** @type {__VLS_StyleScopedClasses['glass-panel']} */ ;
/** @type {__VLS_StyleScopedClasses['state-summary-card']} */ ;
/** @type {__VLS_StyleScopedClasses['glass-panel']} */ ;
/** @type {__VLS_StyleScopedClasses['state-summary-card']} */ ;
/** @type {__VLS_StyleScopedClasses['visitor-twin-layout']} */ ;
/** @type {__VLS_StyleScopedClasses['twin-stage']} */ ;
/** @type {__VLS_StyleScopedClasses['glass-panel']} */ ;
/** @type {__VLS_StyleScopedClasses['visitor-twin-stage']} */ ;
/** @type {__VLS_StyleScopedClasses['twin-overlay']} */ ;
/** @type {__VLS_StyleScopedClasses['visitor-overlay']} */ ;
/** @type {__VLS_StyleScopedClasses['twin-device-hints']} */ ;
/** @type {__VLS_StyleScopedClasses['hint-pill']} */ ;
/** @type {__VLS_StyleScopedClasses['motor']} */ ;
/** @type {__VLS_StyleScopedClasses['hint-pill']} */ ;
/** @type {__VLS_StyleScopedClasses['bearing']} */ ;
/** @type {__VLS_StyleScopedClasses['active']} */ ;
/** @type {__VLS_StyleScopedClasses['hint-pill']} */ ;
/** @type {__VLS_StyleScopedClasses['sensor']} */ ;
/** @type {__VLS_StyleScopedClasses['hint-pill']} */ ;
/** @type {__VLS_StyleScopedClasses['marker']} */ ;
/** @type {__VLS_StyleScopedClasses['active']} */ ;
/** @type {__VLS_StyleScopedClasses['twin-status-stack']} */ ;
/** @type {__VLS_StyleScopedClasses['glass-panel']} */ ;
/** @type {__VLS_StyleScopedClasses['state-explain-card']} */ ;
/** @type {__VLS_StyleScopedClasses['eyebrow']} */ ;
/** @type {__VLS_StyleScopedClasses['recognition-strip']} */ ;
/** @type {__VLS_StyleScopedClasses['glass-panel']} */ ;
/** @type {__VLS_StyleScopedClasses['visitor-result-grid']} */ ;
/** @type {__VLS_StyleScopedClasses['twin-evidence-row']} */ ;
/** @type {__VLS_StyleScopedClasses['maintenance-card']} */ ;
/** @type {__VLS_StyleScopedClasses['glass-panel']} */ ;
/** @type {__VLS_StyleScopedClasses['eyebrow']} */ ;
/** @type {__VLS_StyleScopedClasses['decision-grid']} */ ;
/** @type {__VLS_StyleScopedClasses['maintenance-card']} */ ;
/** @type {__VLS_StyleScopedClasses['glass-panel']} */ ;
/** @type {__VLS_StyleScopedClasses['eyebrow']} */ ;
var __VLS_dollars;
const __VLS_self = (await import('vue')).defineComponent({
    setup() {
        return {
            DeviceTwin: DeviceTwin,
            DiagnosisEvidence: DiagnosisEvidence,
            FaultProbabilityChart: FaultProbabilityChart,
            HealthScoreGauge: HealthScoreGauge,
            MaintenanceSuggestionCard: MaintenanceSuggestionCard,
            diagnosis: diagnosis,
            stages: stages,
            faultLabel: faultLabel,
            markerText: markerText,
            recognitionText: recognitionText,
        };
    },
});
export default (await import('vue')).defineComponent({
    setup() {
        return {};
    },
});
; /* PartiallyEnd: #4569/main.vue */
