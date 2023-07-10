import api_utils from "../api_utils";

class MedsengerActions extends api_utils.ActionGroup {
    async loadScenarios() {

        let query = {
            api_token: this.token,
        }

        let result;

        try {
            result = await this.client.get('/medsenger/scenarios', query);
        } catch (e) {
            console.log(e)
            throw new Error("Ошибка соединения с сервером.")
        }

        let expectedErrors = []

        api_utils.checkForErrors(result, expectedErrors)

        return result.data
    }
}

export default MedsengerActions