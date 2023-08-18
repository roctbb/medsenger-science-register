import {empty} from "./helpers"

class HttpClient {
    constructor(endpoint) {
        this.endpoint = endpoint
    }

    async makeRequest(action, method, body, headers) {
        console.log("Sending request ", method, " to ", this.endpoint + action, " with params ", body)

        let requestOptions = {
            method: method,
            body: body
        }

        if (headers) {
            requestOptions.headers = headers
        }

        try {
            let result = await fetch(this.endpoint + action, requestOptions)

            console.log("Request done, status:", result.status)

            try {
                return await result.json()
            } catch (e) {
                return await result.text()
            }
        } catch (e) {
            console.log("Request failed!")
            throw e
        }
    }

    async post(action, get_params, post_params) {
        if (!empty(get_params)) {
            action = action + '?' + new URLSearchParams(get_params).toString()
        }

        let data = new FormData()
        Object.keys(post_params).forEach((key) => {
            data.append(key, post_params[key])
        })

        return await this.makeRequest(action, 'POST', data)
    }

    async postJson(action, get_params, data, method) {
        if (empty(method)) {
            method = 'POST'
        }

        if (!empty(get_params)) {
            action = action + '?' + new URLSearchParams(get_params).toString()
        }

        let body = JSON.stringify(data)

        return await this.makeRequest(action, method, body, {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },)
    }

    async get(action, get_params) {
        if (!empty(get_params)) {
            action = action + '?' + new URLSearchParams(get_params).toString()
        }

        return await this.makeRequest(action, 'GET')
    }

    async delete(action, delete_params) {
        if (!empty(delete_params)) {
            action = action + '?' + new URLSearchParams(delete_params).toString()
        }

        return await this.makeRequest(action, 'DELETE')
    }
}

export default HttpClient