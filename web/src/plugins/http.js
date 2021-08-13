import axios from 'axios'

const no_auth = axios.create({
    baseURL: 'http://localhost:8000/api',
});

const with_auth = axios.create({
    baseURL: 'http://localhost:8000/api',
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: 'X-CSRFToken',
    withCredentials: true
})

no_auth.get('/auth')

function getAll() {
    return no_auth.get('/nodes')
}

function createNewIssue(postData) {
    return with_auth.post('/nodes/', postData)
}

export default {
    getAll,
    createNewIssue
};