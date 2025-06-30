export function debounce(callback, wait) {
  let timerId;
  return (...args) => {
    clearTimeout(timerId);
    timerId = setTimeout(() => {
      callback(...args);
    }, wait);
  };
}

export function lerp(start, end, amt) {
  return (1 - amt) * start + amt * end;
}

/**
 * Given an RGB matrix with values between 0-225 return the image it represents
 * @param {Array<Array<Array<Number>>>} matrix - The RGB values of the image given in format channelxwidthxheight and BGR channel order
 * @param {Number} width - The width of the image in number of pixels
 * @param {Number} height - The height of the image in number of pixels
 * @return {string} The image source element
 */
export function matrix2image(matrix, width, height) {
  let buffer = new Uint8ClampedArray(width * height * 4);
  for(var x = 0; x < width; x++) {
    for(var y = 0; y < height; y++) {
      var pos = (y + x * width) * 4; // position in buffer based on x and y
      buffer[pos] = matrix[2][x][y];           // some R value
      buffer[pos+1] = matrix[1][x][y]           // some G value
      buffer[pos + 2] = matrix[0][x][y]           // some B value
      buffer[pos+3] = 255
    }
  }
  // create off-screen canvas element
  var canvas = document.createElement('canvas'),
      ctx = canvas.getContext('2d');

  canvas.width = width;
  canvas.height = height;

  // create imageData object
  var idata = ctx.createImageData(width, height);

  // set our buffer as source
  idata.data.set(buffer);

  // update canvas with new data
  ctx.putImageData(idata, 0, 0); 
  return canvas.toDataURL();
  
}