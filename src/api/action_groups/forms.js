async getAll() {
    let result;

    try {
        result = await this.client.get('/get_data');
    } catch (e) {
        console.log(e)
        throw new Error("Ошибка соединения с сервером.")
    }

    let expectedErrors = []

    api_utils.checkForErrors(result, expectedErrors)

    return result.data
}