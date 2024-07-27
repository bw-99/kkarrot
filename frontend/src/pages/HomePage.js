import React, { useState, useEffect} from 'react';
import { Link } from 'react-router-dom';
import './HomePage.css';
import axios from 'axios';
import {fetchHomeFeed} from '../api';

const HomePage = () => {
  const [isLogin, setIsLogin] = useState('');
  const  [bookList, setBookList] = useState([]);
  
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
    fetchHomeFeed()
      .then((response) => {
        setBookList(JSON.parse(response.data["feed_lst"]));
      })
      .catch((error) => {
        console.log("Error while fetching books:", error);
      });
  }
  
  console.log(bookList)

  return (
    <div className="homepage">
      <header className="navbar">
      <Link to={`/`}  className='logo'>KKARROT</Link>
      </header>
      <div style={{width:"100vw"}}>
        <div>
          <div style={{display:"flex", width:"100%", backgroundColor:"#FDF1B2", justifyContent:"center"}}>
              <div style={{display:"flex", flexDirection:"column", justifyContent:"center"}}>
                  <div style={{fontWeight:900, fontSize:"30px", marginTop:  "20px", overflow:"hidden", whiteSpace:"nowrap", textOverflow:"ellipsis"}}>
                        믿을만한
                  </div>
                  <div style={{fontWeight:900, fontSize:"30px", marginTop:  "0px", overflow:"hidden", whiteSpace:"nowrap", textOverflow:"ellipsis"}}>
                        이웃 간 중고거래
                  </div>
                  <div style={{marginTop:  "18px", overflow:"hidden", whiteSpace:"nowrap", textOverflow:"ellipsis"}}>
                      동네 주민들과 가깝고 따뜻한 거래를
                  </div>
                  <div style={{marginTop:  "0px", overflow:"hidden", whiteSpace:"nowrap", textOverflow:"ellipsis"}}>
                      지금 경험해보세요.
                  </div>
              </div>

              <img src='/images/home_banner.jpg' alt='' style={{height:"315px"}}></img>

          </div>
          <section className="popular-products" style={{display:"flex", alignItems:'center', flexDirection:"column"}}>
            <div style={{fontWeight:600, fontSize: "35px", marginTop:"40px", marginBottom:"50px"}}>중고거래 인기매물</div>
            <div className="product-list">
              {bookList.map(product => (
                <Link to={`/product/${product.item_id}`} key={product.item_id} className="product-item">
                  <img src={product.images["hi_res"][0]} alt={product.title} style={{width:"223px", height:"223px", objectFit:"cover"}}/>
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


            <div className="view-more">
              <Link to= {isLogin ? "/explore" : "/login"} >인기매물 더 보기</Link>
            </div>
          </section>

        </div>
      </div>

      <footer>
        <p>&copy; 2024 KKARROT</p>
      </footer>
    </div>
  );
};

export default HomePage;
