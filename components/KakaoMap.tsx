import Script from 'next/script'
import React from 'react'
import {Map, MapMarker} from 'react-kakao-maps-sdk'

const APP_KEY = '633117026be1caa09108a7721bed0b2d'
const KAKAO_SDK_URL = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${APP_KEY}&autoload=false`;
const START_POSITION = {latitude: 37.4961, longitude: 127.0113}

const KakaoMap 
= ({}) => {
  return (
    <div className="mapDiv">
      <Script src={KAKAO_SDK_URL} strategy="beforeInteractive" />
      <Map 
        center={{ lat: START_POSITION.latitude, lng: START_POSITION.longitude }}
        style={{ width: '100%', height: '100%' }} 
      >
        <MapMarker // 마커를 생성합니다
        position={{
          // 마커가 표시될 위치입니다
          lat: START_POSITION.latitude,
          lng: START_POSITION.longitude,
        }}
      />
      </Map>
    </div>
  );
};

export default KakaoMap;