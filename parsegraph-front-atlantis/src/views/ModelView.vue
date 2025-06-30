<script setup>
import { onMounted, ref, onBeforeMount } from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faArrowRightArrowLeft, faExclamationTriangle } from '@fortawesome/free-solid-svg-icons'
import LegendComponent from '@/components/LegendComponent.vue'
import BlockSelectorComponent from '@/components/BlockSelectorComponent.vue'
import MinimapComponent from '@/components/MinimapComponent.vue'
import OverlayComponent from '@/components/OverlayComponent.vue'
import GraphComponent from '@/components/GraphComponent.vue'
import { useManagerStore } from '@/stores/manager'
import { storeToRefs } from 'pinia'
import { watch } from 'vue'

const managerstore = useManagerStore()
const { selectedImageName, selectedimagematrix, selectedNeuron, background, interpretabilitydict, currentBlock, apiservice, mode } = storeToRefs(managerstore)

watch(
  currentBlock,
  (value) => {
    let num = Number(value.split("_")[1])
    let init = Date.now() / 1000
    model_loading.value = true
    crit_nodes.value = 0
    totalnodes.value = 0
    if (mode.value == "REMOTE") {
      apiservice.value.execute("getInterpretabilitybyBlock",
        {
          "Content-Type": "application/json",
        }, { "n_block": num, "face": selectedimagematrix.value - 1 }).then((resp) => {

          interpretabilitydict.value = resp
          let end = Date.now() / 1000
          let total = (end - init) / 60
          let values = Object.values(interpretabilitydict.value)
          crit_nodes.value = values[values.length - 2]
          totalnodes.value = values[values.length - 1]
          console.log(`it took ${Math.floor(total)} minutes and ${Math.round((total - Math.floor(total)) * 60)} to end request}`)
          model_loading.value = false
        })
    }
    else if (mode.value == "LOCAL") {
      let split = selectedImageName.value.split("/")
      let imagename = split[split.length - 1].split(".")[0]
      let num = Number(value.split("_")[1])
      let path = `data/interpretability/${imagename}/block${num}.json`
      fetch(path).then((response) => response.json()).then((value) => {

        interpretabilitydict.value = value
        let values = Object.values(interpretabilitydict.value)
        crit_nodes.value = values[values.length - 2]
        totalnodes.value = values[values.length - 1]
        setTimeout(() => model_loading.value = false, 1000)
      })
    }

  })

watch(selectedNeuron, (value) => {
  explainability_loading.value = true
  src.value = ""
  const split = value.split("_")
  const layer = Number(split[1])
  const neuron = Number(split[2])
  if (mode.value == "REMOTE") {
    apiservice.value.execute("getExplainability", {
      "Content-Type": "application/json",
    }, { "layer": layer, "channel": neuron, "face": selectedimagematrix.value - 1 }, undefined, "file").then((resp) => {
      explainability_loading.value = false
      const objectURL = URL.createObjectURL(resp);
      src.value = objectURL;
    })
  }
  else if (mode.value == "LOCAL") {
    let split = selectedImageName.value.split("/")
    let imagename = split[split.length - 1].split(".")[0]
    src.value = `data/images/explainability/${imagename}_${layer}_${neuron}.jpg`
    explainability_loading.value = false
  }
})

const resizedrag = ref(false)
const currentx = ref(null)
const model_loading = ref(true)
const explainability_loading = ref(true)

const crit_nodes = ref(0)
const totalnodes = ref(0)
const src = ref('')

onBeforeMount(() => {
  console.log(selectedimagematrix.value)
})

onMounted(() => {
  const resizer = document.getElementById('result-resizer')
  const resultarea = document.getElementById('result-area')
  const resultcontainer = document.getElementById('result-container')
  resultcontainer.style.width = `${resultarea.clientWidth - resizer.clientWidth}px`
  resultcontainer.style.height = `${resultarea.height}px`
  const results = document.getElementById('toparea')
  resizer.addEventListener('mousedown', (event) => {
    resizedrag.value = true
    currentx.value = event.clientX
  })
  results.addEventListener('mousemove', (event) => {
    if (resizedrag.value) {
      const chartelem = document.getElementById('chart-area')
      let width = currentx.value - event.clientX
      chartelem.style.width = `${chartelem.clientWidth - width}px`
      currentx.value = event.clientX
      const resizer = document.getElementById('result-resizer')
      const resultarea = document.getElementById('result-area')
      const resultcontainer = document.getElementById('result-container')
      resultcontainer.style.width = `${resultarea.clientWidth + width - resizer.clientWidth}px`
      resultcontainer.style.height = `${resizer.clientHeight}px`
    }
  })
  results.addEventListener('mouseup', () => {
    resizedrag.value = false
  })
  results.addEventListener('mouseleave', () => {
    resizedrag.value = false
  })
})

