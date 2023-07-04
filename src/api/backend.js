import HttpClient from "@/utils/http_client";
import AccountActions from "@/api/action_groups/account";

class ApiClient {
    constructor(host, token, role) {
        let client = new HttpClient(host + '/api')

        this.account = new AccountActions(client, token, role)

        this.__actionGroups = [this.account]
    }

    setRole(role) {
        this.__actionGroups.forEach((group) => {
            group.setRole(role)
        })
    }

    setToken(token) {
        this.__actionGroups.forEach((group) => {
            group.setToken(token)
        })
    }
}

export default ApiClient
