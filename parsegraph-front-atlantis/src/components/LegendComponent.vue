<script setup></script>

<template>
  <h4>IMPACT</h4>
  <div id="gradient"></div>
  <div class="legend">
    <label class="legendlabel">High Negative</label>
    <label class="legendlabel">Null</label>
    <label class="legendlabel">High positive</label>
  </div>
  <h4>INFLUENCE</h4>
  <div class="legend">
    <div class="flex">
      <div class="circle" style="width: 30px; height: 30px"></div>
      <label class="legendlabel">Non Critical Neuron</label>
    </div>
    <div class="flex">
      <div class="circle" style="width: 60px; height: 60px"></div>
      <label class="legendlabel">Critical Neuron</label>
    </div>
  </div>
</template>

<style scoped>
#gradient {
  width: 99%;
  height: 25px;
  margin-inline: 0.5%;
  border: solid 1px black;
  background: linear-gradient(to right,
      rgb(0%, 0%, 100%) 0%,
      rgb(0%, 100%, 0%) 50%,
      rgb(100%, 0%, 0%) 100%);
}

.flex {
  padding: 5px;
  display: flex;
}

.legend {
  display: flex;
  flex-direction: row;
  width: 100%;
  justify-content: space-between;
}

.legendlabel {
  margin: 0.5%;
  font-style: italic;
  font-size: larger;
}

.circle {
  background-color: black;
  border-radius: 50%;
  margin: 3px;
}

h4 {
  width: 100%;
  height: fit-content;
  text-align: center;
  font-weight: bold;
  border: solid 2px black;
  margin-top: 0;
}
</style>
