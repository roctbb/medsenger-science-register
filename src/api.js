import ApiClient from "@/api/backend";
import event_bus from "@/event_bus";

const api = new ApiClient(process.env.VUE_APP_MAINHOST, event_bus)

export default api