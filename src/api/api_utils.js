function checkForErrors(response, errors) {
    if (response.state === 'error') {
        errors.forEach((error) => {
            if (response.error === error[0]) {
                throw new Error(error[1])
            }
        })

        throw new Error("Не удалось выполнить действие.")
    }
}

class ActionGroup {
    constructor(http_client, token) {
        this.client = http_client
        this.token = token
    }

    setToken(token) {
        this.token = token
    }
}

export default {
    checkForErrors: checkForErrors,
    ActionGroup: ActionGroup
}