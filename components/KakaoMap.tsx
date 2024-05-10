'use client'
import {useState} from 'react'
import {Map, MapMarker} from 'react-kakao-maps-sdk'
import {StopInfo, CenterInfo} from '@/app/types'

const PREFIX_ADDR = 'https://rst0070.github.io/HITS_ddareungi'

function getImgSrcByRank(rank:number){
  if(rank <= 328) return PREFIX_ADDR+"/img/markerRed.png"
  if(rank <= 1000) return PREFIX_ADDR+"/img/markerOrange.png"
  if(rank <= 1968) return PREFIX_ADDR+"/img/markerYellow.png"
  return PREFIX_ADDR+"/img/markerGreen.png"
}

function Marker(props: {stopInfo: StopInfo, openAtStart:boolean}){
  let img_src = getImgSrcByRank( props.stopInfo.rank )
  let urlNavigation = 'https://map.kakao.com/link/to/'+props.stopInfo.address+','+props.stopInfo.latitude+','+props.stopInfo.longitude
  let urlRoadView = "https://map.kakao.com/link/roadview/"+props.stopInfo.latitude+","+props.stopInfo.longitude
  // if(props.stopInfo.rank == 1)
  //   console.log(img_src)
  const [isOpen, setIsOpen] = useState(props.openAtStart)

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
      clickable={true}
      onClick={() => {console.log(props.stopInfo.stop_id);setIsOpen(!isOpen);}}
    >
      {isOpen && (
          <div style={{ minWidth: "150px" }}>
            <img
              alt="close"
              width="14"
              height="13"
              src="https://t1.daumcdn.net/localimg/localimages/07/mapjsapi/2x/bt_close.gif"
              style={{
                position: "absolute",
                right: "5px",
                top: "5px",
                cursor: "pointer",
              }}
              onClick={() => setIsOpen(false)}
            />
            <div style={{ padding: "5px", color: "#000" }}>
              <p>{props.stopInfo.address}</p>
              <button type="button" onClick={() => location.href=urlNavigation}>길찾기</button>
              <button type="button" onClick={() => location.href=urlRoadView}>로드뷰</button>
              {/* <div style={{display: 'flex', padding: '5px', flexDirection: 'row', justifyContent: 'center'}}>
                
              </div> */}
            </div>
          </div>
        )}
    </MapMarker>
  );
}

function MarkerList(props: {stopList: StopInfo[], centerInfo: CenterInfo}){
    console.log(props.stopList[0].rank)
    let markers = []
    for(let i = 0; i < props.stopList.length; i++){
      markers.push(<Marker key={props.stopList[i].stop_id} stopInfo={props.stopList[i]} openAtStart={props.stopList[i].stop_id == props.centerInfo.id}/>)
    }
    return (
      <>
        {markers}
      </>
    )
}


export default function KakaoMap(props: {stopList:StopInfo[], centerInfo:CenterInfo}){

  const start_position = {lat: props.centerInfo.latitude, lng: props.centerInfo.longitude}
  return (
    <div className="map-container">
      <Map 
          center={{ lat: start_position.lat, lng: start_position.lng }} 
          style={{ width: '100%', height: '100%' }} 
          level={4}
      >
        <MarkerList stopList={props.stopList} centerInfo={props.centerInfo}/>
      </Map>
    </div>
  );
};