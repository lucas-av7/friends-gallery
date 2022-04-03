import mitt from "mitt";

let emitter = mitt();

export default function (app) {
  app.config.globalProperties.$emitter = emitter;
}
