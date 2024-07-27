import React, { useState,useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import './ProductPage.css';
import {fetchProductFeed} from '../api';

const ProductPage = () => {
  const { id } = useParams();
  const [viewMore, setViewMore] = useState('');
  const navigate = useNavigate();
  const [isLogin, setIsLogin] = useState(false);
  const  [feedList, setFeedList] = useState('');
  const  [productDetail, setProductDetail] = useState('');

  // * 비로그인 방지
  useEffect(() => {
    let user_id = sessionStorage.getItem("user_id");
    if(!user_id){
      navigate("/login");  
      return
    }
    setIsLogin(true);
  }, []);

  const handleFetch = (id) => {
    fetchProductFeed(id)
      .then((data) => {
        setFeedList(data["feed_lst"]);
        setProductDetail(data["item"]);
      })
      .catch((error) => {
        console.log("Error while fetching feeds:", error);
      });
  }
  
  useEffect(() => {
    window.scrollTo(0, 0);
    handleFetch(id);
  }, [id]);
  

  useEffect(() => {
    if(!viewMore) {
      return
    }
    alert("load more");
    setViewMore(false);
    return
  }, [viewMore])

  return (
    isLogin && productDetail && feedList &&
    <div className="product-page">
      <header className="navbar">
        <Link to={`/`}  className='logo'>KKARROT</Link>
      </header>
      <div className='product-layout'>
      <main>
        <div className="product-details">
          <img style={{display:"block",}} src={productDetail.images.hi_res[0]} alt={productDetail.title} className="product-image" />
          <hr></hr>
          <div className="product-info">
          <div style={{fontSize: "20px", fontWeight: "600"}}>{productDetail.title}</div>
          <div style={{fontSize: "12px", fontWeight: "100"}}>{productDetail.main_category}</div>
          <div style={{fontSize: "16px", fontWeight: "600"}}>{productDetail.price}</div>
          <div style={{fontSize: "16px", fontWeight: "500", marginTop:"14px"}}>{productDetail.description}</div>
          </div>
        </div>
        <div className="popular-section">
          <h3>당근 인기중고</h3>
          <div className="popular-products-grid">
          {feedList.map(item => (
              <Link to={`/product/${item.item_id}`} key={item.item_id} className="product-item">
                <img src={item.images.hi_res[0]} alt={item.title} style={{display:"block",width:"223px", height:"223px", objectFit:"cover"}}/>
                <div className="product-info" style={{display:"flex", alignItems:"flex-start", flexDirection:"column"}}>
                  <div style={{overflow:"hidden", whiteSpace:"nowrap", textOverflow:"ellipsis"}}>
                    {item.title}
                  </div>
                  <div style={{fontWeight:"bold", marginTop:"8px"}}>{item.price}$</div>
                  <div style={{marginTop:"8px"}}>Num ratings: {item.rating_number}</div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </main>

      {/* <div className="load-more">
              <button onClick={()=>{
                setViewMore(true);
              }}>더보기</button>
            </div> */}

      </div>
      <footer>
        <p>&copy; 2024 KKARROT</p>
      </footer>
    </div>
    
  );
};

export default ProductPage;
