import React from 'react';
import { useParams } from 'react-router-dom';
import './ProductPage.css';

const ProductPage = () => {
  const { id } = useParams();

  const product = {
    id: id,
    name: '스팸 일괄',
    price: '15,000원',
    description: '사진에 보이는 스팸 일괄 팝니다. 나는 느낌으로 싼 가격에 파니 네고 불가능합니다.',
    imageUrl: '/images/spam.jpg',
    location: '경기도 의정부시 의정부동',
    seller: '곽진',
    temperature: '38.7°C',
  };

  return (
    <div className="product-page">
      <div className="product-header">
        <h1>{product.name}</h1>
        <div className="price">{product.price}</div>
      </div>
      <img src={product.imageUrl} alt={product.name} className="product-image" />
      <div className="product-details">
        <p>{product.description}</p>
        <p>판매자: {product.seller}</p>
        <p>위치: {product.location}</p>
        <p>거래온도: {product.temperature}</p>
      </div>
    </div>
  );
};

export default ProductPage;
