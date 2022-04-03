<script setup>
const props = defineProps({
  big: {
    type: Boolean,
    default: false,
  },
  small: {
    type: Boolean,
    default: false,
  },
  url: String,
});
</script>
<template>
  <div class="photo-thumb" :class="{ big: props.big, small: props.small }">
    <img
      :src="url"
      :class="{ big: props.big }"
      class="photo-thumb__img"
      loading="lazy"
    />
  </div>
</template>
<style scoped>
.photo-thumb {
  width: 23.6rem;
  height: 23.6rem;
}

.photo-thumb.big {
  width: auto;
  height: auto;
  max-height: 50rem;
}

.photo-thumb.small {
  width: 10rem;
  height: 10rem;
}

.photo-thumb__img {
  height: 100%;
  width: 100%;
  object-fit: cover;
}

.photo-thumb__img.big {
  max-height: 50rem;
  object-fit: contain;
}
</style>
