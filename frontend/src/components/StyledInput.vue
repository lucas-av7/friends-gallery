<script setup>
const props = defineProps(["modelValue"], {
  type: String,
});
defineEmits(["update:modelValue"]);
</script>

<template>
  <input
    @input="$emit('update:modelValue', $event.target.value)"
    :value="modelValue"
    :type="props.type"
    class="styled-input"
  />
</template>

<style scoped>
.styled-input {
  min-width: 20rem;
  height: 4rem;
  font-size: 1.6rem;
  border-radius: 1rem;
  border: none;
  outline: none;
  padding: 1rem;
}

.styled-input:disabled {
  background-color: #ccc;
  color: #aaa;
  cursor: not-allowed;
}
</style>
