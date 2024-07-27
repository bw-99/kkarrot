import axios from 'axios';

const gen_headers = (token) => {
    return {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    }
}

export const fetchHomeFeed = () => {
    let user_id = sessionStorage.getItem("user_id");
    return axios.get('/view/home/1/p/1', {
        headers: gen_headers(user_id)
    })
}

export const fetchProductFeed = (item_id) => {
    let user_id = sessionStorage.getItem("user_id");
    return axios.get('/view/product/'+item_id, {
        headers: gen_headers(user_id)
    })
}

export const putSession2Server = () => {
    let user_id = sessionStorage.getItem("user_id");
    return axios.post('/login', {
        user_id: eval(user_id)
    });
}