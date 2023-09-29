import Manager from "@/managers/common";
import User from "@/models/User";

class AuthManager extends Manager {
    async makeLogin(login, password) {
        this.state.user = new User(await this.api.account.login(login, password))
    }

    has_auth() {
        return this.state.user !== undefined
    }

    logout() {
        this.state.clear()
    }
}

export default AuthManager