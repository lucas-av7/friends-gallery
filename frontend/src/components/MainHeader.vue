<script setup>
import { inject } from "vue";
import LoginBox from "./LoginBox.vue";
import UserMenu from "./UserMenu.vue";

const { user } = inject("user");
</script>
<template>
  <header class="main-header">
    <div class="container">
      <router-link to="/">
        <h1>Friend's Gallery</h1>
      </router-link>
      <UserMenu v-if="user" :name="user.name" />
      <LoginBox v-else />
    </div>
  </header>
</template>
<style scoped>
.main-header {
  width: 100%;
  background-color: var(--primary-color);
}

.main-header .container {
  margin: 0 auto;
  max-width: 102.4rem;
  height: 6rem;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.main-header .container h1 {
  font-size: 2rem;
  color: var(--text-secondary-color);
}
</style>
