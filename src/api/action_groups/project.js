import api_utils from "../api_utils";

class ProjectActions extends api_utils.ActionGroup {
    async all() {

        let query = {
            api_token: this.token
        }

        let result;

        try {
            result = await this.client.get('/projects', query);
        } catch (e) {
            console.log(e)
            throw new Error("Ошибка соединения с сервером.")
        }

        let expectedErrors = []

        api_utils.checkForErrors(result, expectedErrors)

        return result.data

    }

    async get(id) {

        let query = {
            api_token: this.token
        }

        let result;

        try {
            result = await this.client.get('/project/' + id, query);
        } catch (e) {
            console.log(e)
            throw new Error("Ошибка соединения с сервером.")
        }

        let expectedErrors = []

        api_utils.checkForErrors(result, expectedErrors)

        return result.data

    }

    async getPatients(project_id) {

        let query = {
            api_token: this.token,
        }

        let result;

        try {
            result = await this.client.get('/project/' + project_id + '/patients', query);
        } catch (e) {
            console.log(e)
            throw new Error("Ошибка соединения с сервером.")
        }

        let expectedErrors = []

        api_utils.checkForErrors(result, expectedErrors)

        return result.data

    }
}

export default ProjectActions