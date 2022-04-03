<script setup>
import { ref, getCurrentInstance, onMounted } from "vue";
import FlagMessage from "./FlagMessage.vue";

const globals = getCurrentInstance().appContext.config.globalProperties;

const flags = ref([]);

function closeFlag(index) {
  flags.value.splice(index, 1);
}

onMounted(() => {
  globals.$emitter.on("flag-message", ({ content, modifier }) => {
    flags.value.unshift({ content, modifier });
  });
});
</script>

<template>
  <div v-if="flags.length" class="flags-container">
    <FlagMessage
      v-for="(flag, index) in flags"
      :content="flag.content"
      :modifier="flag.modifier"
      :key="index"
      @close="() => closeFlag(index)"
    />
  </div>
</template>

<style scoped>
.flags-container {
  position: absolute;
  top: 0.5rem;
  left: 50%;
  transform: translateX(-50%);
}
</style>
