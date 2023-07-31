import Manager from "@/managers/common";
import User from "@/models/User";
import {deleteCookie, getCookie} from "@/utils/helpers";

class StateManager extends Manager {

    constructor(state, bus, api) {
        super(state, bus, api);

        this._state = state
        this.loaded = false;
    }

    async load() {
        if (getCookie("register_token")) {
            let token = getCookie("register_token")
            deleteCookie("register_token")
            localStorage.setItem('register_token', token)
        }

        this._state.api_token = localStorage.getItem('register_token')

        console.log("Token:", this._state.api_token)

        if (this._state.api_token) {
            try {
                this.api.setToken(this._state.api_token)
                this._state.user = new User(await this.api.account.get())
            } catch (e) {
                console.log("Token is not valid")
                console.log(e)
            }
        }

        console.log("Loaded")
        this.loaded = true
    }

    save() {
        localStorage.setItem('register_token', this._state.api_token)
    }

    clear() {
        this._state.user = undefined
        localStorage.clear()
    }

    get user() {
        return this._state.user
    }

    set user(user) {
        console.log("setting user to ", user)

        if (user.api_token) {
            this._state.api_token = user.api_token
            this.api.setToken(this._state.api_token)
            this.save()
        }

        this._state.user = user
    }
}

export default StateManager