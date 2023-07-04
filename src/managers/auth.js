import Manager from "@/managers/common";

class AuthManager extends Manager {
    async makeLogin(login, password) {
        this.state.user = await this.api.account.login(login, password)
        this.eventbus.emit('change-screen', 'projects')
    }

    logout() {
        this.state.clear()
        this.eventbus.emit('change-screen', 'login')
    }

}

export default AuthManager