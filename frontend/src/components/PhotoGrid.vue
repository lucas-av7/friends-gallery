<script setup>
import { ref, onBeforeMount, getCurrentInstance } from "vue";
import { getPhotos } from "../services/friendsApi";
import NoPhotos from "@/components/NoPhotos.vue";
import PhotoThumb from "./PhotoThumb.vue";

const globals = getCurrentInstance().appContext.config.globalProperties;

const photos = ref([]);

onBeforeMount(async () => {
  try {
    const response = await getPhotos();
    photos.value = response.data.data;
  } catch (err) {
    photos.value = [];
    globals.$emitter.emit("flag-message", {
      content: "Unable to retrieve photos.",
      modifier: "error",
    });
  }
});
</script>
<template>
  <div v-if="photos.length > 0" class="photo-grid">
    <h2>Wedding photos</h2>
    <div class="photo-grid__photos">
      <router-link
        v-for="(photo, index) in photos"
        :to="`/photo/${photo._id}`"
        :key="index"
      >
        <PhotoThumb :url="photo.url" class="photo-grid__photo" />
      </router-link>
    </div>
  </div>
  <NoPhotos v-else />
</template>
<style scoped>
.photo-grid {
  width: 100%;
  height: auto;
}

.photo-grid h2 {
  color: var(--text-primary-color);
  font-size: 2rem;
}

.photo-grid__photos {
  width: 100%;
  display: flex;
  flex-wrap: wrap;
}

.photo-grid__photo {
  margin: 0.5rem;
  cursor: pointer;
}

@media screen and (max-width: 532px) {
  .photo-grid__photos {
    flex-direction: column;
    align-items: center;
  }
}
</style>
