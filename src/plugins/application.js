import ApiClient from "@/api/backend";
import mitt from "mitt";
import StateManager from "@/managers/state";
import State from "@/models/state";
import AuthManager from "@/managers/auth";
import UserManager from "@/managers/user";
import {reactive} from "vue";
import ProjectManager from "@/managers/project";


const applicationPlugin = {
    install(app) {
        let stateModel = reactive(new State())
        let event_bus = mitt()
        let api = new ApiClient(process.env.VUE_APP_MAINHOST)
        let state = new StateManager(stateModel, event_bus, api)

        console.log(process.env.VUE_APP_MAINHOST)

        app.config.globalProperties.state = state
        app.config.globalProperties.event_bus = event_bus

        app.config.globalProperties.managers = {
            auth: new AuthManager(state, event_bus, api),
            user: new UserManager(state, event_bus, api),
            project: new ProjectManager(state, event_bus, api)
        }
    }
}

export default applicationPlugin;