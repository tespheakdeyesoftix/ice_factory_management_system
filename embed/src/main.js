import { createApp, reactive } from "vue";
import PrimeVue from 'primevue/config';
import Aura from '@primeuix/themes/aura';
import App from "./App.vue";
 

import router from "./router";
import resourceManager from "../../../doppio/libs/resourceManager";
import call from "../../../doppio/libs/controllers/call";
import socket from "../../../doppio/libs/controllers/socket";
import Auth from "../../../doppio/libs/controllers/auth";

import "@/helper/global-function.js"

const app = createApp(App);
app.use(PrimeVue, {
    theme: {
        preset: Aura
    }
});
const auth = reactive(new Auth());

app.use(PrimeVue); // no theme config needed here
app.use(router);
app.use(resourceManager);

app.provide("$auth", auth);
app.provide("$call", call);
app.provide("$socket", socket);

router.beforeEach(async (to, from, next) => {
    if (to.matched.some((record) => !record.meta.isLoginPage)) {
        if (!auth.isLoggedIn) {
            next({ name: 'Login', query: { route: to.path } });
        } else {
            next();
        }
    } else {
        if (auth.isLoggedIn) {
            next({ name: 'Home' });
        } else {
            next();
        }
    }
});

app.mount("#app");
