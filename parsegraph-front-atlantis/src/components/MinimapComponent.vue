<script setup>
import { onMounted, ref } from 'vue';
import { lerp } from '@/modules/utils';
import { useManagerStore } from '@/stores/manager'
import { storeToRefs } from 'pinia'

const managerstore = useManagerStore()
const {
  maxX,
  maxY,
  minX,
  minY,
  currentNodes,
  currentscale,
  translation,
  canvaswidth,
  canvasheight,
  size,
  isLayerVisible
} = storeToRefs(managerstore)

const canvas = ref()
const ctx = ref()

const minimaptranslation = ref(0, 0)

onMounted(() => {
  minimaptranslation.value = [
    (maxX.value - minX.value) / 2 - canvaswidth.value * 2,
    (maxY.value - minY.value) / 2 - canvasheight.value * 2,
  ]
  window.requestAnimationFrame(loop)
})

function loop() {
  for (var node of currentNodes.value) {
    node.currentX = lerp(node.currentX, node.positionX, 0.005);
    node.currentY = lerp(node.currentY, node.positionY, 0.005);
  }
  draw()
  window.requestAnimationFrame(loop);
}

function draw() {
  canvas.value = !canvas.value ? document.getElementById("minimapcanvas") : canvas.value;
  ctx.value = canvas.value.getContext("2d");
  canvas.value.width = document.getElementById("minimapcontainer").clientWidth;
  canvas.value.height = document.getElementById("minimapcontainer").clientHeight;

  ctx.value.clearRect(0, 0, canvas.value.width, canvas.value.height);
  ctx.value.setTransform(1, 0, 0, 1, 0, 0);
  ctx.value.translate(canvas.value.width / 2, canvas.value.height / 2);
  ctx.value.scale(0.04, 0.04);
  ctx.value.translate(
    -canvas.value.width * 10,
    -canvas.value.height * 10
  );
  for (var node of currentNodes.value) {
    let active = isLayerVisible.value(node.block_layer)
    ctx.value.fillStyle = active ? "rgba(0,0,0,1)" : "rgba(0,0,0,0.3)";

    ctx.value.strokeStyle = active ? "rgba(0,0,0,1)" : "rgba(0,0,0,0.3)";
    var newsize = size.value;
    ctx.value.beginPath();
    ctx.value.arc(node.currentX, node.currentY, newsize, 0, 2 * Math.PI);
    ctx.value.fill();
    ctx.value.stroke();
  }

  ctx.value.setTransform(1, 0, 0, 1, 0, 0);
  ctx.value.translate(canvas.value.width / 2, canvas.value.height / 2);
  ctx.value.scale(0.04, 0.04);
  ctx.value.translate(
    -canvas.value.width * 9 - translation.value[0],
    -canvas.value.height * 9 - translation.value[1]);
  ctx.value.fillStyle = "rgba(0,200,200,0.2)";
  ctx.value.beginPath();
  ctx.value.rect(
    -canvaswidth.value / (2 * currentscale.value),
    -canvasheight.value / (2 * currentscale.value),
    canvaswidth.value / currentscale.value,
    canvasheight.value / currentscale.value
  );
  ctx.value.fill();

  ctx.value.setTransform(1, 0, 0, 1, 0, 0);

}
</script>
<template>
  <div id="minimapcontainer">
    <canvas id="minimapcanvas" oncontextmenu="return false;"></canvas>
  </div>
</template>
<style scoped>
#minimapcontainer {
  width: 100%;
  height: 100%;
  overflow: hidden;
}
</style>