
export async function getcrops(body) {
  const request = new Request("http://10.200.71.31:5050/viz_api/ImageSelection/crop", {
    method: "POST",
    headers: {
        'Access-Control-Expose-Headers': 'Content-Disposition'
    },
    body: body
  });

  try {
    const response = await fetch(request)
    if (!response.ok) {
      throw new Error(`${response.status}: ${response.statusText}`);
    }
    return await response.json();
  }
  catch (error) {
    throw new Error(`Unable to crop faces. ${error}`);
  }
}

export async function testface() {
  const response = await fetch('/data/test/face0data.json')
  return await response.json()
}

export async function getBlockNames() {
  try {
    const response = await fetch(`viz_api/Blocks?model=default`);
    if (!response.ok) {
      throw new Error(`${response.status}: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    throw new Error(`Unable retrieve Block names. ${error}`);
  }
}

export async function getBlockCount() {
  try {
    const response = await fetch(`viz_api/Blocks/count?model=default`);
    if (!response.ok) {
      throw new Error(`${response.status}: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    throw new Error(`Unable retrieve Block count. ${error}`);
  }
}

export  async function getBlockLayers(block) {
  try {
    const response = await fetch(`viz_api/Layers/inblock?block=${block}&model=default`);
    if (!response.ok) {
      throw new Error(`${response.status}: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    throw new Error(`Unable retrieve Layers. ${error}`);
  }
}

export  async function getBlocknodes(block) {
  try {
    const response = await fetch(`viz_api/Nodes?block=${block}&model=default`);
    if (!response.ok) {
      throw new Error(`${response.status}: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    throw new Error(`Unable retrieve Nodes. ${error}`);
  }
}

export async function getInterpretability(imagename) {
  try {
    const response = await fetch(`evapi/interpretability/?image_name=${imagename}`);
    if (!response.ok) {
      throw new Error(`${response.status}: ${response.statusText}`);
    }
    let doc =  await response.json()
    return doc;
  } catch (error) {
    throw new Error(`Unable retrieve Interpretability. ${error}`);
  }
}

export async function getInterpretabilitybyBlock(imagename, blocknumber) {
  try {
    const request = new Request(`evapi/interpretability_by_block/?n_block=${blocknumber}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ face: imagename }),
    })
    const response = await fetch(request);
    if (!response.ok) {
      throw new Error(`${response.status}: ${response.statusText}`);
    }
    let doc =  await response.json()
    return doc;
  } catch (error) {
    throw new Error(`Unable retrieve Interpretability of block ${blocknumber}. ${error}`);
  }
}

export async function getExplainability(imagename, layernumber, neuronnumber) {
  try {
    const response = await fetch(`evapi/explainability/?layer=${layernumber}&channel=${neuronnumber}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ face: imagename }),
    });
    if (!response.ok) {
      throw new Error(`${response.status}: ${response.statusText}`);
    }
    let img =  await response.blob()
    return img;
  } catch (error) {
    throw new Error(`Unable retrieve explainability of layer ${layernumber}, neuron ${neuronnumber}. ${error}`);
  }
}
