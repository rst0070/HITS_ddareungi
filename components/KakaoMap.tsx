import Script from 'next/script'
import React from 'react'
import {Map} from 'react-kakao-maps-sdk'

const APP_KEY = '633117026be1caa09108a7721bed0b2d'
const KAKAO_SDK_URL = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${APP_KEY}&autoload=false`;

const KakaoMap = () => {
  return (
    <div className="mapDiv">
      <Script src={KAKAO_SDK_URL} strategy="beforeInteractive" />
      <Map center={{ lat: 33.450701, lng: 126.570667 }} style={{ width: '100%', height: '100%' }} />
    </div>
  );
};

export default KakaoMap;