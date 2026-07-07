/// <reference types="../../node_modules/.vue-global-types/vue_3.5_0_0_0.d.ts" />
import { onBeforeUnmount, onMounted, ref, watch } from "vue";
import { SceneManager } from "../three/SceneManager";
const props = defineProps();
const emit = defineEmits();
const host = ref(null);
let sm = null;
onMounted(() => {
    if (!host.value)
        return;
    sm = new SceneManager({
        container: host.value,
        onPartClick: (name) => emit("click", name),
        onPartHover: (name) => {
            host.value.style.cursor = name ? "pointer" : "grab";
        },
    });
});
watch(() => [props.fault, props.twinTarget], () => {
    sm?.setFault(props.fault, props.twinTarget);
});
onBeforeUnmount(() => {
    sm?.dispose();
    sm = null;
});
debugger; /* PartiallyEnd: #3632/scriptSetup.vue */
const __VLS_ctx = {};
let __VLS_components;
let __VLS_directives;
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ref: "host",
    ...{ class: "twin-canvas" },
});
/** @type {typeof __VLS_ctx.host} */ ;
/** @type {__VLS_StyleScopedClasses['twin-canvas']} */ ;
var __VLS_dollars;
const __VLS_self = (await import('vue')).defineComponent({
    setup() {
        return {
            host: host,
        };
    },
    __typeEmits: {},
    __typeProps: {},
});
export default (await import('vue')).defineComponent({
    setup() {
        return {};
    },
    __typeEmits: {},
    __typeProps: {},
});
; /* PartiallyEnd: #4569/main.vue */
