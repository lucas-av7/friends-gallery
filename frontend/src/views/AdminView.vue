<script setup>
import { inject, onBeforeMount, ref, getCurrentInstance } from "vue";
import {
  getPhotos,
  getPendingPhotos,
  deletePhoto,
  approvePhoto,
} from "../services/friendsApi";
import PhotoThumb from "../components/PhotoThumb.vue";
import StyledButton from "../components/StyledButton.vue";
import NoPhotos from "../components/NoPhotos.vue";

const globals = getCurrentInstance().appContext.config.globalProperties;
const { user } = inject("user");

const approvedPhotos = ref([]);
const pendingPhotos = ref([]);
const viewOption = ref("approved");

onBeforeMount(async () => {
  try {
    const response = await getPhotos();
    approvedPhotos.value = response.data.data;
  } catch (err) {
    approvedPhotos.value = [];
    globals.$emitter.emit("flag-message", {
      content: "Unable to retrieve approved photos.",
      modifier: "error",
    });
  }

  try {
    const response = await getPendingPhotos();
    pendingPhotos.value = response.data.data;
  } catch (err) {
    pendingPhotos.value = [];
    globals.$emitter.emit("flag-message", {
      content: "Unable to retrieve pending photos.",
      modifier: "error",
    });
  }
});

async function handleDeletePhoto(photoIndex) {
  const photos =
    viewOption.value === "approved" ? approvedPhotos : pendingPhotos;
  const photo = photos.value[photoIndex];

  try {
    photos.value.splice(photoIndex, 1);
    await deletePhoto(photo._id);
  } catch (err) {
    photos.value.splice(photoIndex, 0, photo);

    globals.$emitter.emit("flag-message", {
      content: `Unable to delete photo.`,
      modifier: "error",
    });
  }
}

async function handleApprovePhoto(photoIndex) {
  const photo = pendingPhotos.value[photoIndex];
  const currentLastApprovedIndex = approvedPhotos.value.length;

  try {
    approvedPhotos.value.push(photo);
    pendingPhotos.value.splice(photoIndex, 1);

    await approvePhoto(photo._id);
  } catch (err) {
    pendingPhotos.value.splice(photoIndex, 0, photo);
    approvedPhotos.value.splice(currentLastApprovedIndex, 1);

    globals.$emitter.emit("flag-message", {
      content: `Unable to approve photo.`,
      modifier: "error",
    });
  }
}
</script>
<template>
  <div v-if="user && user.is_admin" class="admin-view">
    <div class="view-options">
      <p class="view-options__label">Showing {{ viewOption }} photos</p>

      <StyledButton
        @click="viewOption = 'approved'"
        :disabled="viewOption === 'approved'"
        :label="`Approved (${approvedPhotos.length})`"
        title="Click to see approved photos"
        green
      />

      <StyledButton
        @click="viewOption = 'pending'"
        :disabled="viewOption === 'pending'"
        :label="`Pending (${pendingPhotos.length})`"
        title="Click to see pending photos"
        orange
      />
    </div>
    <table
      v-if="
        (viewOption === 'pending' && pendingPhotos.length > 0) ||
        (viewOption === 'approved' && approvedPhotos.length > 0)
      "
      class="photo-table"
    >
      <colgroup>
        <col />
        <col />
        <col />
        <col />
      </colgroup>
      <tr>
        <th>Photo</th>
        <th>Title</th>
        <th>Owner</th>
        <th>Actions</th>
      </tr>
      <tr
        v-for="(photo, index) in viewOption === 'approved'
          ? approvedPhotos
          : pendingPhotos"
        :key="photo._id"
      >
        <td>
          <PhotoThumb :url="photo.url" small />
        </td>
        <td>
          {{ photo.title }}
        </td>
        <td>
          {{ photo.user.name }}
        </td>
        <td>
          <StyledButton
            v-if="viewOption === 'pending'"
            @click="() => handleApprovePhoto(index)"
            label="Approve"
            title="Click to approve"
            green
          />
          <StyledButton
            @click="() => handleDeletePhoto(index)"
            title="Click to delete photo"
            label="Delete"
            red
          />
        </td>
      </tr>
    </table>
    <NoPhotos v-else />
  </div>
</template>
<style scoped>
.admin-view {
  width: 100%;
  max-width: 102.4rem;
  margin: 1rem auto;
  padding: 0 2rem;
  font-size: 1.6rem;
}

.view-options {
  width: 100%;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin-bottom: 1rem;
}

.view-options__label {
  margin-right: 1rem;
}

.view-options *:last-of-type {
  margin-left: 1rem;
}

.photo-table {
  width: 100%;
  outline: none;
  border: none;
  border-collapse: collapse;
  text-align: left;
  table-layout: fixed;
}

.photo-table col {
  width: 100%;
}

.photo-table col:first-of-type {
  width: 14rem;
}

.photo-table col:last-child {
  width: 15rem;
}

.photo-table tr:nth-child(odd) {
  background-color: var(--secondary-color);
  color: var(--text-primary-color);
}

.photo-table tr:nth-child(even) {
  background-color: var(--primary-color);
  color: var(--text-secondary-color);
}

.photo-table th,
.photo-table td {
  padding: 1rem;
}

.photo-table td:last-child > *:first-of-type {
  margin-bottom: 1rem;
}

@media screen and (max-width: 532px) {
  .photo-table col:nth-of-type(3),
  .photo-table th:nth-of-type(3),
  .photo-table td:nth-of-type(3) {
    display: none;
  }
}
</style>
