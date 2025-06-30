<script setup>
import { useNetworkStructureStore } from '@/stores/networkStructure'
import { useManagerStore } from '@/stores/manager'
import { storeToRefs } from 'pinia'
import { ref, computed, onMounted } from 'vue'
import { inv, multiply, matrix } from "mathjs";

const netstore = useNetworkStructureStore()
const { network, numberblocks, layersOfBlock, numberLayersinblock, layerText } =
  storeToRefs(netstore)

const managerstore = useManagerStore()
const { currentBlock, visibleLayers, isLayerVisible } = storeToRefs(managerstore)
const { hideLayer, revealLayer, setModel } = managerstore

const parentwidth = ref(0)
const parentheight = ref(0)
const margin_inline = computed(() => {
  return parentwidth.value / 20
})

const buttonWidth = computed(() => parentwidth.value / numberblocks.value)

const layer_width = computed(() => {
  return parentwidth.value - 2 * margin_inline.value
})

const layer_height = computed(() => {
  return Math.ceil(parentheight.value / 10)
})

let currenttranform

onMounted(() => {
  const canvas = document.getElementById('canvas')
  parentwidth.value = canvas.parentElement.clientWidth
  parentheight.value = canvas.parentElement.clientHeight
  canvas.addEventListener('mousemove', (event) => changeCursor(event))
  canvas.addEventListener("mousedown", (event) => handleclick(event))
  setModel()
  renderloop()
})

function handleclick(event) {
  var p = [[event.offsetX], [event.offsetY], [1]];
  var mat = inv(
    matrix([
      [currenttranform.a, 0, currenttranform.e],
      [0, currenttranform.d, currenttranform.f],
      [0, 0, 1],
    ])
  );

  var world = multiply(mat, p);

  if (world.get([1, 0]) < layer_height.value) {
    let currentx = 0
    for (let i = 0; i < numberblocks.value; i++) {
      let clicked_button = currentx < world.get([0, 0]) && world.get([0, 0]) < currentx + buttonWidth.value
      if (clicked_button) {
        currentBlock.value = "block_" + [i + 1]
        visibleLayers.value = layersOfBlock.value(currentBlock.value)
        break;
      }
      currentx = currentx + buttonWidth.value
    }
  }

  let y = 2 * layer_height.value
  let blockheight = numberLayersinblock.value(currentBlock.value) * layer_height.value
  let isonblock = margin_inline.value < world.get([0, 0]) &&
    world.get([0, 0]) < layer_width.value + margin_inline.value &&
    y < world.get([1, 0]) &&
    world.get([1, 0]) < y + blockheight
  if (isonblock) {
    let layerindex = 0
    let layerbottom = y + layer_height.value
    while (layerbottom < world.get([1, 0])) {
      layerindex = layerindex + 1
      layerbottom = layerbottom + layer_height.value
    }
    let layername = layersOfBlock.value(currentBlock.value)[layerindex]
    if (isLayerVisible.value(layername)) {
      hideLayer(layername)
      if (visibleLayers.value.length == 0) {
        visibleLayers.value = layersOfBlock.value(currentBlock.value)
      }
    } else {
      revealLayer(layername)
    }
  }
}

function changeCursor(event) {
  const canvas = document.getElementById('canvas')

  var p = [[event.offsetX], [event.offsetY], [1]];

  var mat = inv(
    matrix([
      [currenttranform.a, 0, currenttranform.e],
      [0, currenttranform.d, currenttranform.f],
      [0, 0, 1],
    ])
  );

  var world = multiply(mat, p);

  let isonbutton = world.get([1, 0]) < layer_height.value

  let y = layer_height.value * 2

  let blockheight = numberLayersinblock.value(currentBlock.value) * layer_height.value
  let isonblock =
    margin_inline.value < world.get([0, 0]) &&
    world.get([0, 0]) < layer_width.value + margin_inline.value &&
    y < world.get([1, 0]) &&
    world.get([1, 0]) < y + blockheight

  canvas.style.cursor = isonblock || isonbutton ? 'pointer' : 'default'
}

function renderloop() {
  drawCanvas()
  window.requestAnimationFrame(renderloop)
}

