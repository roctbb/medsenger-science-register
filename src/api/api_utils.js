function checkForErrors(response, errors) {
    if (response.state == 'failed') {
        errors.forEach((error) => {
            if (response.error.includes(error[0])) {
                throw new Error(error[1])
            }
        })

        throw new Error("Не удалось выполнить действие.")
    }
}

class ActionGroup {
    constructor(http_client, token, role) {
        this.client = http_client
        this.token = token
        this.role = role
    }

    setRole(role) {
        this.role = role
    }

    setToken(token) {
        this.token = token
    }
}

export default {
    checkForErrors: checkForErrors,
    ActionGroup: ActionGroup
}