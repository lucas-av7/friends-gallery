<script setup>
import validator from "validator";
import { ref, computed, getCurrentInstance, inject } from "vue";
import { createUser, loginUser } from "../services/friendsApi";
import { login } from "../services/auth";
import StyledButton from "./StyledButton.vue";
import ModalBox from "./ModalBox.vue";
import StyledInput from "./StyledInput.vue";

const globals = getCurrentInstance().appContext.config.globalProperties;

const { updateUser } = inject("user");

const showModal = ref(false);
const register = ref(false);
const loading = ref(false);
const name = ref("");
const email = ref("");
const password = ref("");

const buttonDisabled = computed(() => {
  return (
    loading.value ||
    !validator.isEmail(email.value) ||
    password.value.length < 8 ||
    (register.value && !name.value)
  );
});

function toggleModal() {
  showModal.value = !showModal.value;
  register.value = false;
  name.value = "";
  email.value = "";
  password.value = "";
}

async function handleLogin() {
  try {
    const response = await loginUser({
      email: email.value,
      password: password.value,
    });

    const { token, user } = response.data.data;
    login(user._id, token);
    toggleModal();
    updateUser(user);

    globals.$emitter.emit("flag-message", {
      content: "Successfully logged in.",
      modifier: "success",
    });
  } catch (err) {
    const status = err.response.status;

    globals.$emitter.emit("flag-message", {
      content: status === 401 ? "Invalid credentials." : "Unable to execute.",
      modifier: "error",
    });
  }
}

async function handleCreate() {
  try {
    await createUser({
      name: name.value,
      email: email.value,
      password: password.value,
    });

    globals.$emitter.emit("flag-message", {
      content: "Account created successfully.",
      modifier: "success",
    });
  } catch (err) {
    const status = err.response.status;

    globals.$emitter.emit("flag-message", {
      content: status === 400 ? "E-mail already in use." : "Unable to execute.",
      modifier: "error",
    });
  }
}

async function handleSubmitUserInfo() {
  if (buttonDisabled.value) {
    return;
  }

  loading.value = true;

  if (register.value) {
    await handleCreate();
  }

  await handleLogin();

  loading.value = false;
}
</script>
<template>
  <div class="login-box">
    <StyledButton @click="toggleModal" label="Log in" />
    <ModalBox v-if="showModal" class="login-modal">
      <div class="login-form">
        <StyledInput
          @keypress.enter="handleSubmitUserInfo"
          v-if="register"
          v-model="name"
          class="input"
          type="text"
          placeholder="Name"
        />
        <StyledInput
          @keypress.enter="handleSubmitUserInfo"
          v-model="email"
          class="input"
          type="email"
          placeholder="E-mail"
        />
        <StyledInput
          v-model="password"
          class="input"
          type="password"
          min="8"
          placeholder="Password"
          @keypress.enter="handleSubmitUserInfo"
        />

        <StyledButton
          @click="handleSubmitUserInfo"
          :label="register ? 'Create' : 'Log in'"
          :disabled="buttonDisabled"
          :loading="loading"
          class="action-button"
          primary
        />
        <StyledButton
          @click="register = !register"
          :label="register ? 'Back to log in' : 'Create account'"
          class="text-button"
          primary
          text-only
        />
      </div>
    </ModalBox>
  </div>
  <div class="modal-close-area" v-if="showModal" @click="toggleModal"></div>
</template>
<style scoped>
.login-box {
  position: relative;
}

.login-modal {
  position: absolute;
  top: 0;
  right: 0;
  z-index: 11;
}

.login-form {
  width: 25rem;
  padding: 1.5rem;
  background-color: var(--secondary-color);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.input,
.action-button,
.text-button {
  width: 22rem;
}

.input {
  margin-bottom: 0.5rem;
}

.action-button {
  margin-top: 1rem;
}

.text-button {
  margin-top: 1.6rem;
}

.modal-close-area {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 10;
  width: 100vw;
  height: 100vh;
}
</style>
