'use client'
import { MouseEventHandler, useState } from "react";
import { StopInfo, CenterInfo } from "@/app/types";
import KakaoMap from "./KakaoMap";

function StopElement(props: {order:string, stopInfo:StopInfo, clickListener:Function}){
    const handleClick: MouseEventHandler = (event) => {
        props.clickListener(props.stopInfo)
    };

    return (
      <div className="stop_element" onClick={handleClick}>
        <div className="stop_element_order">{props.order}</div>
        <div className="stop_element_score">{props.stopInfo.score}</div>
        <div className="stop_element_addr">{props.stopInfo.address}</div>
      </div>
    )
}
  
function StopList(props: {stopList:StopInfo[], clickListener:Function}){
    let el_list = []
    for(let i=0; i < props.stopList.length; i++)
      el_list.push(<StopElement order={String(i+1)} stopInfo={props.stopList[i]} clickListener={props.clickListener}/>)
  
    return (
      <div className="stop_scroll">
        {el_list}
      </div>
    )
}


export default function Container(props: {title:string, scores:StopInfo[]}){

    let initialCenterInfo: CenterInfo = {id: props.scores[0].stop_id, latitude: props.scores[0].latitude, longitude: props.scores[0].longitude}
    
    const [centerInfo, setCenterInfo] = useState(initialCenterInfo)

    const handleClick:Function = (stopInfo:StopInfo) =>{
      setCenterInfo({
        id: stopInfo.stop_id,
        latitude: stopInfo.latitude,
        longitude: stopInfo.longitude
      })
    }

    return (
        <div className="grid-container">
          <div className="grid-item">
            <KakaoMap stopList={props.scores} centerInfo={centerInfo}/>
          </div>
          <div className="grid-item">
            <StopList stopList={props.scores} clickListener={handleClick}/>
          </div>
        </div>
    );
}