import React, { useState, useEffect} from 'react';
import { useNavigate } from "react-router-dom";
import Session from 'react-session-api';
import './LoginPage.css';


const LoginPage = () => {
    const [id, setId] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate()

    // * 중복 로그인 방지
    useEffect(() => {
        let user_id = sessionStorage.getItem("user_id");
        if(!user_id){
            return
        }
        user_id = JSON.parse(user_id);

        if(((user_id >= 0) && (user_id <= 1999))) {
            navigate("/");
        }
      }, []);

    const handleIdChange = (e) => {
        setId(e.target.value);
        const idNumber = parseInt(e.target.value, 10);
        if (isNaN(idNumber) || idNumber < 0 || idNumber > 1999) {
          setError('ID는 0에서 1999 사이의 정수여야 합니다.');
        } else {
          setError('');
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        const idNumber = parseInt(id, 10);
        if (isNaN(idNumber) || idNumber < 0 || idNumber > 1999) {
          setError('ID는 0에서 1999 사이의 정수여야 합니다.');
        } else {
            sessionStorage.setItem("user_id", idNumber);
            setError('');
            navigate("/");
        }
      };
    

  return (
    <div className="login-page">
      <div className="login-container">
          <div className="logo">KKARROT</div>
        <form className="login-form">
        <input
            type="text"
            placeholder="아이디 (0-1999)"
            value={id}
            onChange={handleIdChange}
            required
          />
          <p className="error-message">{error}</p>
          {/* <p className="id-hint">ID는 0에서 1999 사이의 정수여야 합니다.</p> */}
          <button type="submit" onClick={handleSubmit} disabled={error} style={{backgroundColor: error ? "grey":"#ff6f00", marginTop:"20px"}}>서비스 이용하기</button>
        </form>
        <div className="extra-links">
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
