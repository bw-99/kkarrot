import React from 'react';
import { Link } from 'react-router-dom';
import './HomePage.css';

const HomePage = () => {
  const products = [
    { id: 1, name: '스팸 일괄', price: '15,000원', imageUrl: '/images/spam.jpg' },
    { id: 2, name: '냉장고', price: '10,000원', imageUrl: '/images/fridge.jpg' },
    { id: 3, name: '단호박', price: '500원', imageUrl: '/images/pumpkin.jpg' },
    { id: 4, name: '롯데 제습기', price: '30,000원', imageUrl: '/images/dehumidifier.jpg' },
    { id: 5, name: '평상', price: '10,000원', imageUrl: '/images/bed.jpg' },
    { id: 6, name: 'S21 정상이에요', price: '20,000원', imageUrl: '/images/s21.jpg' },
    { id: 7, name: '두바이 초콜렛', price: '30,000원', imageUrl: '/images/chocolate.jpg' },
    { id: 8, name: '오딧세이 투볼 텐 트리플 퍼터', price: '180,000원', imageUrl: '/images/putter.jpg' },
    { id: 9, name: '마샬 스피커', price: '80,000원', imageUrl: '/images/speaker.jpg' },
    { id: 10, name: '전동 킥보드 자전거', price: '50,000원', imageUrl: '/images/bike.jpg' },
    { id: 11, name: '워치6 클래식 47mm 블루투스', price: '100,000원', imageUrl: '/images/watch.jpg' },
    { id: 12, name: '스프레 트리플 탭 뉴 본세트', price: '90,000원', imageUrl: '/images/set.jpg' },
    // 추가 아이템
  ];

  return (
    <div className="homepage">
      <header className="navbar">
        <div className="logo">짭근</div>

      </header>
      <main>
        <div style={{display:"flex", width:"100vw", backgroundColor:"#FDF1B2", justifyContent:"center"}}>
            <div style={{display:"flex", flexDirection:"column", justifyContent:"center"}}>
                <div style={{marginTop:  "-50px"}}>
                    <h1>
                        믿을만한
                    </h1>
                </div>
                <div style={{marginTop:  "-30px"}}>
                    <h1>
                        이웃 간 중고거래
                    </h1>
                </div>
                <div style={{marginTop:  "0px"}}>
                    동네 주민들과 가깝고 따뜻한 거래를
                </div>
                <div style={{marginTop:  "0px"}}>
                    지금 경험해보세요.
                </div>
            </div>

            <img src='/images/home_banner.jpg' alt='' style={{height:"315px"}}></img>

        </div>
        <section className="popular-products">
          <h3>중고거래 인기매물</h3>
          <div className="product-list">
            {products.map(product => (
              <Link to={`/product/${product.id}`} key={product.id} className="product-item">
                <img src={product.imageUrl} alt={product.name} />
                <div className="product-info">
                  <h4>{product.name}</h4>
                  <p>{product.price}</p>
                </div>
              </Link>
            ))}
          </div>
        </section>
        <section className="more-categories">
          <h4>더 구경하기</h4>
          <p>여러 카테고리를 확인해보세요.</p>
          {/* 더 많은 카테고리 정보를 여기에 추가 */}
        </section>
      </main>
      <footer>
        <p>&copy; 2024 당근</p>
      </footer>
    </div>
  );
};

export default HomePage;
