import resources from "@/resources"


const applicationPlugin = {
    install(app) {
        app.config.globalProperties.state = resources.state
        app.config.globalProperties.event_bus = resources.event_bus
        app.config.globalProperties.managers = resources.managers
    }
}

export default applicationPlugin;