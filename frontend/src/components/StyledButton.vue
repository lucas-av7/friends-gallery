<script setup>
const props = defineProps({
  label: String,
  primary: {
    type: Boolean,
    default: false,
  },
  green: {
    type: Boolean,
    default: false,
  },
  red: {
    type: Boolean,
    default: false,
  },
  orange: {
    type: Boolean,
    default: false,
  },
  "text-only": {
    type: Boolean,
    default: false,
  },
  loading: {
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
  <button
    class="styled-button"
    :class="{
      primary: props.primary,
      green: props.green,
      red: props.red,
      orange: props.orange,
      'text-only': props.textOnly,
    }"
    :disabled="loading || disabled"
  >
    {{ loading ? "Loading..." : props.label }}
  </button>
</template>

<style scoped>
.styled-button {
  min-width: 13rem;
  height: 4rem;
  font-size: 1.6rem;
  border-radius: 1rem;
  border: none;
  outline: none;
  cursor: pointer;
  background-color: var(--secondary-color);
  color: var(--text-primary-color);
  user-select: none;
}

.styled-button.primary {
  background-color: var(--primary-color);
}

.styled-button.green {
  background-color: var(--green-color);
}

.styled-button.red {
  background-color: var(--red-color);
}

.styled-button.orange {
  background-color: var(--orange-color);
}

.styled-button.text-only {
  background-color: transparent;
  min-width: auto;
  width: fit-content;
  border-radius: none;
  height: auto;
}

.styled-button.text-only.primary {
  color: var(--primary-color);
}

.styled-button.primary,
.styled-button.green,
.styled-button.red,
.styled-button.text-only {
  color: var(--text-secondary-color);
}

.styled-button:disabled,
.styled-button.primary:disabled {
  background-color: #ccc;
  color: #aaa;
  cursor: not-allowed;
}
</style>
