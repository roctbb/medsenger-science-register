let empty = function (obj) {
    return !obj || Object.keys(obj).length === 0
}

const hasTimePart = (d) => {
    return (d.getHours() !== 0 || d.getMinutes() !== 0);
}

const external_url = (path) => {
    return process.env.VUE_APP_MAINHOST + path
}

const formatDate = (d) => {
    return d.getDate() + "." + ('0' + (d.getMonth() + 1)).slice(-2) + "." + d.getFullYear()
}

const formatDateTime = (d) => {
    if (hasTimePart(d)) {
        return d.getDate() + "." + ('0' + (d.getMonth() + 1)).slice(-2) + "." + d.getFullYear() + " " + d.getHours() + ":" + ('0' + d.getMinutes()).slice(-2)
    }
    else {
        return d.getDate() + "." + ('0' + (d.getMonth() + 1)).slice(-2) + "." + d.getFullYear()
    }
}

const copy = function (obj) {
    return JSON.parse(JSON.stringify(obj))
}

const isString = function (value) {
    return typeof value === 'string' || value instanceof String;
}

const searchForArray = function (haystack, needle) {
    var i, j, current;
    for (i = 0; i < haystack.length; ++i) {
        if (needle.length === haystack[i].length) {
            current = haystack[i];
            for (j = 0; j < needle.length && needle[j] === current[j]; ++j) ;
            if (j === needle.length)
                return true;
        }
    }
    return false;
}

function getCookie(name) {
    var matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)" // eslint-disable-line
    ))
    return matches ? decodeURIComponent(matches[1]) : undefined
}

function setCookie(name, value, props) {
    props = props || {}
    let exp = props.expires

    if (typeof exp == "number" && exp) {
        let d = new Date()
        d.setTime(d.getTime() + exp * 1000)
        exp = props.expires = d
    }

    if (exp && exp.toUTCString) {
        props.expires = exp.toUTCString()
    }

    value = encodeURIComponent(value)

    let updatedCookie = name + "=" + value

    for (let propName in props) {
        updatedCookie += "; " + propName
        let propValue = props[propName]

        if (propValue !== true) {
            updatedCookie += "=" + propValue
        }
    }

    document.cookie = updatedCookie
}

function deleteCookie(name) {
    setCookie(name, null, {expires: -1})
}

function toBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onloadend = () => resolve(reader.result.split(';base64,')[1]);
        reader.onerror = error => reject(error);
    })
}

function fillPatientData(text, patient) {
    if (isString(text)) {
        text = text.replace('<PATIENT_NAME>', patient.name)
    }
    return text
}

const api_url = (action) => external_url('/api/client') + action

export {
    searchForArray,
    empty,
    external_url,
    api_url,
    formatDate,
    formatDateTime,
    copy,
    getCookie,
    deleteCookie,
    toBase64, isString, fillPatientData
}