function drawCanvas() {
  const canvas = document.getElementById('canvas')
  parentwidth.value = canvas.parentElement.clientWidth
  parentheight.value = canvas.parentElement.clientHeight
  canvas.width = parentwidth.value
  canvas.height = parentheight.value
  if (currentBlock.value == undefined) {
    currentBlock.value = Object.keys(network.value)[0]
    visibleLayers.value = layersOfBlock.value(currentBlock.value)
  }
  const ctx = canvas.getContext('2d')

  ctx.clearRect(0, 0, canvas.width, canvas.height)

  let x = 0
  currenttranform = ctx.getTransform();

  ctx.font = `normal small-caps bold ${buttonWidth.value * 0.75 - 4}px arial`
  ctx.textAlign = "center";
  for (let i = 0; i < numberblocks.value; i++) {
    let blockname = "block_" + [i + 1]
    ctx.fillStyle = blockname == currentBlock.value ? "aqua" : "transparent";
    ctx.beginPath()
    ctx.rect(x, 0, buttonWidth.value, layer_height.value)
    ctx.fill()
    ctx.stroke()
    ctx.fillStyle = "black"
    ctx.fillText(
      `B${i + 1}`,
      x + buttonWidth.value * 0.45,
      2 * layer_height.value / 3
    )
    x = x + buttonWidth.value
  }
  let blockheight = numberLayersinblock.value(currentBlock.value) * layer_height.value
  ctx.beginPath()
  ctx.rect(margin_inline.value, layer_height.value * 2, layer_width.value, blockheight)
  ctx.stroke()
  let layer_y = layer_height.value * 2
  ctx.textAlign = "start";
  for (let layer of layersOfBlock.value(currentBlock.value)) {
    ctx.beginPath()
    ctx.rect(margin_inline.value, layer_y, layer_width.value, layer_height.value)
    ctx.stroke()
    ctx.fillText(
      layerText.value(layer, currentBlock.value),
      margin_inline.value + 10,
      layer_y + (2 * layer_height.value) / 3
    )
    if (isLayerVisible.value(layer)) {
      ctx.beginPath()
      ctx.arc(canvas.width - margin_inline.value - layer_width.value / 10, layer_y + layer_height.value / 2, layer_height.value / 6, 0, 2 * Math.PI)
      ctx.stroke()
      ctx.beginPath()
      ctx.arc(canvas.width - margin_inline.value - layer_width.value / 10, layer_y + 2 * layer_height.value / 3, layer_height.value / 2, 1.1 * Math.PI, 1.9 * Math.PI)
      ctx.stroke()
    }
    else {
      ctx.beginPath()
      ctx.arc(canvas.width - margin_inline.value - layer_width.value / 10, layer_y + layer_height.value / 3, layer_height.value / 2, 0.9 * Math.PI, 0.1 * Math.PI, true)
      ctx.stroke()
    }
    layer_y = layer_y + layer_height.value
  }
  const legend = document.getElementById('legend_canvas')
  const lctx = legend.getContext('2d')
  lctx.font = "20px serif"
  lctx.beginPath()
  lctx.arc(15, layer_height.value / 2, layer_height.value / 6, 0, 2 * Math.PI)
  lctx.stroke()
  lctx.beginPath()
  lctx.arc(15, 2 * layer_height.value / 3, layer_height.value / 2, 1.1 * Math.PI, 1.9 * Math.PI)
  lctx.stroke()
  lctx.fillText(
    "Layer Visible",
    17 + layer_height.value / 2,
    2 * layer_height.value / 3
  )
  lctx.beginPath()
  lctx.arc(15 + legend.width / 2, layer_height.value / 3, layer_height.value / 2, 0.9 * Math.PI, 0.1 * Math.PI, true)
  lctx.stroke()
  lctx.fillText(
    "Layer Hidden",
    17 + layer_height.value / 2 + legend.width / 2,
    2 * layer_height.value / 3
  )


}
</script>
<template>
  <div id="container">
    <canvas id="canvas"></canvas>
  </div>
  <div id="legend">
    <canvas id="legend_canvas" height="40px" width="400px"></canvas>
  </div>
</template>
<style scoped>
#container {
  width: 100%;
  height: 80%;
  overflow-x: hidden;
  overflow-y: auto;
}

#legend {
  width: 100%;
  height: 20%;
}
</style>
