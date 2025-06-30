export default class APIService {
  requestdict={}

  constructor() {
    fetch("envconfig.json").then((response) => response.json()).then((value) => { 
      this.requestdict = value["endpoints"]
    })
  }
  /**
   * 
   * @param {String} request request key
   * @param {{String:String}} headers Additional headers for the request
   * @param {{String:String}} args Args for the request if needed
   * @param {any} body The body of the request if needed
   * @param {"file"|"json" } returnType Return type of the function. if file it would return a blob. JSON otherwise
   */
  async execute(request, headers={},args={},body=null, returnType="json") {
    try {
      if (Object.keys(this.requestdict).includes(request)) {
        let hds = {'Access-Control-Expose-Headers': 'Content-Disposition', ...headers}
        let url ="" + this.requestdict[request]["url"]
        const meth = this.requestdict[request]["method"]
        if (Object.keys(args).length > 0) {
          let keys = Object.keys(args)
          url += `?${keys[0]}=${args[keys[0]]}`
          keys.shift()
          for (let k of keys) {
            url += `&${k}=${args[k]}`
          }
        }
        let response = null
        if (body) {
          response = await fetch(url,
            {
              method: meth,
              headers: hds,
              body: body,
            }
          );
        } else {
          response = await fetch(url,
            {
              method: meth,
              headers: hds
            }
          );
        }
        if (!response.ok) {
          throw new Error(`${response.status}: ${response.statusText}`);
        }
        if (returnType == "json") {
          const jsn = await response.json()
          return jsn
        } else {
          const fl =  await response.blob()
          return fl;
        }
      }
      else {
        throw new Error(`Unable to perform ${request}. Unknown request`);
      }
    } catch (error) {
      throw new Error(`ERROR: ${error}`);
    }
  }
}