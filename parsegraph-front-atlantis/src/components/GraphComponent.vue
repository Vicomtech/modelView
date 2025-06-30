<script setup>
import { onMounted, ref, watch } from 'vue';
import { lerp } from '@/modules/utils';
import { inv, multiply, matrix } from "mathjs";
import { useManagerStore } from '@/stores/manager'
import { storeToRefs } from 'pinia'

const managerstore = useManagerStore()
const {
  background,
  currentBlock,
  currentNodes,
  selectedNeuron,
  nodedict,
  layerdict,
  interpretabilitydict,
  isNodeVisible,
  maxImpact,
  minImpact,
  modelfile,
  currentscale,
  translation,
  size,
  canvaswidth,
  canvasheight,
  apiservice,
  mode
} = storeToRefs(managerstore)

const props = defineProps({
  ready: Boolean
})

let text = ""
let pan = false
let scale = 1
let currettranform

let currentx = 0
let currenty = 0

const animframe = ref(0)

watch(() => props.ready, (value) => {
  if (value) {
    apiservice.value.execute("getBlockLayers", {}, { "block": currentBlock.value, "model": (mode.value == "REMOTE" ? "default" : modelfile.value.split(".")[0]) })
      .then((result) => {
        let dict = {}
        for (let layer of result) {
          dict[layer['id']] = layer['layer']
        }
        layerdict.value = dict
        for (let node of currentNodes.value) {
          let lname = layerdict.value[node["layer"]]
          let nodenumber = node["filterinlayer"] - 1
          node["impact"] = Object.keys(interpretabilitydict.value).length > 0 ? interpretabilitydict.value[lname]['data'][nodenumber][0] : 0
          node["expertise"] = Object.keys(interpretabilitydict.value).length > 0 ? interpretabilitydict.value[lname]['data'][nodenumber][1] : 1
        }
        if (value) {
          for (let node of currentNodes.value) {
            let lname = layerdict.value[node["layer"]]
            let nodenumber = node["filterinlayer"] - 1
            node["impact"] = interpretabilitydict.value[lname]['data'][nodenumber][0]
            node["expertise"] = interpretabilitydict.value[lname]['data'][nodenumber][1]
          }
        }
      })
  }
})

watch(() => currentBlock.value, (value) => {

  apiservice.value.execute("getBlocknodes", {}, { "block": value.toLowerCase(), "model": mode.value == "REMOTE" ? "default" : modelfile.value.split(".")[0] })
    .then((resp) => {
      currentNodes.value = resp
      let dict = {}
      let index = 0
      for (let val of currentNodes.value) {
        val["currentX"] = 0
        val["currentY"] = 0
        let n_name = `${val["layer"]}_${val.filterinlayer}`
        val["n_name"] = n_name
        val["impact"] = 0
        val["expertise"] = 0
        dict[n_name] = index
        index += 1
      }
      nodedict.value = dict
    })
})

const canvas = ref()
const ctx = ref()

function loop() {
  currentscale.value = lerp(currentscale.value, scale, 0.1);
  for (var node of currentNodes.value) {
    node.currentX = lerp(node.currentX, node.positionX, 0.005);
    node.currentY = lerp(node.currentY, node.positionY, 0.005);
  }
  draw()
  animframe.value = window.requestAnimationFrame(loop);
}

