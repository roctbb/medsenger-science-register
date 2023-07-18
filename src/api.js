import ApiClient from "@/api/backend";

const api = new ApiClient(process.env.VUE_APP_MAINHOST)

export default api