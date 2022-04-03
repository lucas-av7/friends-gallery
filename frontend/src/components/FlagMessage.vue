<script setup>
const props = defineProps({
  content: String,
  modifier: String,
});

const emit = defineEmits(["close"]);
</script>
<template>
  <div class="flag-message" :class="[props.modifier]">
    {{ props.content }}
    <font-awesome-icon
      @click="emit('close')"
      class="flag-message-close__icon"
      icon="xmark-circle"
    />
  </div>
</template>
<style scoped>
.flag-message {
  position: relative;
  display: flex;
  align-items: center;
  padding: 1rem 2rem 1rem 1rem;
  width: 30rem;
  min-height: 6rem;
  background: white;
  border-left: 2rem solid;
  border-color: var(--secondary-color);
  margin-bottom: 0.6rem;
  border-radius: 1rem;
}

.flag-message.error {
  border-color: var(--red-color);
}

.flag-message.caution {
  border-color: var(--orange-color);
}

.flag-message.success {
  border-color: var(--green-color);
}

.flag-message-close__icon {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  color: var(--primary-color);
  font-size: 2rem;
  cursor: pointer;
}
</style>
