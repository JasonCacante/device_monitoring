import { createPinia } from 'pinia'; // Import createPinia
import { createApp } from 'vue';
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";
import App from './App.vue';
import router from './router'; // Import the router
import { useAuthStore } from './stores/authStore'; // Import authStore
import './style.css';

const app = createApp(App);
const pinia = createPinia(); // Create a Pinia instance

app.use(pinia); // Use Pinia FIRST (required for stores)
app.use(router); // Use the router
app.use(Toast); // Use vue-toastification

// Restore authentication session from localStorage
const authStore = useAuthStore();
authStore.restoreSession();

app.mount('#app');

