<script setup>
const props = defineProps({
  icon: String,
  primary: {
    type: Boolean,
    default: false,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
});
</script>

<template>
  <button class="icon-button" :class="{ primary: props.primary }">
    <font-awesome-icon class="no-photos__icon" :icon="props.icon" />
  </button>
</template>

<style scoped>
.icon-button {
  width: 4rem;
  height: 4rem;
  font-size: 1.6rem;
  border-radius: 50%;
  border: none;
  outline: none;
  cursor: pointer;
  background-color: var(--secondary-color);
  color: var(--text-primary-color);
  user-select: none;
}

.icon-button.primary {
  background-color: var(--primary-color);
  color: var(--text-secondary-color);
}

.icon-button:disabled,
.icon-button.primary:disabled {
  background-color: #ccc;
  color: #aaa;
  cursor: not-allowed;
}
</style>
