import api_utils from "../api_utils";

class SubmissionActions extends api_utils.ActionGroup {
    async all(project_id, patient_id) {

        let query = {
            api_token: this.token,
        }

        let result;

        try {
            result = await this.client.get('/project/' + project_id + '/patients/' + patient_id + '/submissions', query);
        } catch (e) {
            console.log(e)
            throw new Error("Ошибка соединения с сервером.")
        }

        let expectedErrors = []

        api_utils.checkForErrors(result, expectedErrors)

        return result.data

    }

    async submit(project_id, patient_id, form_id, answers) {

        let query = {
            api_token: this.token,
        }

        let data = {
            form_id: form_id,
            answers: answers
        }

        let result;

        try {
            result = await this.client.postJson('/project/' + project_id + '/patients/' + patient_id + '/submissions', query, data);
        } catch (e) {
            console.log(e)
            throw new Error("Ошибка соединения с сервером.")
        }

        let expectedErrors = [
            ['InsufficientData', 'Заполните все обязательные поля']
        ]

        api_utils.checkForErrors(result, expectedErrors)

        return result.data

    }

    async update(project_id, patient_id, form_id, submission_id, answers) {

        let query = {
            api_token: this.token,
        }

        let data = {
            form_id: form_id,
            answers: answers
        }

        let result;

        try {
            result = await this.client.postJson('/project/' + project_id + '/patients/' + patient_id + '/submissions/' + submission_id, query, data, 'put');
        } catch (e) {
            console.log(e)
            throw new Error("Ошибка соединения с сервером.")
        }

        let expectedErrors = [
            ['InsufficientData', 'Заполните все обязательные поля']
        ]

        api_utils.checkForErrors(result, expectedErrors)

        return result.data

    }
}

export default SubmissionActions