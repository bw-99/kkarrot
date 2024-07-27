import React, { useState,useEffect } from 'react';
import { useNavigate } from "react-router-dom";
import { Link } from 'react-router-dom';
import './ExplorePage.css';
import {fetchExploreFeed} from '../api';

const ExplorePage = () => {
  const  [bookList, setBookList] = useState([]);

    // * 비로그인 방지
    useEffect(() => {
      let user_id = sessionStorage.getItem("user_id");
      if(!user_id){
        navigate("/login");  
        return
      }
      setIsLogin(true);
    }, []);

  useEffect(() => {
    fetchBookList();
    let user_id = sessionStorage.getItem("user_id");
    if(!user_id){
      setIsLogin(false);
      return
    }
    user_id = JSON.parse(user_id);

    if(((user_id >= 0) && (user_id <= 1999))) {
      setIsLogin(true);
    }
    else{
      setIsLogin(false);
    }
  }, []);
  
  const fetchBookList = () => {
    fetchExploreFeed()
      .then((data) => {
        setBookList(data["feed_lst"]);
      })
      .catch((error) => {
        console.log("Error while fetching books:", error);
      });
  }

  const [viewMore, setViewMore] = useState('');
  const navigate = useNavigate();
  const [isLogin, setIsLogin] = useState(false);


  
  useEffect(() => {
    if(!viewMore) {
      return
    }

    alert("load more");
    setViewMore(false);
    return
  }, [viewMore])
  
  return (
    isLogin &&
    <div className="ExplorePage">
      <header className="navbar">
        <Link to={`/`}  className='logo'>KKARROT</Link>
      </header>
      <div>

        <section className="popular-products" style={{display:"flex", alignItems:'center', flexDirection:"column"}}>
        <div style={{fontWeight:600, fontSize: "35px", marginTop:"40px", marginBottom:"50px"}}>중고거래 인기매물</div>
        <div className="product-list">
             {bookList.map(product => (
                <Link to={`/product/${product.item_id}`} key={product.item_id} className="product-item">
                  <img src={product.images["hi_res"][0]} alt={product.title} style={{display:"block",  width:"223px", height:"223px", objectFit:"cover"}}/>
                  <div className="product-info" style={{display:"flex", alignItems:"flex-start", flexDirection:"column"}}>
                    <div style={{overflow:"hidden", whiteSpace:"nowrap", textOverflow:"ellipsis"}}>
                      {product.title}
                    </div>
                    <div style={{fontWeight:"bold", marginTop:"8px"}}>{product.price ? product.price + "$" : ""}</div>
                    <div style={{marginTop:"8px"}}>Num ratings: {product.rating_number}</div>
                  </div>
                </Link>
              ))}
          </div>

          <div className="load-more">
              <button onClick={()=>{
                setViewMore(true);
              }}>더보기</button>
            </div>

        </section>

      </div>
      <footer>
        <p>&copy; 2024 KKARROT</p>
      </footer>
    </div>
  );
};

export default ExplorePage;
