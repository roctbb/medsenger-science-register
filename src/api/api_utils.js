class DetailedError extends Error {
    constructor(message, details) {
        super(message)
        try {
            this.details = JSON.parse(details)
        }
        catch (e) {
            this.details = details
        }
    }
}

function checkForErrors(response, errors) {
    if (response.state === 'error') {
        errors.forEach((error) => {
            if (response.error === error[0]) {

                if (response.details) {
                    throw new DetailedError(error[1], response.details)
                }
                else {
                    throw new Error(error[1])
                }
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