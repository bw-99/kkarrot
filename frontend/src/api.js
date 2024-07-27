import axios from 'axios';


const gen_headers = (token) => {
    return {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    }
}

export async function fetchHomeFeed() {
    let user_id = sessionStorage.getItem("user_id");
    let result = await axios.get('/view/home/1/p/1', {
        headers: gen_headers(user_id)
    })
    
    try {
        return {
            "feed_lst": JSON.parse(result.data["feed_lst"]),
        };
    } catch (error) {
        sessionStorage.clear();
        window.open("/login");
    }
}


export async function fetchExploreFeed () {
    let user_id = sessionStorage.getItem("user_id");
    let result = await axios.post('/view/home/1/p/1', {}, {
        headers: gen_headers(user_id)
    })
    
    try {
        return {
            "feed_lst": JSON.parse(result.data["feed_lst"]),
        };
    } catch (error) {
        sessionStorage.clear();
        window.open("/login");
    }
}

export async function fetchProductFeed (item_id) {
    let user_id = sessionStorage.getItem("user_id");
    let result = await axios.get('/view/product/'+item_id, {
        headers: gen_headers(user_id)
    })
    
    try {
        return {
            "feed_lst": JSON.parse(result.data["feed_lst"]),
            "item": JSON.parse(result.data["item"])[0],
        };
    } catch (error) {
        sessionStorage.clear();
        window.open("/login");
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
        window.open("/login");
        return
    }
    
}