</script>

<template>
  <div id="toparea">
    <div id="chart-area">
      <graph-component :ready="!model_loading"></graph-component>
    </div>
    <div id="result-area" class="flexible-area">
      <div id="result-resizer" class="resizer">
        <font-awesome-icon :icon="faArrowRightArrowLeft" />
      </div>
      <div id="result-container">
        <div id="menu-area">
          <button :disabled="background" @click="background = true">Show Background</button>
          <button :disabled="!background" @click="background = false">Hide Background</button>
        </div>
        <div id="g-info">
          <h3>GENERAL INFO</h3>
          <div class="row" style="height: 90px;">
            <h4>Image:</h4>
            <img :src="selectedImageName" style="width: 65px; height: 65px; padding-inline: 5px;" />
          </div>
          <div class="row">
            <h5>Critical Nodes:</h5>
            <label>{{ crit_nodes }}</label>
            <h5>Node Number:</h5>
            <label>{{ totalnodes }}</label>
          </div>
        </div>
        <div id="explainify">
          <h3>EXPLAINABILITY</h3>

          <div style="display: flex; justify-content: center; overflow: hidden; width: 100%; height: 90%">
            <div v-show="explainability_loading && selectedNeuron != ''" id="warning">
              <font-awesome-icon style="margin-inline: 4px;" :icon="faExclamationTriangle" />
              <p> Image for neuron {{ selectedNeuron }} is not ready yet. </p>
            </div>
            <img class="resultim" id="br_img" :src="src" alt="Back Raw" @error="(event) => {
              event.onerror = null
              event.target.src = '/placeholder/placeholder-image.webp'
            }
            " />
          </div>
        </div>
      </div>
    </div>
  </div>
  <div id="nav-area">
    <div id="nav-info" class="nav-component">
      <legend-component></legend-component>
    </div>
    <div id="minimap" class="nav-component">
      <minimap-component></minimap-component>
    </div>
    <div id="block-nav" class="nav-component">
      <block-selector-component></block-selector-component>
    </div>
  </div>
  <overlay-component v-show="model_loading"></overlay-component>
</template>

<style scoped>
#backbtn {
  border: none;
  background-image: radial-gradient(var(--color-accent) 15%, transparent 100%);
  ;
  position: fixed;
  margin-left: 1%;
  margin-top: 1%;
  width: 48px;
  height: 48px;
  border-radius: 50%;
}

#toparea {
  width: 100%;
  height: 70%;
  flex-wrap: nowrap;
}

#nav-area {
  width: 100%;
  height: 30%;
  background-color: var(--color-background-soft);
}

#chart-area {
  min-width: 60%;
  max-width: 99%;
}

#result-area {
  max-width: 40%;
  background-color: var(--color-background-soft);
}

#result-container {
  flex-direction: column;
}

#menu-area {
  width: 100%;
  height: 5%;
}

#g-info {
  height: 25%;
  flex-direction: column;
}

#explainify {
  height: 70%;
  overflow: hidden;
}

#warning {
  background-color: var(--color-warning);
  display: flex;
  width: 100%;
  height: fit-content;
  align-items: center;
  justify-content: center;
  text-overflow: ellipsis;
  text-wrap: stable;
  flex-wrap: nowrap;
}

#imoverlay {
  width: 100%;
  height: auto;
}

.resultim {
  display: block;
  width: auto;
  max-height: 98%;
  object-fit: contain;
}

.flexible-area {
  flex: 1 1 auto;
  flex-wrap: nowrap;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: clip;
}

.nav-component {
  display: inherit;
  flex: 1 1 0;
  width: 30%;
  border: 1px solid var(--color-border);
  ;
  background-color: var(--color-background-soft);
}

.row {
  height: 35px;
  padding: 1%;
}

font-awesome-icon {
  pointer-events: none;
}

div {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  overflow-y: auto;
  overflow-x: hidden;
}

figure {
  display: flex;
  flex-direction: column;
  flex-shrink: 1;
  min-width: 48%;
  height: 40%;
  border: solid 1px var(--color-border);
  margin: 5px;
}

figcaption {
  display: flex;
  text-align: center;
  justify-content: center;
  font-style: italic;
  font-weight: bold;
  font-size: 18px;
}

button {
  width: 50%;
  background-color: rgb(212, 207, 207);
  border: 1px solid var(--color-border);
  cursor: pointer;
}

button:disabled {
  background-color: aqua;
  color: black;
  cursor: default
}

label {
  margin-inline-start: 2%;
  height: fit-content;
  font-style: italic;
  font-size: larger;
}
</style>
