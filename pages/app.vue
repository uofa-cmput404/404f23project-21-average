<template>
  <header>
    <nav>
      <ul>
        <li>
          <NuxtLink to="/loginPage">login</NuxtLink>
        </li>
        <li>
          <NuxtLink to="/profilePage">Profile Page</NuxtLink>
        </li>
        <li>
          <NuxtLink to="/searchPage">Search Page</NuxtLink>
        </li>
        <li>
          <NuxtLink to="/friendsPage">Search Page</NuxtLink>
        </li>
      </ul>
    </nav>
  </header>
</template>
<script setup lang="ts">
import { navigateTo, useRuntimeConfig } from 'nuxt/app';
const config = useRuntimeConfig();

navigateTo('/loginPage')
</script>