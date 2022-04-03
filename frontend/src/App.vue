<script setup>
import { ref, provide, onBeforeMount } from "vue";
import { RouterView } from "vue-router";
import MainHeader from "./components/MainHeader.vue";
import FlagsContainer from "./components/FlagsContainer.vue";
import { getUserId, isAuthenticated, logout } from "./services/auth";
import { getUser } from "./services/friendsApi";

const user = ref(null);

function updateUser(newUser) {
  user.value = newUser;
}

provide("user", { user, updateUser });

onBeforeMount(async () => {
  if (isAuthenticated()) {
    const userId = getUserId();

    try {
      const response = await getUser(userId);
      user.value = response.data.data;
    } catch (err) {
      logout();
      user.value = null;
    }
  }
});
</script>

<template>
  <MainHeader />

  <FlagsContainer />

  <RouterView v-slot="{ Component }">
    <KeepAlive :max="5">
      <component :is="Component"></component>
    </KeepAlive>
  </RouterView>
</template>

<style>
@import "@/assets/base.css";
</style>
