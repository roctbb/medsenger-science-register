import HttpClient from "@/helpers/http_client";
import AccountActions from "@/utils/medsenger_api/action_groups/account";

class MedsengerApiClient {
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

export default MedsengerApiClient
