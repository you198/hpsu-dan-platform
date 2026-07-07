/// <reference types="../../node_modules/.vue-global-types/vue_3.5_0_0_0.d.ts" />
import { computed } from 'vue';
const props = defineProps();
function sample(i) {
    const x = i / 119;
    const base = Math.sin(i * .42) * .18 + Math.sin(i * .09) * .1;
    if (props.waveformMode === 'stable')
        return base;
    if (props.waveformMode === 'impact_periodic')
        return base + (i % 18 === 0 ? .72 : 0);
    if (props.waveformMode === 'impact_fixed')
        return base + (i % 24 === 0 ? .58 : 0);
    if (props.waveformMode === 'impact_modulated')
        return base + (i % 21 === 0 ? .46 + Math.sin(x * 16) * .18 : 0);
    return base + (i % 17 === 0 ? .52 : 0) + (i % 31 === 0 ? -.38 : 0);
}
const waveform = computed(() => {
    if (props.waveform?.length) {
        return props.waveform.map((point) => {
            const x = Math.max(0, Math.min(1, Number(point.x))) * 100;
            const y = 50 - Math.max(-1, Math.min(1, Number(point.y))) * 42;
            return `${x.toFixed(2)},${Math.max(8, Math.min(92, y)).toFixed(2)}`;
        }).join(' ');
    }
    return Array.from({ length: 120 }, (_, i) => {
        const x = (i / 119) * 100;
        const y = 50 - sample(i) * 42;
        return `${x.toFixed(2)},${Math.max(8, Math.min(92, y)).toFixed(2)}`;
    }).join(' ');
});
const bars = computed(() => {
    if (props.spectrum?.length) {
        const markerSet = new Set(props.markers);
        const markerPositions = { BPFO: 8, BPFI: 17, BSF: 26, FTF: 33 };
        return props.spectrum.slice(0, 42).map((point, i) => {
            const marker = Object.entries(markerPositions).find(([, index]) => Math.abs(index - i) <= 1 && markerSet.has(_markerAlias(_markerName(index))))?.[0] || '';
            return { x: i * 2.25 + 2, height: Math.max(4, Math.min(72, Number(point.magnitude) * 72)), marker, active: Boolean(marker) };
        });
    }
    const markerSet = new Set(props.markers);
    return Array.from({ length: 42 }, (_, i) => {
        const marker = i === 8 ? 'BPFO' : i === 17 ? 'BPFI' : i === 26 ? 'BSF' : i === 33 ? 'FTF' : '';
        const active = marker && markerSet.has(marker);
        const height = active ? 68 : 10 + Math.abs(Math.sin(i * 1.7)) * 22;
        return { x: i * 2.25 + 2, height, marker, active };
    });
});
function _markerName(index) {
    return index === 8 ? 'BPFO' : index === 17 ? 'BPFI' : index === 26 ? 'BSF' : index === 33 ? 'FTF' : '';
}
function _markerAlias(marker) {
    return marker;
}
debugger; /* PartiallyEnd: #3632/scriptSetup.vue */
const __VLS_ctx = {};
let __VLS_components;
let __VLS_directives;
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "evidence-grid" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.article, __VLS_intrinsicElements.article)({
    ...{ class: "glass-panel evidence-card" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
    ...{ class: "eyebrow" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.svg, __VLS_intrinsicElements.svg)({
    viewBox: "0 0 100 100",
    preserveAspectRatio: "none",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.line)({
    x1: "0",
    y1: "50",
    x2: "100",
    y2: "50",
    ...{ class: "axis" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.polyline)({
    points: (__VLS_ctx.waveform),
    ...{ class: "wave-line" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.article, __VLS_intrinsicElements.article)({
    ...{ class: "glass-panel evidence-card" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
    ...{ class: "eyebrow" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.svg, __VLS_intrinsicElements.svg)({
    viewBox: "0 0 100 100",
    preserveAspectRatio: "none",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.line)({
    x1: "0",
    y1: "88",
    x2: "100",
    y2: "88",
    ...{ class: "axis" },
});
for (const [bar] of __VLS_getVForSourceType((__VLS_ctx.bars))) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.g, __VLS_intrinsicElements.g)({
        key: (bar.x),
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.rect)({
        x: (bar.x),
        y: (88 - bar.height),
        width: "1.35",
        height: (bar.height),
        ...{ class: (bar.active ? 'fft-active' : 'fft-bar') },
    });
    if (bar.active) {
        __VLS_asFunctionalElement(__VLS_intrinsicElements.text, __VLS_intrinsicElements.text)({
            x: (bar.x - 2),
            y: (84 - bar.height),
            ...{ class: "fft-label" },
        });
        (bar.marker);
    }
}
/** @type {__VLS_StyleScopedClasses['evidence-grid']} */ ;
/** @type {__VLS_StyleScopedClasses['glass-panel']} */ ;
/** @type {__VLS_StyleScopedClasses['evidence-card']} */ ;
/** @type {__VLS_StyleScopedClasses['eyebrow']} */ ;
/** @type {__VLS_StyleScopedClasses['axis']} */ ;
/** @type {__VLS_StyleScopedClasses['wave-line']} */ ;
/** @type {__VLS_StyleScopedClasses['glass-panel']} */ ;
/** @type {__VLS_StyleScopedClasses['evidence-card']} */ ;
/** @type {__VLS_StyleScopedClasses['eyebrow']} */ ;
/** @type {__VLS_StyleScopedClasses['axis']} */ ;
/** @type {__VLS_StyleScopedClasses['fft-label']} */ ;
var __VLS_dollars;
const __VLS_self = (await import('vue')).defineComponent({
    setup() {
        return {
            waveform: waveform,
            bars: bars,
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
