<template>
  <div class="no-photos">
    <font-awesome-icon class="no-photos__icon" icon="camera" />
    <p class="no-photos__label">No photos to show yet</p>
  </div>
</template>
<style scoped>
.no-photos {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  margin-top: 6rem;
}

.no-photos__icon {
  padding: 2rem;
  border-radius: 50%;
  border: 0.3rem solid var(--text-primary-color);
  font-size: 4rem;
  color: var(--text-primary-color);
}

.no-photos__label {
  margin-top: 1rem;
  color: var(--text-primary-color);
  font-size: 2rem;
}
</style>
