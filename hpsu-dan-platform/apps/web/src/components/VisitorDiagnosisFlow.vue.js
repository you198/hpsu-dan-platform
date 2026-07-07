/// <reference types="../../node_modules/.vue-global-types/vue_3.5_0_0_0.d.ts" />
const props = defineProps();
const steps = [
    ['Data acquisition', 'Signal received'],
    ['Quality check', 'Signal window validated'],
    ['Time / frequency analysis', 'Waveform and FFT evidence'],
    ['AI state recognition', 'HPSU-DAN inference'],
    ['Fault localization', 'Digital twin target'],
    ['Confidence assessment', 'Risk and trust score'],
    ['Maintenance advice', 'Action suggestion'],
];
function state(index) {
    if (!props.active)
        return index === 0 ? 'running' : 'waiting';
    if (props.severity === 'severe' && index >= 4)
        return 'risk';
    return 'done';
}
debugger; /* PartiallyEnd: #3632/scriptSetup.vue */
const __VLS_ctx = {};
let __VLS_components;
let __VLS_directives;
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "visitor-flow glass-panel" },
});
for (const [step, index] of __VLS_getVForSourceType((__VLS_ctx.steps))) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        ...{ class: "flow-step" },
        key: (step[0]),
        ...{ class: (__VLS_ctx.state(index)) },
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
    (index + 1);
    __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({});
    __VLS_asFunctionalElement(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
    (step[0]);
    __VLS_asFunctionalElement(__VLS_intrinsicElements.small, __VLS_intrinsicElements.small)({});
    (step[1]);
}
/** @type {__VLS_StyleScopedClasses['visitor-flow']} */ ;
/** @type {__VLS_StyleScopedClasses['glass-panel']} */ ;
/** @type {__VLS_StyleScopedClasses['flow-step']} */ ;
var __VLS_dollars;
const __VLS_self = (await import('vue')).defineComponent({
    setup() {
        return {
            steps: steps,
            state: state,
        };
    },
    __typeProps: {},
});
export default (await import('vue')).defineComponent({
    setup() {
        return {};
    },
    __typeProps: {},
});
; /* PartiallyEnd: #4569/main.vue */
