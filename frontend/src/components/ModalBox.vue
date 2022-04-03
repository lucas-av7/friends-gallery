<template>
  <div class="modal-box">
    <slot></slot>
  </div>
</template>
<style scoped>
.modal-box {
  width: auto;
  height: auto;
  box-shadow: 0.5rem 0.5rem 1rem #222;
  border-radius: 1rem;
  overflow: hidden;
}
</style>
