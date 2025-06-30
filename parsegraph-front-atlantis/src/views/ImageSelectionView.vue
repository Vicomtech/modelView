<script setup>
import { onMounted, ref, computed } from "vue";
import { debounce } from "../modules/utils";
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faAngleDoubleLeft, faAngleDoubleRight } from '@fortawesome/free-solid-svg-icons'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useManagerStore } from '@/stores/manager'

import OverlayComponent from '@/components/OverlayComponent.vue'

const managerstore = useManagerStore()
const { selectedImageName, selectedimagematrix, apiservice, mode, modelfile } = storeToRefs(managerstore)

const router = useRouter()
const msg = ref("")

const imagelist = ref([]);
const numimages = ref(5);
const currentpage = ref(1);

const imagefileuploader = ref(null)
const selectedfile = ref(null)
const model_loading = ref(false)

const selectedcrop = ref("")

const totalpages = computed(() => {
  return Math.ceil(imagelist.value.length / numimages.value);
});


const selected = computed(() => {
  return selectedfile.value == null ? null : URL.createObjectURL(selectedfile.value)
})

const offset = computed(() => {
  return (currentpage.value - 1) * numimages.value;
});

const numelements = computed(() => {
  return Math.min(numimages.value, imagelist.value.length - offset.value);
});

const selectiondebounce = debounce(() => {
  markSelection();
}, 300);

onMounted(() => {
  fetch("envconfig.json").then((response) => response.json()).then((value) => {
    mode.value = value["Mode"]["value"]
    if (mode.value == "REMOTE")
      msg.value = ""
    else if (mode.value == "LOCAL") {
      msg.value = ""
      modelfile.value = value["localconf"]["modelfile"]
      for (var image of value["localconf"]["original"])
        imagelist.value.push(`/data/images/original/${image}`)
    }
    else {
      msg.value = "Unsuported mode requested: please set it to LOCAL or REMOTE"
    }
    document.getElementById("Unsuported").innerHTML = `<p>${msg.value}</p>`
  })

  imagefileuploader.value = document.getElementById("fileuploader")
  imagefileuploader.value.addEventListener("change", getImage)
});

function getImage() {
  selectedfile.value = imagefileuploader.value.files.length > 0 ? imagefileuploader.value.files[0] : null
}

function selectImage(index) {
  selectedcrop.value = imagelist.value[index];
  selectedImageName.value = selectedcrop.value
  selectedimagematrix.value = index + 1
  console.log(selectedimagematrix.value)
  markSelection();
}

function markSelection() {
  let imgs = document.getElementsByClassName("catalogimages");
  console.log(imgs)
  for (let i = 0; i < imgs.length; i++) {
    console.log(imgs[i].id, selectedimagematrix.value)
    imgs[i].className =
      selectedimagematrix.value.toString() == imgs[i].id
        ? "catalogimages selectedimage"
        : "catalogimages";
  }
}

async function cropfaces() {

  model_loading.value = true
  var success = async function (content) {
    try {
      var base64 = content.split(",")[1]
      let deliver = JSON.stringify({ "file": base64 })
      let ans = await apiservice.value.execute("getcrops", { "Content-Type": "application/json" }, {}, deliver, "json")
      imagelist.value = []
      for (let elem of Object.values(ans)) {
        let imstr = `data:image/png;base64,${String(elem)}`
        imagelist.value.push(imstr)
      }
    } catch (err) {
      console.log(err)
    }
    finally {
      model_loading.value = false
    }
  }

  var fileReader = new FileReader();
  fileReader.onload = function (evt) { success(evt.target.result) };
  fileReader.readAsDataURL(selectedfile.value);
}

function clickImageSelector() {
  imagefileuploader.value.click()
}

function tomodel() {
  router.replace('/mv')
}

