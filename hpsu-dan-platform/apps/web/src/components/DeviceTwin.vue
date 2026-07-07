<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, watch } from "vue";
import { SceneManager } from "../three/SceneManager";

const props = defineProps<{ fault: string; twinTarget?: string }>();
const emit = defineEmits<{ click: [name: string] }>();
const host = ref<HTMLDivElement | null>(null);
let sm: SceneManager | null = null;

onMounted(() => {
  if (!host.value) return;
  sm = new SceneManager({
    container: host.value,
    onPartClick: (name) => emit("click", name),
    onPartHover: (name) => {
      host.value!.style.cursor = name ? "pointer" : "grab";
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
</script>

<template>
  <div ref="host" class="twin-canvas"></div>
</template>
