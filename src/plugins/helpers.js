import {external_url, formatDate} from "@/utils/helpers";

const helpersPlugin = {
    install(app) {
        app.config.globalProperties.external_url = external_url
        app.config.globalProperties.formatDate = formatDate
        app.config.globalProperties.external_url = external_url
    }
}

export default helpersPlugin;