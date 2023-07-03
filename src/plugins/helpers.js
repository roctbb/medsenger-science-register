import {external_url} from "@/utils/helpers";

const helpersPlugin = {
    install(app) {
        app.config.globalProperties.external_url = external_url
    }
}

export default helpersPlugin;