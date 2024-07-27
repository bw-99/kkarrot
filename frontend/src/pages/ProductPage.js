import React, { useState,useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import './ProductPage.css';

const ProductPage = () => {
  const { id } = useParams();
  const [viewMore, setViewMore] = useState('');
  const navigate = useNavigate();
  const [isLogin, setIsLogin] = useState(false);

  // * 비로그인 방지
  useEffect(() => {
    let user_id = sessionStorage.getItem("user_id");
    if(!user_id){
      navigate("/login");  
      return
    }
    setIsLogin(true);
  }, []);

  // * 비로그인 방지
  useEffect(() => {
    let user_id = sessionStorage.getItem("user_id");
    if(!user_id){
      navigate("/login");  
      return
    }
  }, []);

  useEffect(() => {
    if(!viewMore) {
      return
    }

    alert("load more");
    setViewMore(false);
    return
  }, [viewMore])
  const product = {
    id: id,
    name: '냉장고 팝니다 가져가셔야해요',
    category: "생활가전",
    date: "August 2, 2024",
    description: '결마당에 위치합니다 만원 내시고 가져가세요',
    price: '10,000원',
    imageUrl: ['/images/fridge.jpg', '/images/fridge.jpg', '/images/fridge.jpg'], // 실제 이미지 경로
    popularProducts: [
        { id: 1, name: '스팸 일괄', price: '15,000원', imageUrl: '/images/spam.jpg' },
        { id: 2, name: '냉장고', price: '10,000원', imageUrl: '/images/fridge.jpg' },
        { id: 3, name: '3x6컨테이너팝니다.', price: '160만원', imageUrl: '/images/container.jpg' },
        { id: 4, name: '롯데 제습기', price: '30,000원', imageUrl: '/images/dehumidifier.jpg' },
        { id: 5, name: '다이슨 선풍기', price: '60,000원', imageUrl: '/images/fan.jpg' },
        { id: 6, name: 'S21 정상이에요', price: '20,000원', imageUrl: '/images/s21.jpg' },
        { id: 7, name: '두바이 초콜렛', price: '30,000원', imageUrl: '/images/chocolate.jpg' },
        { id: 8, name: '오딧세이 투볼 텐 트리플 퍼터', price: '180,000원', imageUrl: '/images/putter.jpg' },
        { id: 9, name: '마샬 스피커', price: '80,000원', imageUrl: '/images/speaker.jpg' },
        { id: 10, name: '전동 킥보드 자전거', price: '50,000원', imageUrl: '/images/bike.jpg' },
        { id: 11, name: '워치6 클래식 47mm 블루투스', price: '100,000원', imageUrl: '/images/watch.jpg' },
        { id: 12, name: '혼다 예초기', price: '90,000원', imageUrl: '/images/mower.jpg' },
      ]
  };

  return (
    isLogin &&
    <div className="product-page">
      <header className="navbar">
        <Link to={`/`}  className='logo'>KKARROT</Link>
      </header>
      <div className='product-layout'>
      <main>
        <div className="product-details">
          <img src={product.imageUrl[0]} alt={product.name} className="product-image" />
          <hr></hr>
          <div className="product-info">
          <div style={{fontSize: "20px", fontWeight: "600"}}>{product.name}</div>
          <div style={{fontSize: "12px", fontWeight: "100"}}>{product.category}</div>
          <div style={{fontSize: "16px", fontWeight: "600"}}>{product.price}</div>
          <div style={{fontSize: "16px", fontWeight: "500", marginTop:"14px"}}>{product.description}</div>
          </div>
        </div>
        <div className="popular-section">
          <h3>당근 인기중고</h3>
          <div className="popular-products-grid">
          {product.popularProducts.map(item => (
              <Link to={`/product/${item.id}`} key={item.id} className="product-item">
                <img src={item.imageUrl} alt={item.name} style={{width:"223px", height:"223px", objectFit:"cover"}}/>
                <div className="product-info" style={{display:"flex", alignItems:"flex-start", flexDirection:"column"}}>
                  <div style={{overflow:"hidden", whiteSpace:"nowrap", textOverflow:"ellipsis"}}>
                    {item.name}
                  </div>
                  <div style={{fontWeight:"bold", marginTop:"8px"}}>{item.price}</div>
                  <div style={{marginTop:"8px"}}>Additional Informations...</div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </main>

      <div className="load-more">
              <button onClick={()=>{
                setViewMore(true);
              }}>더보기</button>
            </div>

      </div>
            <footer>
        <p>&copy; 2024 당근</p>
      </footer> 
    </div>
    
  );
};

export default ProductPage;
