<script setup>
import LoaderComponent from './LoaderComponent.vue';
</script>
<template>
  <div id="background">
    <div id="loadmsgcontainer">
      <p class="loadmsg">Loading results</p><p class="loadmsg">.</p><p class="loadmsg">.</p><p class="loadmsg">.</p>
    </div>
    <loader-component></loader-component>
  </div>
</template>
<style>
#loadmsgcontainer{
  display: flex;
  align-items: end;
  justify-content: center;
  width: 100%;
  height: 15%;
}
#background{
  display: flex;
  justify-content: center;
  position: absolute;
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0.3);
  overflow: hidden;
}
.loadmsg {
  font-size: 30px;
  font-weight: bolder;
  color: white;
  text-anchor: end;
}

.loadmsg:nth-of-type(2){
  animation: fade 2s linear infinite;
}

.loadmsg:nth-of-type(3){
  animation: fade 2s linear infinite;
  animation-delay: 0.5s;
}

.loadmsg:nth-of-type(4){
  animation: fade 2s linear infinite;
  animation-delay: 1s;
}

@keyframes fade{
  0% {
    opacity: 0;
  }

  50% {
    opacity: 1;
  }
  0% {
    opacity: 0;
  }
}

</style>