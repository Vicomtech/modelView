import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useNetworkStructureStore = defineStore('networkStructure', () => {
  const network = ref(new Object())

  const numberLayers = computed(() => {
    let maxlayernumber = 0
    for (let value of Object.values(network.value)) {
      maxlayernumber = Math.max(Object.keys(value).length, maxlayernumber)
    }
    return maxlayernumber
  })

  const numberblocks = computed(() => {
    return Object.keys(network.value).length
  })

  const layersOfBlock = computed(() => (blockname) => {
    return blockname != undefined ? Object.keys(network.value[blockname]) : []
  })

  const numberLayersinblock = computed(() => (blockname) => {
    return blockname != undefined ? Object.keys(network.value[blockname]).length : 0
  })

  const layerText = computed(() => (layer, block) => {
    return `${layer}: ${network.value[block][layer]["type"]} (${network.value[block][layer]['n_nodes']})`
  })

  return {
    network,
    numberLayers,
    numberblocks,
    layersOfBlock,
    numberLayersinblock,
    layerText
  }
})
