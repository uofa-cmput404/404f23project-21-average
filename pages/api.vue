<template></template>
    
<script lang="ts" setup>
import { navigateTo, useRuntimeConfig } from 'nuxt/app';
const config = useRuntimeConfig();

navigateTo(config.public.baseUrl, { external: true })

</script>