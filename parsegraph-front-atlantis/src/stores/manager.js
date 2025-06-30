import { ref, computed } from 'vue'
import { defineStore, storeToRefs } from 'pinia'
import { useNetworkStructureStore } from './networkStructure'
import APIService from '@/modules/APIservice'

export const useManagerStore = defineStore('manager', () => {
  const netstore = useNetworkStructureStore()
  const { layersOfBlock, network } = storeToRefs(netstore)

  const background = ref(true);
  const mode = ref("")
  const modelfile = ref("")

  const selectedImageName = ref('')
  const selectedimagematrix = ref(-1)

  const currentBlock = ref()
  const currentNodes = ref([])
  const nodedict = ref({})
  const visibleLayers = ref([])
  const selectedNeuron = ref("")
  const layerdict = ref({})
  const interpretabilitydict = ref({})

  const currentscale = ref(1)
  const translation = ref([0.0, 0.0]);
  const size = ref(15)
  const canvaswidth = ref(0)
  const canvasheight = ref(0)

  const apiservice = ref(new APIService())


  const isNodeVisible = computed(() => (nodename) => {
    let visible = false
    let aux = nodename ? nodename.split("_") : null
    let node = aux ? aux[0] + "_" + aux[1] : null
    for (let layer of visibleLayers.value) {
      let hasname = nodename && node && layerdict.value[node] ? layerdict.value[node].includes(layer):false
      visible = visible || hasname
    }
    return visible
  })

  const isLayerVisible = computed(() => (nodename) => {
    let visible = false
    for (let layer of visibleLayers.value) {
      visible = visible || (nodename && nodename.includes(layer))
    }
    return visible
  })
  const isLayerInCurrentBlock = computed(
    () => (layer) => layersOfBlock.value(currentBlock.value).includes(layer)
  )
  const isCurrentBlock = computed(() => (block) => block == currentBlock.value)
  const isNeuronSelected = computed(() => (neuron) => neuron == selectedNeuron.value)
  
  const imsrc = computed(() => (node_name) => {
    let blockstart = node_name.indexOf("Block")
    let blocknumber = Number(node_name[blockstart + "Block_".length]) - 1
    let layerstart = node_name.indexOf("Layer")
    let layernumber = Number(node_name[layerstart + "Layer_".length])
    let layer = network.value[currentBlock.value][`Layer_${layernumber}`]["n_layer"]
    let split = node_name.split("_")
    let neuronnumber = Number(split[split.length - 1]) - 1
    const resp = `block_${blocknumber}/layer_${layer}_node_${neuronnumber}.jpg`
    return resp
  })

  const maxX = computed(() => {
    if (currentNodes.value.length == 0) {
      return 0
    } else {
      return currentNodes.value.reduce((a,b) => Math.max(a, b.positionX),0)
    }
  })

  const currentzoomlevel = computed(() => {
    return 7 - Math.ceil(currentscale.value * 100 / 15)
  })
  const maxY = computed(() => {
    if (currentNodes.value.length == 0) {
      return 0
    } else {
      return currentNodes.value.reduce((a,b) => Math.max(a, b.positionY),0)
    }
  })
  
  const minX = computed(() => {
    if (currentNodes.value.length == 0) {
      return 0
    } else {
      return currentNodes.value.reduce((a,b) => Math.min(a, b.positionX),0)
    }
  })

  const minY = computed(() => {
    if (currentNodes.value.length == 0) {
      return 0
    } else {
      return currentNodes.value.reduce((a,b) => Math.min(a, b.positionY),0)
    }
  })

  const maxImpact = computed(() => {
    if (currentNodes.value.length == 0) {
      return 0
    } else {
      return currentNodes.value.reduce((a, b) => Math.max(a, b.impact), 0)
    }
  })
  
  const minImpact = computed(() => {
    if (currentNodes.value.length == 0) {
      return 0
    } else {
      return currentNodes.value.reduce((a, b) => Math.min(a, b.impact), 0)
    }
  })

  function loadModelview(imagename, modelname) {
    selectedImageName.value = imagename
    selectedimagematrix.value = modelname
  }

  function selectblock(block) {
    currentBlock.value = block
    visibleLayers.value = layersOfBlock.value(currentBlock.value)
  }

  function revealLayer(layer) {
    visibleLayers.value.push(layer)
    let set = new Set(visibleLayers.value)
    visibleLayers.value = [...set]
  }

  function hideLayer(layer) {
    visibleLayers.value = visibleLayers.value.filter((element) => element != layer)
  }

  function setModel() {
    if (mode.value == "REMOTE") {
      apiservice.value.execute("getModel").then((value) => network.value = value)
    } else {

      fetch(modelfile.value).then((response) => response.json()).then((value) => {
         network.value = value
      })
    }
  }

  return {
    background,
    selectedImageName,
    selectedimagematrix,
    visibleLayers,
    currentBlock,
    selectedNeuron,
    isCurrentBlock,
    currentNodes,
    nodedict,
    layerdict,
    interpretabilitydict,
    isLayerInCurrentBlock,
    isLayerVisible,
    isNeuronSelected,
    isNodeVisible,
    maxX,
    maxY,
    maxImpact,
    minX,
    minY,
    minImpact,
    mode,
    modelfile,
    currentscale,
    currentzoomlevel,
    translation,
    size,
    canvaswidth,
    canvasheight,
    imsrc,
    loadModelview,
    selectblock,
    revealLayer,
    hideLayer,
    setModel,
    apiservice
  }
})