</script>
<template>
  <div v-show="mode == 'REMOTE' || mode == 'LOCAL'" id="selectionpage">
    <div id="preview">
      <div id="file_selector">
        <input id="fileuploader" type="file" accept=".jpg, .jpeg, .png"
          style="opacity: 0; position: fixed; width: 0.1; height: 0.1;" />
        <button id="upload_btn" class="nextpagebtn" @click="clickImageSelector" :disabled="mode == 'LOCAL'"
          style="transform: translate(0%, 0%); fill:white">
          <svg height=" 32px" width="32px" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
            viewBox="0 0 490.955 490.955">
            <g>
              <path
                d="M445.767,308.42l-53.374-76.49v-20.656v-11.366V97.241c0-6.669-2.604-12.94-7.318-17.645L312.787,7.301 C308.073,2.588,301.796,0,295.149,0H77.597C54.161,0,35.103,19.066,35.103,42.494V425.68c0,23.427,19.059,42.494,42.494,42.494 h159.307h39.714c1.902,2.54,3.915,5,6.232,7.205c10.033,9.593,23.547,15.576,38.501,15.576c26.935,0-1.247,0,34.363,0 c14.936,0,28.483-5.982,38.517-15.576c11.693-11.159,17.348-25.825,17.348-40.29v-40.06c16.216-3.418,30.114-13.866,37.91-28.811 C459.151,347.704,457.731,325.554,445.767,308.42z M170.095,414.872H87.422V53.302h175.681v46.752 c0,16.655,13.547,30.209,30.209,30.209h46.76v66.377h-0.255v0.039c-17.685-0.415-35.529,7.285-46.934,23.46l-61.586,88.28 c-11.965,17.134-13.387,39.284-3.722,57.799c7.795,14.945,21.692,25.393,37.91,28.811v19.842h-10.29H170.095z M410.316,345.771 c-2.03,3.866-5.99,6.271-10.337,6.271h-0.016h-32.575v83.048c0,6.437-5.239,11.662-11.659,11.662h-0.017H321.35h-0.017 c-6.423,0-11.662-5.225-11.662-11.662v-83.048h-32.574h-0.016c-4.346,0-8.308-2.405-10.336-6.271 c-2.012-3.866-1.725-8.49,0.783-12.07l61.424-88.064c2.189-3.123,5.769-4.984,9.57-4.984h0.017c3.802,0,7.38,1.861,9.568,4.984 l61.427,88.064C412.04,337.28,412.328,341.905,410.316,345.771z">
              </path>
            </g>
          </svg>
          <span>Load Image</span>
        </button>
      </div>
      <figure>
        <img :src="selected != null ? selected : 'placeholder/placeholder-image.webp'"
          style="width: auto; height: 45vh; border: 1px black solid" />
        <figcaption>{{ mode == 'LOCAL' ? 'Image selection unabailable' : selectedfile == null
          ? "No image has been selected" : selectedfile.name }}</figcaption>
      </figure>
      <button class="nextpagebtn" :disabled="selected == null" @click="cropfaces">
        Crop Faces
      </button>
    </div>
    <div id="catalog">
      <h3>Found Faces</h3>
      <div id="catalogprev">
        <img v-for="index in numelements" class="catalogimages" :id="index" :key="index"
          :src="imagelist[index + offset - 1]" @click="selectImage(index + offset - 1)" />
      </div>
      <div id="controls">
        <button :disabled="currentpage == 1 || totalpages == 0" @click="() => {
          currentpage--;
          selectiondebounce();
        }
        ">
          <font-awesome-icon :icon="faAngleDoubleLeft" />
        </button>
        <label id="pagecount">{{ totalpages > 0 ? currentpage : 0 }} of {{ totalpages }}</label>
        <button :disabled="currentpage >= totalpages || totalpages == 0" @click="() => {
          currentpage++;
          selectiondebounce();
        }
        ">
          <font-awesome-icon :icon="faAngleDoubleRight" />
        </button>
      </div>
      <button class="nextpagebtn" :disabled="selectedcrop == null || selectedcrop == ''"
        style="transform: translate(450%, 0%); height: 30px; margin-top: 5px;" @click="tomodel()">Send to Model</button>
      <overlay-component class="overlay" v-show="model_loading"></overlay-component>
    </div>
  </div>
  <div id="Unsuported" v-show="mode != 'REMOTE' && mode != 'LOCAL'">

  </div>
</template>

<style scoped>
#selectionpage {
  width: 100%;
  height: 100%;
}

#preview {
  width: 100%;
  height: 65%;
  padding: 1%;
}

#file_selector {
  display: flex;
  justify-content: center;
}

#upload_btn {
  width: 20%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

#catalog {
  width: 100%;
  height: 35%;
  background-color: var(--vt-c-white-soft);
}

#catalogprev {
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
  height: 70%;
  width: 100%;
}

#controls {
  display: flex;
  flex-direction: row;
  justify-items: center;
  justify-content: center;
}

#pagecount {
  margin-inline: 1%;
}

.nextpagebtn {
  width: 10%;
  height: 45px;
  transform: translate(450%, -50%);
  background-color: var(--color-accent);
  border-radius: 5%;
  color: var(--vt-c-white);
  cursor: pointer;
}

.nextpagebtn:disabled {
  background-color: var(--color-disabled);
  color: var(--color-disabled-text);
  cursor: not-allowed;
}

.catalogimages {
  width: auto;
  height: 40%;
  border: 1px black solid;
  cursor: pointer;
}

.selectedimage {
  border: 2px solid;
  border-color: var(--color-accent);
}

figure {
  padding: 4px;
  margin-block: 1%;
  margin-inline: auto;
  width: fit-content;
}

figcaption {
  font-style: italic;
  padding: 2px;
  text-align: center;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
}
</style>