onMounted(() => {
  canvas.value = document.getElementById("gcanvas");
  ctx.value = canvas.value.getContext("2d");
  canvaswidth.value = document.getElementById("parent").clientWidth;
  canvasheight.value = document.getElementById("parent").clientHeight;
  canvas.value.width = document.getElementById("parent").clientWidth;
  canvas.value.height = document.getElementById("parent").clientHeight;

  canvas.value.addEventListener("mousedown", async (evt) => {
    switch (evt.button) {
      case 0:
        var p = [[evt.offsetX], [evt.offsetY], [1]];
        var mat = inv(
          matrix([
            [currettranform.a, 0, currettranform.e],
            [0, currettranform.d, currettranform.f],
            [0, 0, 1],
          ])
        );
        var world = multiply(mat, p);
        for (var node of currentNodes.value) {
          if (
            node.currentX - size.value * (node.expertise + 1) < world.get([0, 0]) &&
            node.currentX + size.value * (node.expertise + 1) > world.get([0, 0]) &&
            node.currentY - size.value * (node.expertise + 1) < world.get([1, 0]) &&
            node.currentY + size.value * (node.expertise + 1) > world.get([1, 0]) &&
            node.expertise == 1
          ) {
            selectedNeuron.value = node.n_name;
          }
        }
        break;
      case 1:
        break;
      case 2:
        pan = true;
        break;
    }
  });
  canvas.value.addEventListener("mouseup", (evt) => {
    if (evt.button == 2) {
      pan = false;
    }
  });
  canvas.value.addEventListener("mousemove", (evt) => {
    if (pan) {
      translation.value[0] += evt.movementX / currentscale.value;
      translation.value[1] += evt.movementY / currentscale.value;
    } else {
      var p = [[evt.offsetX], [evt.offsetY], [1]];
      var mat = inv(
        matrix([
          [currettranform.a, 0, currettranform.e],
          [0, currettranform.d, currettranform.f],
          [0, 0, 1],
        ])
      );
      var world = multiply(mat, p);
      text = "";
      canvas.value.style.cursor = 'default'
      for (var node of currentNodes.value) {
        if (
          node.currentX - size.value * (node.expertise + 1) < world.get([0, 0]) &&
          node.currentX + size.value * (node.expertise + 1) > world.get([0, 0]) &&
          node.currentY - size.value * (node.expertise + 1) < world.get([1, 0]) &&
          node.currentY + size.value * (node.expertise + 1) > world.get([1, 0])
        ) {
          text = node.n_name
          text = text.split("_")
          text = text[text.length - 1]
          currentx = evt.offsetX
          currenty = evt.offsetY
          if (node.expertise == 1) {
            canvas.value.style.cursor = 'pointer'
          }
        }
      }
    }
  });

  canvas.value.addEventListener("mouseleave", () => {
    pan = false;
  });

  canvas.value.addEventListener("wheel", (evt) => {
    evt.preventDefault();
    currentscale.value = scale;
    scale += evt.deltaY * -0.0015;
    scale = Math.min(Math.max(0.10, Number(scale.toFixed(2))), 1);
  });

  window.requestAnimationFrame(loop)
})

function draw() {
  canvas.value = document.getElementById("gcanvas");
  ctx.value = canvas.value.getContext("2d");
  canvaswidth.value = document.getElementById("parent").clientWidth;
  canvasheight.value = document.getElementById("parent").clientHeight;
  canvas.value.width = document.getElementById("parent").clientWidth;
  canvas.value.height = document.getElementById("parent").clientHeight;

  ctx.value.clearRect(0, 0, canvas.value.width, canvas.value.height);

  ctx.value.translate(canvas.value.width / 2, canvas.value.height / 2);
  ctx.value.scale(currentscale.value, currentscale.value);

  ctx.value.translate(
    -canvas.value.width / 2 + translation.value[0],
    -canvas.value.height / 2 + translation.value[1]
  );
  currettranform = ctx.value.getTransform();
  for (var node of currentNodes.value) {
    let active = isNodeVisible.value(node.n_name)

    let bluerange = 100 / Math.max(Math.abs(minImpact.value), 1);
    let redrange = 100 / Math.max(Math.abs(maxImpact.value), 1);
    let linval =
      node.impact > 0
        ? node.impact * redrange
        : Math.abs(node.impact) * bluerange;
    let expval = linval != 0 ? 50 * Math.log10(linval) : 0;
    ctx.value.fillStyle = active
      ? node.impact > 0
        ? `rgb(${expval}%,${100 - expval}%,0% )`
        : `rgb(0%,${100 - expval}%,${expval}% )`
      : "rgba(0,0,0,0)";

    ctx.value.strokeStyle = active
      ? node.n_name == selectedNeuron.value
        ? "#24DDEC"
        : "black"
      : background.value
        ? "rgba(0,0,0,0.3)"
        : "rgba(0,0,0,0)";
    ctx.value.lineWidth = 5;
    var newsize = (node.expertise + 1) * size.value;
    ctx.value.beginPath();
    ctx.value.arc(node.currentX, node.currentY, newsize, 0, 2 * Math.PI);
    ctx.value.fill();
    ctx.value.stroke();
  }
  ctx.value.setTransform(1, 0, 0, 1, 0, 0);
  ctx.value.font = "bold 14pt Arial";
  ctx.value.fillStyle = "black";
  ctx.value.strokeStyle = "#EBEDEF";
  ctx.value.lineWidth = 0.5;
  ctx.value.textAlign = "center";
  ctx.value.fillText(text, currentx, currenty - 10);
  ctx.value.strokeText(text, currentx, currenty - 10);
}

</script>
<template>
  <div id="parent">
    <canvas id="gcanvas" oncontextmenu="return false;"></canvas>
  </div>
</template>
<style scoped>
#parent {
  width: 100%;
  height: 100%;
  background-color: aliceblue;
  overflow: hidden;
}
</style>