/// <reference types="../../node_modules/.vue-global-types/vue_3.5_0_0_0.d.ts" />
import { ref } from 'vue';
import { useI18n } from 'vue-i18n';
import DeviceTwin from '../components/DeviceTwin.vue';
import DiagnosisEvidence from '../components/DiagnosisEvidence.vue';
import { useDiagnosisStore } from '../stores/diagnosis';
const { t } = useI18n();
const diagnosis = useDiagnosisStore();
const selectedPart = ref('');
const partLabels = {
    motor: '驱动电机 | Drive Motor',
    coupling: '弹性联轴器 | Elastic Coupling',
    shaft: '传动转轴 | Drive Shaft',
    bearing: '测试轴承 6205 | Test Bearing 6205',
    bearing_outer_race: '轴承外圈 | Outer Race',
    bearing_inner_race: '轴承内圈 | Inner Race',
    rolling_element: '滚动体 | Rolling Element',
    gearbox: '行星齿轮箱 | Planetary Gearbox',
    load_disk: '负载盘/制动器 | Load Disk / Brake',
    sensor_x: 'X向振动传感器 | X-Axis Sensor',
    sensor_y: 'Y向振动传感器 | Y-Axis Sensor',
    sensor_z: 'Z向振动传感器 | Z-Axis Sensor',
    speed_controller: '转速控制器 | Speed Controller',
};
const states = [['normal', 'twin.normal'], ['inner_race_fault', 'twin.inner'], ['outer_race_fault', 'twin.outer'], ['rolling_element_fault', 'twin.rolling'], ['compound_fault', 'twin.compound']];
function onPartClick(name) { selectedPart.value = name; }
debugger; /* PartiallyEnd: #3632/scriptSetup.vue */
const __VLS_ctx = {};
let __VLS_components;
let __VLS_directives;
/** @type {__VLS_StyleScopedClasses['part-info-close']} */ ;
/** @type {__VLS_StyleScopedClasses['status-dot']} */ ;
/** @type {__VLS_StyleScopedClasses['status-dot']} */ ;
/** @type {__VLS_StyleScopedClasses['status-dot']} */ ;
/** @type {__VLS_StyleScopedClasses['status-dot']} */ ;
/** @type {__VLS_StyleScopedClasses['part-metrics']} */ ;
/** @type {__VLS_StyleScopedClasses['part-metrics']} */ ;
/** @type {__VLS_StyleScopedClasses['part-metrics']} */ ;
// CSS variable injection 
// CSS variable injection end 
__VLS_asFunctionalElement(__VLS_intrinsicElements.section, __VLS_intrinsicElements.section)({
    ...{ class: "twin-page" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "page-title" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
    ...{ class: "eyebrow" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.h1, __VLS_intrinsicElements.h1)({});
(__VLS_ctx.t('twin.title'));
__VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({});
(__VLS_ctx.t('twin.hint'));
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({
    ...{ class: "online-pill" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.i, __VLS_intrinsicElements.i)({});
(__VLS_ctx.diagnosis.current.engineMode);
(__VLS_ctx.diagnosis.current.modelVersion);
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "twin-stage glass-panel" },
});
/** @type {[typeof DeviceTwin, ]} */ ;
// @ts-ignore
const __VLS_0 = __VLS_asFunctionalComponent(DeviceTwin, new DeviceTwin({
    ...{ 'onClick': {} },
    fault: (__VLS_ctx.diagnosis.current.faultKey),
    twinTarget: (__VLS_ctx.diagnosis.current.twinTarget),
}));
const __VLS_1 = __VLS_0({
    ...{ 'onClick': {} },
    fault: (__VLS_ctx.diagnosis.current.faultKey),
    twinTarget: (__VLS_ctx.diagnosis.current.twinTarget),
}, ...__VLS_functionalComponentArgsRest(__VLS_0));
let __VLS_3;
let __VLS_4;
let __VLS_5;
const __VLS_6 = {
    onClick: (__VLS_ctx.onPartClick)
};
var __VLS_2;
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "twin-overlay" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
(__VLS_ctx.diagnosis.current.code);
__VLS_asFunctionalElement(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
(__VLS_ctx.diagnosis.current.labelEn);
__VLS_asFunctionalElement(__VLS_intrinsicElements.small, __VLS_intrinsicElements.small)({});
(__VLS_ctx.diagnosis.current.twinTarget);
if (__VLS_ctx.selectedPart) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        ...{ class: "part-info-panel" },
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        ...{ class: "part-info-content" },
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
        ...{ onClick: (...[$event]) => {
                if (!(__VLS_ctx.selectedPart))
                    return;
                __VLS_ctx.selectedPart = '';
            } },
        ...{ class: "part-info-close" },
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.h4, __VLS_intrinsicElements.h4)({});
    (__VLS_ctx.partLabels[__VLS_ctx.selectedPart] || __VLS_ctx.selectedPart);
    __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        ...{ class: "part-status" },
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({
        ...{ class: "status-dot" },
        ...{ class: (__VLS_ctx.diagnosis.current.faultKey) },
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
    (__VLS_ctx.diagnosis.current.labelZh);
    (__VLS_ctx.diagnosis.current.labelEn);
    __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        ...{ class: "part-metrics" },
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
    __VLS_asFunctionalElement(__VLS_intrinsicElements.small, __VLS_intrinsicElements.small)({});
    (__VLS_ctx.t('diagnosis.confidence'));
    __VLS_asFunctionalElement(__VLS_intrinsicElements.b, __VLS_intrinsicElements.b)({});
    ((__VLS_ctx.diagnosis.current.confidence * 100).toFixed(1));
    __VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
    __VLS_asFunctionalElement(__VLS_intrinsicElements.small, __VLS_intrinsicElements.small)({});
    (__VLS_ctx.t('diagnosis.health'));
    __VLS_asFunctionalElement(__VLS_intrinsicElements.b, __VLS_intrinsicElements.b)({});
    (__VLS_ctx.diagnosis.current.healthScore);
}
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "fault-controls" },
});
for (const [s] of __VLS_getVForSourceType((__VLS_ctx.states))) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
        ...{ onClick: (...[$event]) => {
                __VLS_ctx.diagnosis.setFault(s[0]);
            } },
        key: (s[0]),
        ...{ class: ({ active: __VLS_ctx.diagnosis.current.faultKey === s[0] }) },
    });
    (__VLS_ctx.t(s[1]));
}
/** @type {[typeof DiagnosisEvidence, ]} */ ;
// @ts-ignore
const __VLS_7 = __VLS_asFunctionalComponent(DiagnosisEvidence, new DiagnosisEvidence({
    waveformMode: (__VLS_ctx.diagnosis.current.waveformMode),
    markers: (__VLS_ctx.diagnosis.current.spectrumMarkers),
    waveform: (__VLS_ctx.diagnosis.current.waveformPoints),
    spectrum: (__VLS_ctx.diagnosis.current.spectrumPoints),
}));
const __VLS_8 = __VLS_7({
    waveformMode: (__VLS_ctx.diagnosis.current.waveformMode),
    markers: (__VLS_ctx.diagnosis.current.spectrumMarkers),
    waveform: (__VLS_ctx.diagnosis.current.waveformPoints),
    spectrum: (__VLS_ctx.diagnosis.current.spectrumPoints),
}, ...__VLS_functionalComponentArgsRest(__VLS_7));
__VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
    ...{ class: "demo-caption" },
});
(__VLS_ctx.diagnosis.current.suggestionZh);
/** @type {__VLS_StyleScopedClasses['twin-page']} */ ;
/** @type {__VLS_StyleScopedClasses['page-title']} */ ;
/** @type {__VLS_StyleScopedClasses['eyebrow']} */ ;
/** @type {__VLS_StyleScopedClasses['online-pill']} */ ;
/** @type {__VLS_StyleScopedClasses['twin-stage']} */ ;
/** @type {__VLS_StyleScopedClasses['glass-panel']} */ ;
/** @type {__VLS_StyleScopedClasses['twin-overlay']} */ ;
/** @type {__VLS_StyleScopedClasses['part-info-panel']} */ ;
/** @type {__VLS_StyleScopedClasses['part-info-content']} */ ;
/** @type {__VLS_StyleScopedClasses['part-info-close']} */ ;
/** @type {__VLS_StyleScopedClasses['part-status']} */ ;
/** @type {__VLS_StyleScopedClasses['status-dot']} */ ;
/** @type {__VLS_StyleScopedClasses['part-metrics']} */ ;
/** @type {__VLS_StyleScopedClasses['fault-controls']} */ ;
/** @type {__VLS_StyleScopedClasses['active']} */ ;
/** @type {__VLS_StyleScopedClasses['demo-caption']} */ ;
var __VLS_dollars;
const __VLS_self = (await import('vue')).defineComponent({
    setup() {
        return {
            DeviceTwin: DeviceTwin,
            DiagnosisEvidence: DiagnosisEvidence,
            t: t,
            diagnosis: diagnosis,
            selectedPart: selectedPart,
            partLabels: partLabels,
            states: states,
            onPartClick: onPartClick,
        };
    },
});
export default (await import('vue')).defineComponent({
    setup() {
        return {};
    },
});
; /* PartiallyEnd: #4569/main.vue */
