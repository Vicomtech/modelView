<script setup>
</script>
<template>
  <div class="loader"></div>
</template>
<style>
  .loader {
    position: absolute;
    border: 10px dotted var(--color-text); /* Blue */
    border-spacing: 1cap;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    top: 25%;
    animation: spin 3s linear infinite;
  }

  @keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>