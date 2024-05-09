import Script from 'next/script'
import React from 'react'
import {Map, MapMarker} from 'react-kakao-maps-sdk'
import {StopInfo, CenterInfo} from '@/app/types'

const APP_KEY = '633117026be1caa09108a7721bed0b2d'
const KAKAO_SDK_URL = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${APP_KEY}&autoload=false`;

function getImgSrcByRank(rank:number){
  if(rank <= 328) return "/img/markerRed.png"
  if(rank <= 1000) return "/img/markerOrange.png"
  if(rank <= 1968) return "/img/markerYellow.png"
  return "/img/markerGreen.png"
}
function Marker(props: {stopInfo: StopInfo}){
  let img_src = getImgSrcByRank( props.stopInfo.rank )
  
  return (
    <MapMarker // 마커를 생성합니다
      key={props.stopInfo.stop_id}
      position={{
        // 마커가 표시될 위치입니다
        lat: props.stopInfo.latitude,
        lng: props.stopInfo.longitude,
      }}
      image={{
        src: img_src, 
        size: {
          width: 24,
          height: 35
        }, // 마커이미지의 크기입니다
      }}
      title={props.stopInfo.address}
    />
  );
}

function MarkerList(props: {stopList: StopInfo[]}){
    return (
      <>
        {
          props.stopList.map((value, index, arr) => <Marker stopInfo={value} />)
        }
    </>
    )
}


export default function KakaoMap(props: {stopList:StopInfo[], centerInfo:CenterInfo}){

  const start_position = {lat: props.centerInfo.latitude, lng: props.centerInfo.longitude}

  return (
    <div className="map-container">
      <Script src={KAKAO_SDK_URL} strategy="beforeInteractive" />
      <Map 
          center={{ lat: start_position.lat, lng: start_position.lng }} 
          style={{ width: '100%', height: '100%' }} 
          level={4}
      >
        <MarkerList stopList={props.stopList} />
      </Map>
    </div>
  );
};