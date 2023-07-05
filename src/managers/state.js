import Manager from "@/managers/common";
import User from "@/models/user";

class StateManager extends Manager {

    constructor(state, bus, api) {
        super(state, bus, api);
        this.load().then(() => {
            console.log("State is loaded")
            this.eventbus.emit('state-load-done')
        })
    }

    get user() {
        return this.state.user
    }

    set user(user_description) {
        if (user_description.api_token && user_description.api_token !== this.state.token) {
            this.state.token = user_description.api_token
            this.api.setToken(this.state.token)
            this.save()
        } else {
            user_description.api_token = this.state.token
        }

        this.state.user = new User(user_description)
    }

    async load() {
        this.state.token = localStorage.getItem('register_token')

        console.log("Token:", this.state.token)

        if (this.state.token) {
            try {
                this.api.setToken(this.state.token)
                this.user = await this.api.account.get()
                this.eventbus.emit('change-screen', 'projects')
            } catch (e) {
                console.log(e)
                this.eventbus.emit('change-screen', 'login')
            }
        }
    }

    save() {
        localStorage.setItem('register_token', this.state.token)
    }

    clear() {
        localStorage.clear()
    }
}

export default StateManager