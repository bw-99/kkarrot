import React from 'react';
import { Link } from 'react-router-dom';
import './ExplorePage.css';

const ExplorePage = () => {
  const products = [
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
    // 추가 아이템
  ];

  return (
    <div className="ExplorePage">
      <header className="navbar">
        <div className="logo">KKARROT</div>

      </header>
      <main>
        <div style={{display:"flex", width:"100%", backgroundColor:"#FDF1B2", justifyContent:"center"}}>
            <div style={{display:"flex", flexDirection:"column", justifyContent:"center"}}>
                <div style={{fontWeight:900, fontSize:"30px", marginTop:  "-50px", overflow:"hidden", whiteSpace:"nowrap", textOverflow:"ellipsis"}}>
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
          <div style={{fontWeight:"bold", fontSize: "25px", marginTop:"40px", marginBottom:"32px"}}>중고거래 인기매물</div>
          <div className="product-list">
            {products.map(product => (
              <Link to={`/product/${product.id}`} key={product.id} className="product-item">
                <img src={product.imageUrl} alt={product.name} style={{width:"223px", height:"223px", objectFit:"cover"}}/>
                <div className="product-info" style={{display:"flex", alignItems:"flex-start", flexDirection:"column"}}>
                  <div style={{overflow:"hidden", whiteSpace:"nowrap", textOverflow:"ellipsis"}}>
                    {product.name}
                  </div>
                  <div style={{fontWeight:"bold", marginTop:"8px"}}>{product.price}</div>
                  <div style={{marginTop:"8px"}}>Additional Informations...</div>
                </div>
              </Link>
            ))}
          </div>
          <div className="view-more">
            <Link to="/more-products">인기매물 더 보기</Link>
          </div>
        </section>

      </main>
      <footer>
        <p>&copy; 2024 KKARROT</p>
      </footer>
    </div>
  );
};

export default ExplorePage;
