import App from "./App.vue";
import router from "./router";
import emitterPlugin from "./emitter.js";
import { createApp } from "vue";
import { library } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import {
  faCamera,
  faUser,
  faXmarkCircle,
  faHeart,
  faTrashCan,
} from "@fortawesome/free-solid-svg-icons";

const app = createApp(App);

app.use(router);
app.use(emitterPlugin);

// Font awesome
app.component("font-awesome-icon", FontAwesomeIcon);
library.add(faCamera, faUser, faXmarkCircle, faHeart, faTrashCan);

app.mount("#app");
