import axios from 'axios'

const no_auth = axios.create({
    baseURL: 'http://localhost:8000/api',
    headers: {
        post: {
            "Content-Type": "application/json"
        }
    }
});

const with_auth = axios.create({
    baseURL: 'http://localhost:8000/api',
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: 'X-CSRFToken',
    withCredentials: true,
    headers: {
        post: {
            "Content-Type": "application/json"
        }
    },
})

no_auth.get('/auth')

function getAll() {
    return no_auth.get('/nodes')
}

function createNewIssue(postData) {
    return with_auth.post('/nodes/', postData)
}

function updateIssue(issueId, postData) {
    return with_auth.post(`/nodes/${issueId}`, postData)
}

function deleteIssue(issueId) {
    return with_auth.delete(`/nodes/${issueId}`)
}

export default {
    getAll,
    createNewIssue,
    updateIssue,
    deleteIssue,
};