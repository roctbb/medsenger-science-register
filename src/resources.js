import {reactive} from "vue";
import State from "@/models/State";
import StateManager from "@/managers/state";
import AuthManager from "@/managers/auth";
import SubmissionManager from "@/managers/submission";
import event_bus from "@/event_bus";
import api from "@/api"


const stateModel = reactive(new State())
const state = new StateManager(stateModel, event_bus, api)
const managers = {
    auth: new AuthManager(state, event_bus, api),
    submission: new SubmissionManager(state, event_bus, api)
}

console.log("state manager in state.js:", state)

const resources = {
    event_bus: event_bus,
    api: api,
    state: state,
    managers: managers
}

export default resources