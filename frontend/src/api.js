import axios from 'axios';


const gen_headers = (token) => {
    return {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    }
}

export async function fetchHomeFeed() {
    let user_id = sessionStorage.getItem("user_id");
    
    try {
        let result = await axios.get('/view/home/p/0', {
            headers: gen_headers(user_id)
        })
        return {
            "feed_lst": JSON.parse(result.data["feed_lst"]),
        };
    } catch (error) {
        sessionStorage.clear();
    }
}


export async function fetchExploreFeed () {
    let user_id = sessionStorage.getItem("user_id");
    
    try {
        let result = await axios.post('/view/home/p/0', {}, {
            headers: gen_headers(user_id)
        })
        return {
            "feed_lst": JSON.parse(result.data["feed_lst"]),
        };
    } catch (error) {
        
        sessionStorage.removeItem("user_id");
    }
}

export async function fetchProductFeed (item_id) {
    let user_id = sessionStorage.getItem("user_id");
    
    try {
        let result = await axios.get('/view/product/'+item_id, {
            headers: gen_headers(user_id)
        })
        let data = {
            "feed_lst": JSON.parse(result.data["feed_lst"]),
            "item": JSON.parse(result.data["item"])[0],
        }
        return data;
    } catch (error) {
        sessionStorage.clear();
    }
}

export async function putSession2Server () {
    let user_id = sessionStorage.getItem("user_id");
    let result = await axios.post('/login', {
        user_id: eval(user_id)
    }, {
        headers: gen_headers(user_id)
    })
    
    if(result.status != 200) {
        sessionStorage.clear();
        return
    }
    
}