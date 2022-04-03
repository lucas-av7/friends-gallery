<script setup>
import { inject, ref } from "vue";
import ModalBox from "./ModalBox.vue";
import StyledButton from "./StyledButton.vue";
import IconButton from "./IconButton.vue";
import { logout } from "../services/auth";
import SendPhotoModal from "./SendPhotoModal.vue";

const props = defineProps({
  name: String,
});

const showModal = ref(false);
const showSendPhotoModal = ref(false);
const { user, updateUser } = inject("user");

function hideModals() {
  showModal.value = false;
  showSendPhotoModal.value = false;
}

function handleLogout() {
  logout();
  showModal.value = false;
  updateUser(null);
}
</script>
<template>
  <div class="user-menu">
    <IconButton icon="user" @click="showModal = true" />
    <ModalBox v-if="showModal" class="user-modal">
      <div class="user-options">
        <span class="user-name">Hello, {{ props.name }}!</span>
        <nav class="user-nav">
          <router-link to="/admin">
            <StyledButton
              v-if="user.is_admin"
              @click="showModal = false"
              label="Admin panel"
              text-only
              primary
            />
          </router-link>
          <StyledButton
            @click="showSendPhotoModal = true"
            label="Send photo"
            text-only
            primary
          />
          <StyledButton
            @click="handleLogout"
            label="Log out"
            text-only
            primary
          />
        </nav>
      </div>
    </ModalBox>
    <SendPhotoModal v-if="showSendPhotoModal" class="send-photo-modal" />
  </div>
  <div
    class="modal-close-area"
    v-if="showModal || showSendPhotoModal"
    @click="hideModals"
  ></div>
</template>
<style scoped>
.user-menu {
  position: relative;
}

.user-modal,
.send-photo-modal {
  position: absolute;
  top: 0;
  right: 0;
  z-index: 11;
}

.modal-close-area {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 10;
  width: 100vw;
  height: 100vh;
}

.user-options {
  padding: 1.5rem;
  background-color: var(--secondary-color);
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 25rem;
}

.user-name {
  font-size: 1.6rem;
  border-bottom: 0.3rem solid var(--primary-color);
}

.user-nav {
  margin-top: 1rem;
  display: flex;
  flex-direction: column;
}

.user-nav :not(:last-child) {
  margin-bottom: 0.5rem;
}
</style>
