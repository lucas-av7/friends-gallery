<script setup>
import { ref, computed, getCurrentInstance } from "vue";
import { sendPhoto } from "../services/friendsApi";
import ModalBox from "./ModalBox.vue";
import StyledInput from "./StyledInput.vue";
import StyledButton from "./StyledButton.vue";

const globals = getCurrentInstance().appContext.config.globalProperties;

const photoInputRef = ref(null);
const photoPreview = ref(null);
const base64img = ref(null);
const photoTitle = ref("");
const loading = ref(false);

const allowedFileTypes = ["image/jpeg", "image/jpg"];

const buttonDisabled = computed(() => {
  return !photoPreview.value || photoTitle.value.length < 3;
});

function handleFileSelected(event) {
  const type = event.target.files[0].type;
  if (allowedFileTypes.includes(type)) {
    const file = event.target.files[0];
    photoPreview.value = URL.createObjectURL(file);

    const fr = new FileReader();
    fr.onloadend = () => {
      base64img.value = fr.result.replace("data:image/jpeg;base64,", "");
    };
    fr.readAsDataURL(file);
  }
}

async function handleSendPhoto() {
  if (buttonDisabled.value) {
    return;
  }

  loading.value = true;

  try {
    await sendPhoto({
      title: photoTitle.value,
      base64_img: base64img.value,
    });

    globals.$emitter.emit("flag-message", {
      content: "Photo sent successfully. Waiting for admin approval.",
      modifier: "success",
    });

    photoPreview.value = null;
    base64img.value = null;
    photoTitle.value = "";
  } catch (err) {
    globals.$emitter.emit("flag-message", {
      content: "Unable to execute.",
      modifier: "error",
    });
  }

  loading.value = false;
}
</script>
<template>
  <ModalBox class="send-photo-modal">
    <div class="photo-form">
      <div
        class="photo-preview"
        @click="photoInputRef.click()"
        title="Select photo"
      >
        <img
          class="photo-preview__img"
          v-if="photoPreview"
          :src="photoPreview"
          alt="Photo preview"
        />
        <font-awesome-icon v-else class="camera__icon" icon="camera" />
      </div>
      <input
        class="photo-input"
        type="file"
        name="photo"
        ref="photoInputRef"
        :accept="allowedFileTypes.join(',')"
        @change="handleFileSelected"
      />
      <StyledInput
        @keypress.enter="handleSendPhoto"
        v-model="photoTitle"
        class="photo-title-input"
        type="text"
        placeholder="Photo title"
      />
      <StyledButton
        @click="handleSendPhoto"
        :disabled="buttonDisabled"
        :loading="loading"
        label="Send"
        primary
      />
    </div>
  </ModalBox>
</template>
<style scoped>
.send-photo-modal {
  position: absolute;
  top: 0;
  right: 0;
  z-index: 11;
  user-select: none;
}

.photo-form {
  width: 25rem;
  padding: 1.5rem;
  background-color: var(--secondary-color);
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.photo-preview {
  align-self: center;
  cursor: pointer;
  border: 0.3rem solid var(--text-primary-color);
  border-radius: 1rem;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 10rem;
  height: 10rem;
  font-size: 4rem;
  overflow: hidden;
}

.photo-preview__img {
  height: 100%;
  width: 100%;
  object-fit: cover;
}

.photo-input {
  display: none;
}

.photo-title-input {
  margin-top: 0.5rem;
  margin-bottom: 1rem;
}
</style>
