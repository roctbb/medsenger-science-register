let empty = function (obj) {
    return !obj || Object.keys(obj).length === 0
}

const external_url = (path) => {
    return process.env.VUE_APP_MAINHOST + path
}

const api_url = (action) => external_url('/api/client') + action

export {empty, external_url, api_url}